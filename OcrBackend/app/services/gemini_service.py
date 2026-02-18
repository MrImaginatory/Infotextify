"""
Gemini AI Service for text correction and summarization.
"""
from google import genai
from google.genai import types
from typing import Optional, Dict
from app.core.config import settings

# Configure Gemini API client
client = None
if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

def get_ai_correction_and_summary(text: str) -> Dict[str, Optional[str]]:
    """
    Use Gemini AI to correct OCR text and generate a summary.
    
    Args:
        text: The extracted OCR text to process
        
    Returns:
        Dictionary with 'corrected_text' and 'summary' keys
    """
    try:
        # Check if client is configured
        if not client:
            return {
                "corrected_text": None,
                "summary": None
            }
        
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
        
        # Generate response using new API
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=prompt
        )
        
        # Parse the response
        response_text = response.text
        
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
                        import re
                        score_match = re.search(r'\d+\.?\d*', score_text)
                        if score_match:
                            ai_score = float(score_match.group())
                    except:
                        ai_score = None
                
                corrected_text = corrected_part
                summary = summary_part
        else:
            # Fallback parsing
            corrected_text = response_text
            summary = "Unable to generate summary"
            ai_score = None
        
        return {
            "corrected_text": corrected_text,
            "summary": summary,
            "ai_score": ai_score
        }
        
    except Exception as e:
        print(f"Error calling Gemini API: {str(e)}")
        return {
            "corrected_text": None,
            "summary": None,
            "ai_score": None
        }
