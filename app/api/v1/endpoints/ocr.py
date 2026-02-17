from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Response
from fastapi.responses import HTMLResponse
from typing import Optional
from PIL import Image
import io

from app.schemas.ocr import OCRResponse, FullAnalysisResponse, AIAnalysisResponse
from app.services import ocr_service, nlp_service, report_service, correction_service, gemini_service

router = APIRouter()

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
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(400, detail="File must be an image")
    
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        text = ocr_service.extract_text(
            image, 
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
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(400, detail="File must be an image")

    try:
        # Step 1: OCR
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        text = ocr_service.extract_text(
            image, 
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
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(400, detail="File must be an image")

    try:
        # Step 1: OCR
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        text = ocr_service.extract_text(
            image, 
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
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(400, detail="File must be an image")

    try:
        # Step 1: OCR
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        text = ocr_service.extract_text(
            image, 
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
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(400, detail="File must be an image")

    try:
        # Step 1: OCR
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        text = ocr_service.extract_text(
            image, 
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