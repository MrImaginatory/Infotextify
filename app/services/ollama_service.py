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
