"""
Image processing module for OCR text extraction.
"""
from typing import Optional

import pytesseract
from PIL import Image, ImageFilter

import config


def process_image(image_path: str) -> str:
    """
    Process image and extract text using OCR.
    
    Args:
        image_path: Path to image file
        
    Returns:
        Extracted text from image
        
    Raises:
        FileNotFoundError: If image file not found
        Exception: If OCR processing fails
    """
    logger = config.get_logger()
    
    try:
        image = Image.open(image_path)
        
        # Apply sharpening filter for better OCR accuracy
        image = image.filter(ImageFilter.SHARPEN)
        
        # Extract text using Tesseract
        text = pytesseract.image_to_string(image)
        
        logger.info(f"Successfully processed image: {image_path}")
        return text
        
    except FileNotFoundError as e:
        logger.error(f"Image file not found: {image_path}")
        raise
    except Exception as e:
        logger.error(f"Error processing image {image_path}: {repr(e)}")
        raise


def get_image(image_path: str) -> Image.Image:
    """
    Open and return PIL Image object.
    
    Args:
        image_path: Path to image file
        
    Returns:
        PIL Image object
        
    Raises:
        FileNotFoundError: If image file not found
    """
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        config.get_logger().error(f"Image not found: {image_path}")
        raise


if __name__ == "__main__":
    config.setup_logging()
    try:
        # Example: process image from img directory
        text = process_image(f"{config.IMG_DIR}sample.png")
        print(f"Extracted text:\n{text}")
    except Exception as e:
        print(f"Error: {e}")
