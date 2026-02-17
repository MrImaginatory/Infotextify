# Image OCR Script - Installation & Usage Guide

## Prerequisites

### 1. Install Tesseract OCR Engine

**Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS:**

```bash
brew install tesseract
```

**Windows:**
Download installer from: https://github.com/UB-Mannheim/tesseract/wiki

### 2. Install Python Dependencies

**Basic OCR only:**

```bash
pip install pytesseract pillow
```

**With spaCy NLP support:**

```bash
pip install pytesseract pillow spacy
python -m spacy download en_core_web_sm
```

## Usage

### Basic OCR (extract text from image)

```bash
python image_ocr.py your_image.png
```

### Save extracted text to file

```bash
python image_ocr.py your_image.jpg --output result.txt
```

### OCR with NLP analysis (requires spaCy)

```bash
python image_ocr.py your_image.png --nlp
```

### OCR in different language (e.g., Spanish)

```bash
python image_ocr.py image.png --lang spa
```

### All options combined

```bash
python image_ocr.py document.jpg --lang eng --output extracted.txt --nlp
```

## Command Line Options

- `image` - Path to image file (required)
- `-o, --output` - Save extracted text to file
- `-l, --lang` - OCR language code (default: eng)
- `--nlp` - Process text with spaCy for NLP analysis
- `--spacy-model` - spaCy model to use (default: en_core_web_sm)

## Supported Image Formats

- PNG
- JPEG/JPG
- TIFF
- BMP
- GIF

## Language Codes for OCR

Common language codes:

- `eng` - English
- `spa` - Spanish
- `fra` - French
- `deu` - German
- `ita` - Italian
- `por` - Portuguese
- `rus` - Russian
- `chi_sim` - Chinese (Simplified)
- `jpn` - Japanese
- `kor` - Korean

Install additional languages:

```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr-[lang_code]

# Example for Spanish
sudo apt-get install tesseract-ocr-spa
```

## What the Script Does

1. **OCR** : Uses Tesseract to extract text from images
2. **NLP (optional)** : Uses spaCy to analyze the extracted text:

- Named Entity Recognition (people, places, organizations)
- Part-of-speech tagging
- Sentence segmentation
- Lemmatization

## Troubleshooting

**Error: "tesseract is not installed"**

- Install Tesseract OCR engine (see Prerequisites)

**Error: "spaCy model not found"**

```bash
python -m spacy download en_core_web_sm
```

**Poor OCR accuracy**

- Ensure image is clear and high resolution
- Try preprocessing: increase contrast, remove noise
- Use correct language code
