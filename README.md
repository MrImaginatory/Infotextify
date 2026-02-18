# InfoTextify - OCR Application

A full-stack OCR (Optical Character Recognition) application with AI-powered text analysis, correction, and summarization capabilities. The system consists of a FastAPI backend service and a React frontend application.

## 🏗️ Architecture

```
OCR/
├── OcrBackend/          # FastAPI backend service
│   ├── app/            # Application source code
│   ├── testScripts/    # Testing utilities
│   └── README.md       # Backend documentation
├── OcrFrontend/        # React frontend application
│   ├── src/            # Frontend source code
│   ├── public/         # Static assets
│   └── README.md       # Frontend documentation
└── README.md           # This file
```

## ✨ Features

### Core OCR Capabilities
- **Text Extraction**: Extract text from images using Tesseract OCR
- **PDF Support**: Multi-page PDF analysis with per-page processing
- **Multiple Languages**: Support for 100+ OCR languages

### AI-Powered Analysis
- **Text Correction**: AI-enhanced text correction (Gemini & Ollama)
- **Summarization**: Automatic content summarization
- **Quality Scoring**: AI-based readability and accuracy assessment
- **Enhancement Suggestions**: Actionable improvement recommendations

### NLP Processing
- **Named Entity Recognition**: Extract entities (people, places, organizations)
- **Part-of-Speech Tagging**: Grammatical analysis
- **Sentence Detection**: Automatic sentence boundary detection

### User Experience
- **Modern Web Interface**: Responsive React-based UI
- **Drag & Drop Upload**: Easy file upload experience
- **Dark/Light Theme**: User preference support
- **Offline Fallback**: Client-side OCR when backend is unavailable

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 18+** or **Bun** (for frontend)
- **Tesseract OCR** (system dependency)

### 1. Install Tesseract OCR

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
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### 2. Start the Backend

```bash
cd OCR/OcrBackend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r app/requirements.txt

# Download spaCy model
python -m spacy download en_core_web_trf

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY (optional)

# Start the server
python -m app.main
```

Backend will be available at `http://localhost:8001`

### 3. Start the Frontend

```bash
cd OCR/OcrFrontend

# Install dependencies
npm install  # or: bun install

# Configure environment
cp .env.example .env
# Edit .env if needed (default: http://localhost:8001/api/v1)

# Start development server
npm run dev  # or: bun run dev
```

Frontend will be available at `http://localhost:5173`

## 📚 Documentation

- **[Backend Documentation](OcrBackend/README.md)** - API endpoints, services, configuration
- **[Frontend Documentation](OcrFrontend/README.md)** - Components, UI, development

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/ocr/extract` | POST | Extract text from image/PDF |
| `/api/v1/ocr/analyze` | POST | Extract text with NLP analysis |
| `/api/v1/ocr/analyze/text` | POST | Get plain text report |
| `/api/v1/ocr/analyze/html` | POST | Get HTML formatted report |
| `/api/v1/ocr/analyze/ai` | POST | AI analysis with Gemini |
| `/api/v1/ocr/analyze/ollama` | POST | AI analysis with Ollama |
| `/api/v1/ocr/analyze/pdf-pages` | POST | Per-page PDF analysis |

Full API documentation available at: `http://localhost:8001/docs`

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Tesseract OCR** - Optical character recognition
- **spaCy** - NLP processing
- **Google Gemini** - Cloud AI services
- **Ollama** - Local LLM support
- **TextBlob** - Text correction

### Frontend
- **React 19** - UI library
- **TypeScript** - Type safety
- **Vite 8** - Build tool
- **Tailwind CSS 4** - Styling
- **shadcn/ui** - Component library
- **Tesseract.js** - Client-side OCR fallback

## 🔧 Configuration

### Backend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | `""` |
| `SPACY_MODEL` | spaCy NLP model | `en_core_web_trf` |
| `API_V1_STR` | API version prefix | `/api/v1` |

### Frontend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BACKEND_URL` | Backend API URL | `http://localhost:8001/api/v1` |

## 🌐 Supported Languages

Common OCR language codes:

| Code | Language | Code | Language |
|------|----------|------|----------|
| `eng` | English | `fra` | French |
| `deu` | German | `spa` | Spanish |
| `ita` | Italian | `por` | Portuguese |
| `rus` | Russian | `chi_sim` | Chinese (Simplified) |
| `jpn` | Japanese | `kor` | Korean |

## 🧪 Testing

### Backend Verification
```bash
cd OCR/OcrBackend
python verification_script.py
```

### Frontend Linting
```bash
cd OCR/OcrFrontend
npm run lint
```

## 🚀 Production Deployment

### Backend
```bash
# Using Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8001
```

### Frontend
```bash
# Build for production
npm run build

# Serve with nginx or similar
```

## 🔒 Security Considerations

- API keys should be stored in `.env` files (not committed to version control)
- CORS is configured to allow all origins in development - restrict in production
- Consider adding authentication for production deployments
- File size is limited to 10MB by default

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For issues and feature requests, please open an issue in the repository.
