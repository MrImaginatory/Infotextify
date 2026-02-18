from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Response
from fastapi.responses import HTMLResponse
from typing import Optional
from PIL import Image
import io
from pdf2image import convert_from_bytes

from app.schemas.ocr import OCRResponse, FullAnalysisResponse, AIAnalysisResponse, PDFPageAnalysisResponse, PageAnalysis
from app.services import ocr_service, nlp_service, report_service, correction_service, gemini_service, ollama_service


router = APIRouter()

async def extract_text_from_file(
    file: UploadFile, 
    lang: str, 
    contrast: float, 
    brightness: float, 
    sharpness: float
) -> str:
    if file.content_type == "application/pdf":
        file_bytes = await file.read()
        try:
            images = convert_from_bytes(file_bytes)
        except Exception as e:
            raise HTTPException(400, detail=f"Invalid PDF file: {str(e)}")
            
        full_text = []
        for i, image in enumerate(images):
            try:
                page_text = ocr_service.extract_text(
                    image, 
                    lang=lang, 
                    contrast=contrast, 
                    brightness=brightness, 
                    sharpness=sharpness
                )
                full_text.append(f"--- Page {i+1} ---\n{page_text}")
            except Exception as e:
                full_text.append(f"--- Page {i+1} (Error) ---\n[{str(e)}]")
                
        return "\n\n".join(full_text)
        
    elif file.content_type and file.content_type.startswith("image/"):
        image_data = await file.read()
        try:
            image = Image.open(io.BytesIO(image_data))
        except Exception:
            raise HTTPException(400, detail="Invalid image file")
            
        return ocr_service.extract_text(
            image, 
            lang=lang, 
            contrast=contrast, 
            brightness=brightness, 
            sharpness=sharpness
        )
    else:
        raise HTTPException(400, detail="File must be an image or PDF")


@router.post("/extract", response_model=OCRResponse)
async def extract_text_endpoint(
    file: UploadFile = File(...),
    lang: str = Form("eng"),
    autocorrect: bool = Form(False),
    contrast: float = Form(1.0),
    brightness: float = Form(1.0),
    sharpness: float = Form(1.0)
    ):
    """
    Extract text from an uploaded image file.
    """
    try:
        text = await extract_text_from_file(
            file, 
            lang=lang, 
            contrast=contrast, 
            brightness=brightness, 
            sharpness=sharpness
        )
        
        corrected_text = None
        if autocorrect:
            corrected_text = correction_service.correct_text(text)
            
        return OCRResponse(text=text, corrected_text=corrected_text)
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@router.post("/analyze", response_model=FullAnalysisResponse)
async def analyze_text_endpoint(
    file: UploadFile = File(...),
    lang: str = Form("eng"),
    autocorrect: bool = Form(False),
    contrast: float = Form(1.0),
    brightness: float = Form(1.0),
    sharpness: float = Form(1.0)
    ):
    """
    Extract text and perform NLP analysis.
    """
    try:
        # Step 1: OCR
        text = await extract_text_from_file(
            file, 
            lang=lang, 
            contrast=contrast, 
            brightness=brightness, 
            sharpness=sharpness
        )
        
        # Step 2: NLP
        nlp_result = None
        if text.strip():
             nlp_result = nlp_service.process_text(text)
             
        corrected_text = None
        if autocorrect:
            corrected_text = correction_service.correct_text(text)

        return FullAnalysisResponse(
            text=text,
            corrected_text=corrected_text,
            nlp_analysis=nlp_result
        )

    except Exception as e:
        raise HTTPException(500, detail=f"Processing error: {str(e)}")

@router.post("/analyze/text")
async def analyze_text_report_endpoint(
    file: UploadFile = File(...),
    lang: str = Form("eng"),
    autocorrect: bool = Form(False),
    contrast: float = Form(1.0),
    brightness: float = Form(1.0),
    sharpness: float = Form(1.0)
    ):
    """
    Extract text and perform NLP analysis, returning a formatted text report.
    This mimics the original CLI tool output.
    """
    try:
        # Step 1: OCR
        text = await extract_text_from_file(
            file, 
            lang=lang, 
            contrast=contrast, 
            brightness=brightness, 
            sharpness=sharpness
        )
        
        # Step 2: NLP
        nlp_result = None
        if text.strip():
             nlp_result = nlp_service.process_text(text)
             
        # Step 3: Generate Report
        corrected_text = None
        if autocorrect:
            corrected_text = correction_service.correct_text(text)
            
        report = report_service.generate_report(text, nlp_result, corrected_text=corrected_text)
        
        return Response(content=report, media_type="text/plain")

    except Exception as e:
        raise HTTPException(500, detail=f"Processing error: {str(e)}")

@router.post("/analyze/html", response_class=HTMLResponse)
async def analyze_html_report_endpoint(
    file: UploadFile = File(...),
    lang: str = Form("eng"),
    autocorrect: bool = Form(False),
    contrast: float = Form(1.0),
    brightness: float = Form(1.0),
    sharpness: float = Form(1.0)
    ):
    """
    Extract text and perform NLP analysis, returning an HTML report.
    """
    try:
        # Step 1: OCR
        text = await extract_text_from_file(
            file, 
            lang=lang, 
            contrast=contrast, 
            brightness=brightness, 
            sharpness=sharpness
        )
        
        # Step 2: NLP
        nlp_result = None
        if text.strip():
             nlp_result = nlp_service.process_text(text)
             
        # Step 3: Generate HTML Report
        corrected_text = None
        if autocorrect:
            corrected_text = correction_service.correct_text(text)

        html_report = report_service.generate_html_report(text, nlp_result, lang, corrected_text=corrected_text)
        
        return HTMLResponse(content=html_report)

    except Exception as e:
        raise HTTPException(500, detail=f"Processing error: {str(e)}")


@router.post("/analyze/ai", response_model=AIAnalysisResponse)
async def analyze_ai_endpoint(
    file: UploadFile = File(...),
    lang: str = Form("eng"),
    autocorrect: bool = Form(False),
    contrast: float = Form(1.0),
    brightness: float = Form(1.0),
    sharpness: float = Form(1.0)
    ):
    """
    Extract text, perform NLP analysis, and use Gemini AI for advanced correction and summarization.
    """
    try:
        # Step 1: OCR
        text = await extract_text_from_file(
            file, 
            lang=lang, 
            contrast=contrast, 
            brightness=brightness, 
            sharpness=sharpness
        )
        
        # Step 2: NLP
        nlp_result = None
        if text.strip():
             nlp_result = nlp_service.process_text(text)
             
        # Step 3: Traditional correction (if requested)
        corrected_text = None
        if autocorrect:
            corrected_text = correction_service.correct_text(text)
        
        # Step 4: Gemini AI correction and summarization
        ai_result = gemini_service.get_ai_correction_and_summary(text)

        return AIAnalysisResponse(
            text=text,
            corrected_text=corrected_text,
            nlp_analysis=nlp_result,
            ai_corrected_text=ai_result.get("corrected_text"),
            summary=ai_result.get("summary"),
            ai_score=ai_result.get("ai_score")
        )

    except Exception as e:
        raise HTTPException(500, detail=f"Processing error: {str(e)}")


@router.post("/analyze/ollama", response_model=AIAnalysisResponse)
async def analyze_ollama_endpoint(
    file: UploadFile = File(...),
    lang: str = Form("eng"),
    autocorrect: bool = Form(False),
    contrast: float = Form(1.0),
    brightness: float = Form(1.0),
    sharpness: float = Form(1.0)
    ):
    """
    Extract text, perform NLP analysis, and use local Ollama AI for advanced correction and summarization.
    """
    try:
        # Step 1: OCR
        text = await extract_text_from_file(
            file, 
            lang=lang, 
            contrast=contrast, 
            brightness=brightness, 
            sharpness=sharpness
        )
        
        # Step 2: NLP
        nlp_result = None
        if text.strip():
             nlp_result = nlp_service.process_text(text)
             
        # Step 3: Traditional correction (if requested)
        corrected_text = None
        if autocorrect:
            corrected_text = correction_service.correct_text(text)
        
        # Step 4: Ollama AI correction and summarization
        ai_result = ollama_service.get_ai_correction_and_summary(text)

        return AIAnalysisResponse(
            text=text,
            corrected_text=corrected_text,
            nlp_analysis=nlp_result,
            ai_corrected_text=ai_result.get("corrected_text"),
            summary=ai_result.get("summary"),
            ai_score=ai_result.get("ai_score")
        )

    except Exception as e:
        raise HTTPException(500, detail=f"Processing error: {str(e)}")


@router.post("/analyze/pdf-pages", response_model=PDFPageAnalysisResponse)
async def analyze_pdf_per_page_endpoint(
    file: UploadFile = File(...),
    lang: str = Form("eng"),
    contrast: float = Form(1.0),
    brightness: float = Form(1.0),
    sharpness: float = Form(1.0)
    ):
    """
    Per-page PDF analysis: extracts text from each page individually,
    then generates an AI summary and quality score for every page using Gemini.
    Only accepts PDF files.
    """
    # Validate that the uploaded file is a PDF
    if file.content_type != "application/pdf":
        raise HTTPException(400, detail="This endpoint only accepts PDF files. Use /analyze/ai for images.")

    try:
        file_bytes = await file.read()
        try:
            images = convert_from_bytes(file_bytes)
        except Exception as e:
            raise HTTPException(400, detail=f"Invalid PDF file: {str(e)}")

        # Step 1: OCR all pages first
        pages_ocr = []
        for i, image in enumerate(images):
            page_number = i + 1
            try:
                page_text = ocr_service.extract_text(
                    image,
                    lang=lang,
                    contrast=contrast,
                    brightness=brightness,
                    sharpness=sharpness
                )
            except Exception as e:
                page_text = f"[OCR Error on page {page_number}: {str(e)}]"
            
            pages_ocr.append({"page_number": page_number, "text": page_text})

        # Step 2: Single batch AI analysis call (Ollama) for all pages
        pages_with_text = [p for p in pages_ocr if p["text"].strip()]
        batch_results = ollama_service.get_batch_pdf_analysis(pages_with_text) if pages_with_text else []

        # Map batch results back by page number
        batch_map = {}
        for idx, page_data in enumerate(pages_with_text):
            if idx < len(batch_results):
                batch_map[page_data["page_number"]] = batch_results[idx]

        # Step 3: Build final results, falling back to Gemini for pages where batch failed
        pages_analysis = []
        for page_data in pages_ocr:
            pn = page_data["page_number"]
            ai_result = batch_map.get(pn, {"corrected_text": None, "summary": None, "ai_score": None})

            # Fallback to Gemini if Ollama batch didn't produce results for this page
            if ai_result.get("summary") is None and ai_result.get("ai_score") is None and page_data["text"].strip():
                ai_result = gemini_service.get_ai_correction_and_summary(page_data["text"])

            pages_analysis.append(PageAnalysis(
                page_number=pn,
                text=page_data["text"],
                summary=ai_result.get("summary"),
                ai_score=ai_result.get("ai_score"),
                ai_corrected_text=ai_result.get("corrected_text")
            ))

        # Compute overall score (average of all valid page scores)
        valid_scores = [p.ai_score for p in pages_analysis if p.ai_score is not None]
        overall_score = round(sum(valid_scores) / len(valid_scores), 2) if valid_scores else None

        # Compute overall summary (combine page summaries)
        page_summaries = [
            f"Page {p.page_number}: {p.summary}"
            for p in pages_analysis
            if p.summary
        ]
        overall_summary = "\n".join(page_summaries) if page_summaries else None

        return PDFPageAnalysisResponse(
            total_pages=len(images),
            pages=pages_analysis,
            overall_summary=overall_summary,
            overall_score=overall_score
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=f"Processing error: {str(e)}")