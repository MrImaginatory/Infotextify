"""
Ollama AI Service for text correction and summarization.
"""
import requests
import re
from typing import Optional, Dict
from app.core.config import settings

# Configure Ollama API
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "glm-5:cloud"

def get_ai_correction_and_summary(text: str) -> Dict[str, Optional[str]]:
    """
    Use Ollama (local) to correct OCR text and generate a summary.
    
    Args:
        text: The extracted OCR text to process
        
    Returns:
        Dictionary with 'corrected_text', 'summary', and 'ai_score' keys
    """
    try:
        # Create prompt for correction, summary, and quality score
        prompt = f"""Please analyze the following OCR-extracted text and provide:
1. A corrected version of the text. IMPORTANT: Be conservative. Only fix clear spelling and OCR errors. Do NOT change the vocabulary or sentence structure unless it is completely unintelligible. Maintain the original meaning and style exactly.
2. A brief summary of the text content
3. A quality score (0-100) based on the content of the provided "OCR Text" below, evaluating its readability and accuracy.
   - 90-100: Text is very clear and perfectly readable
   - 70-89: Text is mostly clear with minor errors
   - 50-69: Text is readable but has noticeable errors
   - 30-49: Text is difficult to read with many errors
   - 0-29: Text is almost illegible

Format your response as:
CORRECTED TEXT:
[corrected text here]

SUMMARY:
[summary here]

SCORE:
[numerical score 0-100]

OCR Text:
{text}
"""
        
        # Prepare payload for Ollama
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 8192,  # Maximize output token limit
                "num_ctx": 8192       # Increase context window size
            }
        }
        
        # Generate response
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120) 
        # Increased timeout as local inference might take time
        
        if response.status_code != 200:
            print(f"Error calling Ollama API: Status {response.status_code}, {response.text}")
            return {
                "corrected_text": None,
                "summary": None,
                "ai_score": None
            }
            
        result_json = response.json()
        response_text = result_json.get("response", "")
        
        # Extract corrected text, summary, and score
        corrected_text = None
        summary = None
        ai_score = None
        
        if "CORRECTED TEXT:" in response_text and "SUMMARY:" in response_text and "SCORE:" in response_text:
            # Split by SUMMARY first
            parts = response_text.split("SUMMARY:")
            corrected_part = parts[0].replace("CORRECTED TEXT:", "").strip()
            
            # Split remaining by SCORE
            if len(parts) > 1:
                summary_and_score = parts[1].split("SCORE:")
                summary_part = summary_and_score[0].strip()
                
                # Extract score
                if len(summary_and_score) > 1:
                    score_text = summary_and_score[1].strip()
                    try:
                        # Extract first number found in score section
                        score_match = re.search(r'\d+\.?\d*', score_text)
                        if score_match:
                            ai_score = float(score_match.group())
                    except:
                        ai_score = None
                
                corrected_text = corrected_part
                summary = summary_part
        else:
            # Fallback parsing - attempt to salvage what we can
            corrected_text = response_text
            summary = "Unable to generate summary"
            ai_score = None
        
        return {
            "corrected_text": corrected_text,
            "summary": summary,
            "ai_score": ai_score
        }
        
    except Exception as e:
        print(f"Error calling Ollama API: {str(e)}")
        return {
            "corrected_text": None,
            "summary": None,
            "ai_score": None
        }


def get_batch_pdf_analysis(pages_text: list[dict]) -> list[dict]:
    """
    Analyze all PDF pages in a single Ollama call.
    
    Args:
        pages_text: List of dicts with 'page_number' and 'text' keys
        
    Returns:
        List of dicts with 'corrected_text', 'summary', 'ai_score' per page
    """
    default_result = {"corrected_text": None, "summary": None, "ai_score": None}
    
    if not pages_text:
        return []

    try:
        # Build the combined prompt with all pages
        pages_block = ""
        for page in pages_text:
            pages_block += f"\n=== PAGE {page['page_number']} ===\n{page['text']}\n"

        prompt = f"""You are analyzing a multi-page PDF document. Below is OCR-extracted text for each page.
For EACH page, provide:
1. A corrected version of the text (be conservative — only fix clear OCR/spelling errors, preserve original meaning and style)
2. A brief summary of the content
3. A quality score (0-100) based on readability and accuracy:
   - 90-100: Very clear and perfectly readable
   - 70-89: Mostly clear with minor errors
   - 50-69: Readable but has noticeable errors
   - 30-49: Difficult to read with many errors
   - 0-29: Almost illegible

You MUST format your response EXACTLY like this for EACH page (repeat this block for every page):

PAGE 1:
CORRECTED TEXT:
[corrected text here]

SUMMARY:
[summary here]

SCORE:
[numerical score 0-100]

PAGE 2:
CORRECTED TEXT:
[corrected text here]

SUMMARY:
[summary here]

SCORE:
[numerical score 0-100]

... and so on for all pages.

Here is the OCR text:
{pages_block}
"""

        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 16384,
                "num_ctx": 131072
            }
        }

        response = requests.post(OLLAMA_API_URL, json=payload, timeout=300)

        if response.status_code != 200:
            print(f"Error calling Ollama API (batch): Status {response.status_code}, {response.text}")
            return [dict(default_result) for _ in pages_text]

        result_json = response.json()
        response_text = result_json.get("response", "")

        # Parse per-page results from the response
        results = _parse_batch_response(response_text, len(pages_text))
        return results

    except Exception as e:
        print(f"Error calling Ollama API (batch): {str(e)}")
        return [dict(default_result) for _ in pages_text]


def _parse_batch_response(response_text: str, num_pages: int) -> list[dict]:
    """
    Parse the batch response into per-page results.
    Splits by 'PAGE N:' markers and extracts CORRECTED TEXT, SUMMARY, SCORE for each.
    """
    default_result = {"corrected_text": None, "summary": None, "ai_score": None}
    results = []

    # Split by PAGE markers (PAGE 1:, PAGE 2:, etc.)
    page_pattern = re.compile(r'PAGE\s+(\d+)\s*:', re.IGNORECASE)
    page_splits = page_pattern.split(response_text)

    # page_splits will be like: [preamble, "1", page1_content, "2", page2_content, ...]
    # Skip preamble (index 0), then take pairs of (page_num, content)
    page_contents = {}
    for i in range(1, len(page_splits) - 1, 2):
        try:
            page_num = int(page_splits[i])
            content = page_splits[i + 1]
            page_contents[page_num] = content
        except (ValueError, IndexError):
            continue

    for page_idx in range(1, num_pages + 1):
        content = page_contents.get(page_idx)
        if not content:
            results.append(dict(default_result))
            continue

        corrected_text = None
        summary = None
        ai_score = None

        if "CORRECTED TEXT:" in content and "SUMMARY:" in content and "SCORE:" in content:
            parts = content.split("SUMMARY:")
            corrected_part = parts[0].replace("CORRECTED TEXT:", "").strip()

            if len(parts) > 1:
                summary_and_score = parts[1].split("SCORE:")
                summary_part = summary_and_score[0].strip()

                if len(summary_and_score) > 1:
                    score_text = summary_and_score[1].strip()
                    try:
                        score_match = re.search(r'\d+\.?\d*', score_text)
                        if score_match:
                            ai_score = float(score_match.group())
                    except:
                        ai_score = None

                corrected_text = corrected_part
                summary = summary_part
        else:
            corrected_text = content.strip()
            summary = "Unable to generate summary"

        results.append({
            "corrected_text": corrected_text,
            "summary": summary,
            "ai_score": ai_score
        })

    return results
