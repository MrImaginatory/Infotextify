#!/usr/bin/env python3
"""
Simple Image OCR Script
Uses pytesseract for OCR and optionally spaCy for NLP processing
"""

import argparse
import sys
from pathlib import Path

try:
    import pytesseract
    from PIL import Image
except ImportError:
    print("Error: Required libraries not installed.")
    print("Install with: pip install pytesseract pillow")
    sys.exit(1)

# Optional spaCy import
SPACY_AVAILABLE = False
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    pass


def extract_text_from_image(image_path, lang='eng'):
    """
    Extract text from an image using Tesseract OCR
    
    Args:
        image_path: Path to the image file
        lang: Language code (default: 'eng' for English)
    
    Returns:
        Extracted text as string
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=lang)
        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        sys.exit(1)


def process_with_spacy(text, model='en_core_web_sm'):
    """
    Process extracted text with spaCy for NLP analysis
    
    Args:
        text: Text to process
        model: spaCy model name
    
    Returns:
        spaCy Doc object
    """
    if not SPACY_AVAILABLE:
        print("Warning: spaCy not installed. Skipping NLP processing.")
        return None
    
    try:
        nlp = spacy.load(model)
        doc = nlp(text)
        return doc
    except OSError:
        print(f"Error: spaCy model '{model}' not found.")
        print(f"Install with: python -m spacy download {model}")
        return None
    except Exception as e:
        print(f"Error in spaCy processing: {e}")
        return None


def display_spacy_analysis(doc):
    """Display basic spaCy NLP analysis"""
    if doc is None:
        return
    
    print("\n" + "="*50)
    print("SPACY NLP ANALYSIS")
    print("="*50)
    
    # Entities
    if doc.ents:
        print("\nNamed Entities:")
        for ent in doc.ents:
            print(f"  - {ent.text}: {ent.label_}")
    
    # Part of Speech
    print("\nTokens (first 20):")
    for token in list(doc)[:20]:
        print(f"  {token.text:15} | POS: {token.pos_:10} | Lemma: {token.lemma_}")
    
    # Sentences
    sentences = list(doc.sents)
    print(f"\nNumber of sentences: {len(sentences)}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract text from images using OCR',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python image_ocr.py image.png
  python image_ocr.py image.jpg --nlp
  python image_ocr.py image.png --lang spa --output result.txt
        """
    )
    
    parser.add_argument('image', help='Path to image file')
    parser.add_argument('-o', '--output', help='Output file for extracted text')
    parser.add_argument('-l', '--lang', default='eng', 
                       help='OCR language (default: eng)')
    parser.add_argument('--nlp', action='store_true',
                       help='Process text with spaCy NLP')
    parser.add_argument('--spacy-model', default='en_core_web_sm',
                       help='spaCy model to use (default: en_core_web_sm)')
    
    args = parser.parse_args()
    
    # Check if image exists
    if not Path(args.image).exists():
        print(f"Error: Image file '{args.image}' not found.")
        sys.exit(1)
    
    # Extract text
    print(f"Processing image: {args.image}")
    text = extract_text_from_image(args.image, args.lang)
    
    # Display extracted text
    print("\n" + "="*50)
    print("EXTRACTED TEXT")
    print("="*50)
    print(text)
    
    # Save to file if specified
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"\nText saved to: {args.output}")
    
    # Process with spaCy if requested
    if args.nlp:
        if text.strip():
            doc = process_with_spacy(text, args.spacy_model)
            display_spacy_analysis(doc)
        else:
            print("\nNo text extracted for NLP processing.")


if __name__ == '__main__':
    main()