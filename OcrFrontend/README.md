# OcrFrontend - InfoTextify OCR Web Application

A modern React-based frontend for the OCR (Optical Character Recognition) service. This application provides a user-friendly interface for extracting text from images and PDFs with AI-powered analysis capabilities.

## 🚀 Features

- **File Upload**: Drag & drop or click to upload images and PDFs
- **Image Preview**: Visual preview of uploaded images before processing
- **OCR Processing**: Extract text from images and PDF documents
- **AI Analysis**: View AI-corrected text, summaries, and quality scores
- **Offline Mode**: Automatic fallback to Tesseract.js when backend is unavailable
- **NLP Insights**: View named entities, tokens, and sentence analysis
- **PDF Support**: Multi-page PDF analysis with per-page summaries
- **Copy to Clipboard**: Easy copying of extracted text
- **Dark/Light Theme**: Theme toggle for user preference
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Tech Stack

- **React 19** - UI library
- **TypeScript** - Type safety
- **Vite 8** - Build tool and dev server
- **Tailwind CSS 4** - Styling
- **shadcn/ui** - UI component library (Radix UI based)
- **Tesseract.js** - Client-side OCR fallback
- **Sonner** - Toast notifications
- **Lucide React** - Icon library

## 📋 Prerequisites

- Node.js 18+ or Bun
- npm, yarn, or bun package manager

## 🔧 Installation

1. **Navigate to the frontend directory:**
```bash
cd OCR/OcrFrontend
```

2. **Install dependencies:**
```bash
# Using npm
npm install

# Using bun
bun install
```

3. **Configure environment variables:**
```bash
# Create .env file
cp .env.example .env

# Edit .env to set the backend URL
# VITE_API_BACKEND_URL=http://localhost:8001/api/v1
```

## 🏃 Running the Application

### Development Mode
```bash
# Using npm
npm run dev

# Using bun
bun run dev
```

The application will be available at `http://localhost:5173`

### Production Build
```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Linting
```bash
npm run lint
```

## 📁 Project Structure

```
OcrFrontend/
├── public/                     # Static assets
│   └── logo.svg               # Application logo
├── src/
│   ├── components/            # React components
│   │   ├── ui/               # shadcn/ui components
│   │   │   ├── alert.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── collapsible.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── label.tsx
│   │   │   ├── select.tsx
│   │   │   ├── separator.tsx
│   │   │   ├── slider.tsx
│   │   │   ├── sonner.tsx
│   │   │   ├── switch.tsx
│   │   │   └── tabs.tsx
│   │   ├── AdvancedSettings.tsx  # OCR configuration panel
│   │   ├── ControlsPanel.tsx     # Main controls container
│   │   ├── Navbar.tsx            # Navigation bar
│   │   ├── PDFResultsPanel.tsx   # PDF results display
│   │   ├── PreviewPanel.tsx      # File upload/preview
│   │   ├── ResultsModal.tsx      # Results modal dialog
│   │   ├── ResultsPanel.tsx      # Image results display
│   │   └── ThemeToggle.tsx       # Dark/light mode toggle
│   ├── lib/
│   │   └── utils.ts             # Utility functions
│   ├── pages/
│   │   └── OCRPage.tsx          # Main OCR page
│   ├── services/
│   │   ├── ocrApi.ts            # Backend API client
│   │   └── tesseractApi.ts      # Offline OCR fallback
│   ├── types/
│   │   └── ocr.ts               # TypeScript interfaces
│   ├── App.tsx                  # Root component
│   ├── index.css                # Global styles
│   └── main.tsx                 # Application entry point
├── components.json              # shadcn/ui configuration
├── eslint.config.js            # ESLint configuration
├── index.html                  # HTML template
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript configuration
├── tsconfig.app.json           # App-specific TS config
├── tsconfig.node.json          # Node-specific TS config
└── vite.config.ts              # Vite configuration
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BACKEND_URL` | Backend API URL | `http://localhost:8001/api/v1` |

### OCR Settings

The application allows users to configure:

| Setting | Description | Default |
|---------|-------------|---------|
| `lang` | OCR language code | `eng` |
| `autocorrect` | Enable text correction | `true` |
| `contrast` | Image contrast enhancement | `1.8` |
| `brightness` | Image brightness enhancement | `1.8` |
| `sharpness` | Image sharpness enhancement | `1.8` |

## 🔌 API Integration

The frontend connects to the following backend endpoints:

- **POST** `/ocr/analyze/ollama` - Image analysis with AI
- **POST** `/ocr/analyze/pdf-pages` - PDF per-page analysis

### Offline Fallback

When the backend is unavailable, the application automatically falls back to Tesseract.js for client-side OCR processing. This provides basic text extraction without AI features.

## 🎨 UI Components

The application uses shadcn/ui components with the "new-york" style variant:

- **Button** - Primary actions
- **Card** - Content containers
- **Tabs** - Text version switching
- **Badge** - Score and status display
- **Collapsible** - NLP analysis section
- **Slider** - Image enhancement controls
- **Switch** - Toggle settings
- **Select** - Language selection
- **Sonner** - Toast notifications

## 📱 Responsive Design

The application is fully responsive:

- **Desktop**: Side-by-side layout with preview and controls
- **Mobile**: Stacked layout with full-width panels

## 🔒 File Constraints

- **Maximum file size**: 10MB
- **Supported image formats**: PNG, JPEG, JPG, WebP
- **Supported document formats**: PDF

## 🧪 Development

### Available Scripts

| Script | Description |
|--------|-------------|
| `dev` | Start development server |
| `build` | Build for production |
| `preview` | Preview production build |
| `lint` | Run ESLint |

### Adding New UI Components

```bash
# Using shadcn CLI
npx shadcn@latest add [component-name]
```

## 🚀 Deployment

The application is configured with a base path of `/tools/infotextify/` for deployment. Modify [`vite.config.ts`](vite.config.ts:8) for different deployment paths.

```typescript
export default defineConfig({
  base: '/tools/infotextify/',
  // ...
})
```

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
