# OCR FastAPI Application

A FastAPI-based OCR (Optical Character Recognition) service with optional NLP processing using spaCy.

## Features

- 📸 Extract text from images using Tesseract OCR
- 🧠 Optional NLP analysis with spaCy (entities, POS tagging, sentence detection)
- 🚀 RESTful API with automatic documentation
- 🔧 Support for multiple languages
- 📊 Structured JSON responses

## Prerequisites

- Python 3.8+
- Tesseract OCR installed on your system

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

## Installation

1. **Clone or create the project directory:**

```bash
mkdir ocr-fastapi && cd ocr-fastapi
```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Download spaCy model (optional, for NLP features):**

```bash
python -m spacy download en_core_web_sm
```

5. **Create .env file (optional):**

```bash
cp .env.example .env
```

## Running the Application

### Development Mode

```bash
# From the project root directory
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## API Endpoints

### 1. Extract Text from Image

**POST** `/api/v1/ocr/extract`

**Form Data:**

- `file`: Image file (required)
- `lang`: OCR language code (default: "eng")
- `enable_nlp`: Enable NLP processing (default: false)
- `spacy_model`: spaCy model name (default: "en_core_web_sm")

**Example using curl:**

```bash
curl -X POST "http://localhost:8000/api/v1/ocr/extract" \
  -F "file=@image.png" \
  -F "lang=eng" \
  -F "enable_nlp=true"
```

**Example using Python:**

```python
import requests

url = "http://localhost:8000/api/v1/ocr/extract"
files = {"file": open("image.png", "rb")}
data = {
    "lang": "eng",
    "enable_nlp": True,
    "spacy_model": "en_core_web_sm"
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

**Response:**

```json
{
  "success": true,
  "text": "Extracted text from image...",
  "nlp_analysis": {
    "entities": [{ "text": "New York", "label": "GPE" }],
    "tokens": [{ "text": "Example", "pos": "NOUN", "lemma": "example" }],
    "sentence_count": 5
  },
  "message": "Text extracted and NLP analysis completed"
}
```

### 2. Get Supported Languages

**GET** `/api/v1/ocr/languages`

Returns list of available Tesseract OCR languages.

### 3. Get spaCy Models Info

**GET** `/api/v1/ocr/spacy-models`

Returns information about spaCy availability and suggested models.

### 4. Health Check

**GET** `/health`

Returns API health status.

## Project Structure

```
app/
├── api/
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   └── ocr.py          # OCR endpoints
│   │   ├── __init__.py
│   │   └── api.py              # API router
│   └── __init__.py
├── core/
│   ├── __init__.py
│   └── config.py               # Configuration settings
├── schemas/
│   ├── __init__.py
│   └── ocr.py                  # Pydantic models
├── services/
│   ├── __init__.py
│   ├── ocr_service.py          # OCR logic
│   └── nlp_service.py          # NLP logic
├── __init__.py
└── main.py                     # FastAPI app
```

## Configuration

Environment variables can be set in `.env` file:

```env
PROJECT_NAME=OCR API
VERSION=1.0.0
DEBUG=True
HOST=0.0.0.0
PORT=8000
DEFAULT_OCR_LANG=eng
DEFAULT_SPACY_MODEL=en_core_web_sm
MAX_FILE_SIZE=10485760  # 10 MB
```

## Supported Languages

Common language codes for OCR:

- `eng` - English
- `fra` - French
- `deu` - German
- `spa` - Spanish
- `ita` - Italian
- `por` - Portuguese
- `rus` - Russian
- `chi_sim` - Chinese Simplified
- `jpn` - Japanese
- `kor` - Korean

To see all available languages, install language packs or check:

```bash
tesseract --list-langs
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (invalid file type, file too large)
- `500` - Internal Server Error (OCR processing failed)

## Testing

Example test with pytest (create `tests/` directory):

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

## Troubleshooting

### Tesseract not found

```
Error: Tesseract not found
```

**Solution:** Install Tesseract and ensure it's in your PATH.

### spaCy model not found

```
Error: spaCy model 'en_core_web_sm' not found
```

**Solution:** Download the model:

```bash
python -m spacy download en_core_web_sm
```

### File too large error

**Solution:** Adjust `MAX_FILE_SIZE` in config or compress the image.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
