from PIL import Image, ImageEnhance

def preprocess_image(
    image: Image.Image,
    contrast: float = 1.0,
    brightness: float = 1.0,
    sharpness: float = 1.0
) -> Image.Image:
    """
    Apply image enhancements (contrast, brightness, sharpness) to a PIL Image.
    
    Args:
        image: Original PIL Image.
        contrast: Contrast factor (1.0 = original).
        brightness: Brightness factor (1.0 = original).
        sharpness: Sharpness factor (1.0 = original).
        
    Returns:
        Enhanced PIL Image.
    """
    
    # Apply Contrast
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)
        
    # Apply Brightness
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness)
        
    # Apply Sharpness
    if sharpness != 1.0:
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(sharpness)
        
    # Save the processed image
    # save_processed_image(image)
        
    return image

# def save_processed_image(image: Image.Image, output_dir: str = "processedimages"):
#     """
#     Saves the processed image to the specified directory with a unique filename.
#     """
#     import os
#     import uuid
#     from datetime import datetime
    
#     # Create directory if it doesn't exist
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
        
#     # Generate unique filename
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     unique_id = str(uuid.uuid4())[:8]
#     filename = f"processed_{timestamp}_{unique_id}.png"
#     filepath = os.path.join(output_dir, filename)
    
#     try:
#         image.save(filepath)
#         print(f"Saved processed image to: {filepath}")
#     except Exception as e:
#         print(f"Failed to save processed image: {e}")
