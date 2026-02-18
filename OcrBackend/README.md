# OcrBackend - OCR Service API

A FastAPI-based OCR (Optical Character Recognition) backend service with AI-powered text analysis, correction, and summarization capabilities.

## 🚀 Features

- **Text Extraction**: Extract text from images and PDFs using Tesseract OCR
- **NLP Analysis**: Process text with spaCy for entity recognition, POS tagging, and sentence detection
- **AI Integration**: 
  - Gemini AI for advanced text correction and summarization
  - Ollama (local LLM) support for privacy-focused AI processing
- **Image Enhancement**: Adjustable contrast, brightness, and sharpness preprocessing
- **PDF Support**: Multi-page PDF analysis with per-page summaries
- **Auto-correction**: Built-in text correction using TextBlob
- **Multiple Output Formats**: JSON, plain text, and HTML reports

## 📋 Prerequisites

- Python 3.8+
- Tesseract OCR installed on your system
- (Optional) Ollama for local AI processing
- (Optional) Gemini API key for cloud AI features

### Installing Tesseract

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

### Installing Ollama (Optional)

```bash
# Follow instructions at https://ollama.ai
# Pull the required model
ollama pull glm-5:cloud
```

## 🔧 Installation

1. **Navigate to the backend directory:**
```bash
cd OCR/OcrBackend
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r app/requirements.txt
```

4. **Download spaCy model:**
```bash
python -m spacy download en_core_web_trf
```

5. **Configure environment variables:**
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your Gemini API key (optional)
# GEMINI_API_KEY=your_api_key_here
```

## 🏃 Running the Application

### Development Mode
```bash
# From the OcrBackend directory
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 4
```

### Using Gunicorn
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8001
```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc

## 🔌 API Endpoints

### 1. Extract Text
**POST** `/api/v1/ocr/extract`

Extract text from an image or PDF file.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file` | File | required | Image or PDF file |
| `lang` | string | "eng" | OCR language code |
| `autocorrect` | boolean | false | Enable text correction |
| `contrast` | float | 1.0 | Contrast enhancement factor |
| `brightness` | float | 1.0 | Brightness enhancement factor |
| `sharpness` | float | 1.0 | Sharpness enhancement factor |

### 2. Analyze Text
**POST** `/api/v1/ocr/analyze`

Extract text and perform NLP analysis (entities, tokens, sentences).

### 3. Analyze with Text Report
**POST** `/api/v1/ocr/analyze/text`

Returns a formatted plain text report.

### 4. Analyze with HTML Report
**POST** `/api/v1/ocr/analyze/html`

Returns an HTML formatted report.

### 5. AI Analysis (Gemini)
**POST** `/api/v1/ocr/analyze/ai`

Extract text, perform NLP analysis, and use Gemini AI for correction and summarization.

### 6. AI Analysis (Ollama)
**POST** `/api/v1/ocr/analyze/ollama`

Extract text, perform NLP analysis, and use local Ollama for correction and summarization.

### 7. PDF Per-Page Analysis
**POST** `/api/v1/ocr/analyze/pdf-pages`

Analyze PDF documents with per-page summaries and quality scores.

## 📁 Project Structure

```
OcrBackend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── ocr.py          # OCR API endpoints
│   │       └── api.py              # API router configuration
│   ├── core/
│   │   └── config.py               # Application settings
│   ├── schemas/
│   │   └── ocr.py                  # Pydantic models
│   ├── services/
│   │   ├── ocr_service.py          # Tesseract OCR logic
│   │   ├── nlp_service.py          # spaCy NLP processing
│   │   ├── gemini_service.py       # Gemini AI integration
│   │   ├── ollama_service.py       # Ollama AI integration
│   │   ├── correction_service.py   # TextBlob correction
│   │   ├── image_processing_service.py  # Image preprocessing
│   │   └── report_service.py       # Report generation
│   ├── templates/
│   │   └── report.html             # HTML report template
│   ├── main.py                     # FastAPI application
│   └── requirements.txt            # Python dependencies
├── testScripts/                    # Test utilities
├── verification_script.py          # API verification script
├── .env                            # Environment variables
├── .gitignore
└── gunicorn.ctl                    # Gunicorn configuration
```

## ⚙️ Configuration

Environment variables (in `.env` file):

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | "" | Google Gemini API key |
| `SPACY_MODEL` | "en_core_web_trf" | spaCy model for NLP |
| `API_V1_STR` | "/api/v1" | API version prefix |
| `PROJECT_NAME` | "OCR Service" | Project name |

## 🌐 Supported Languages

Common OCR language codes:

| Code | Language |
|------|----------|
| `eng` | English |
| `fra` | French |
| `deu` | German |
| `spa` | Spanish |
| `ita` | Italian |
| `por` | Portuguese |
| `rus` | Russian |
| `chi_sim` | Chinese Simplified |
| `jpn` | Japanese |
| `kor` | Korean |

Check available languages:
```bash
tesseract --list-langs
```

## 🧪 Testing

Run the verification script:
```bash
# Ensure the server is running first
python verification_script.py
```

## 🔒 Security Notes

- The API has CORS enabled for all origins (`allow_origins=["*"]`)
- API keys should be stored in `.env` file (not committed to version control)
- Consider adding authentication for production deployments

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
