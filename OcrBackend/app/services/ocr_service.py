import pytesseract
from PIL import Image
from fastapi import HTTPException, status
from app.services import image_processing_service

def extract_text(
    image: Image.Image, 
    lang: str = 'eng',
    contrast: float = 1.0,
    brightness: float = 1.0,
    sharpness: float = 1.0
) -> str:
    """
    Extract text from an image using Tesseract OCR.
    
    Args:
        image: PIL Image object
        lang: Language code (default: 'eng')
        contrast: Contrast factor (1.0 = original)
        brightness: Brightness factor (1.0 = original)
        sharpness: Sharpness factor (1.0 = original)
    
    Returns:
        Extracted text as string
        
    Raises:
        HTTPException: If OCR processing fails
    """
    try:
        # Pre-process image if enhancements are requested
        if contrast != 1.0 or brightness != 1.0 or sharpness != 1.0:
            image = image_processing_service.preprocess_image(
                image, contrast=contrast, brightness=brightness, sharpness=sharpness
            )
            
        text = pytesseract.image_to_string(image, lang=lang)
        return text
    except Exception as e:
        # In a production app, log the actual error 'e' and return a generic message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image with Tesseract: {str(e)}"
        )
