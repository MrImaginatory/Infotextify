import { useState } from "react";
import { Navbar } from "../components/Navbar";
import { PreviewPanel } from "../components/PreviewPanel";
import { ControlsPanel } from "../components/ControlsPanel";
import { ResultsPanel } from "../components/ResultsPanel";
import { PDFResultsPanel } from "../components/PDFResultsPanel";
import { analyzeImage, analyzePdf } from "../services/ocrApi";
import { analyzeImageWithTesseract } from "../services/tesseractApi";
import { DEFAULT_OCR_SETTINGS } from "../types/ocr";
import type {
  OCRSettings,
  OCRResponse,
  OCRRequest,
  PDFAnalysisResponse,
} from "../types/ocr";
import { toast } from "sonner";
import { CheckCircle2, XCircle, Info, Upload } from "lucide-react";

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

export default function OCRPage() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [settings, setSettings] = useState<OCRSettings>(DEFAULT_OCR_SETTINGS);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<OCRResponse | null>(null);
  const [pdfResult, setPdfResult] = useState<PDFAnalysisResponse | null>(null);

  const handleFileSelect = (selectedFile: File) => {
    // Validate file size
    if (selectedFile.size > MAX_FILE_SIZE) {
      toast.error("File too large", {
        description: "Please select a file smaller than 10MB",
        icon: <XCircle className="h-5 w-5" />,
        className: "border border-destructive",
      });
      return;
    }

    // Validate file type
    const isImage = selectedFile.type.startsWith("image/");
    const isPDF = selectedFile.type === "application/pdf";

    if (!isImage && !isPDF) {
      toast.error("Invalid file type", {
        description:
          "Please select an image file (PNG, JPEG, JPG, WebP) or PDF",
        icon: <XCircle className="h-5 w-5" />,
        className: "border border-destructive",
      });
      return;
    }

    setFile(selectedFile);
    // Clear previous results when selecting a new file
    setResult(null);
    setPdfResult(null);

    // Generate preview for images only
    if (isImage) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(selectedFile);
    } else {
      // For PDFs, clear preview
      setPreview(null);
    }

    toast.success("File uploaded", {
      description: selectedFile.name,
      icon: <Upload className="h-5 w-5" />,
      className: "border border-green-500",
    });
  };

  const handleFileRemove = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setPdfResult(null);
    toast.info("File removed", {
      icon: <Info className="h-5 w-5" />,
      className: "border border-blue-500",
    });
  };

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    setResult(null);
    setPdfResult(null);

    const isPDF = file.type === "application/pdf";

    // Create request object
    const request: OCRRequest = {
      file,
      ...settings,
    };

    try {
      if (isPDF) {
        // PDF: call the per-page analysis endpoint
        const response = await analyzePdf(request);
        setPdfResult(response);

        toast.success("PDF Analysis complete", {
          description: `Analyzed ${response.total_pages} page${response.total_pages === 1 ? "" : "s"} successfully`,
          icon: <CheckCircle2 className="h-5 w-5" />,
          className: "border border-green-500",
        });
      } else {
        // Image: use the existing flow (unchanged)
        const response = await analyzeImage(request);
        setResult(response);

        toast.success("Analysis complete", {
          description: "OCR processing finished successfully",
          icon: <CheckCircle2 className="h-5 w-5" />,
          className: "border border-green-500",
        });
      }
    } catch (error) {
      console.error("OCR Analysis failed:", error);

      const errorMessage =
        error instanceof Error ? error.message : "An unknown error occurred";

      // For images only: attempt offline fallback
      if (!isPDF) {
        const isNetworkError =
          errorMessage.includes("Network error") ||
          errorMessage.includes("Service temporarily unavailable") ||
          errorMessage.includes("timed out") ||
          errorMessage.includes("Failed to fetch") ||
          !navigator.onLine;

        const isImage = file.type.startsWith("image/");

        if (isNetworkError && isImage) {
          toast.info("Switching to Offline Mode", {
            description:
              "Online service unreachable. Attempting offline OCR...",
            icon: <Info className="h-5 w-5" />,
            className: "border border-blue-500",
          });

          try {
            const offlineData = await analyzeImageWithTesseract(request);
            setResult(offlineData);

            toast.success("Offline Analysis complete", {
              description: "Text extracted using local OCR",
              icon: <CheckCircle2 className="h-5 w-5" />,
              className: "border border-green-500",
            });
            return;
          } catch (offlineError) {
            const offlineErrorMessage =
              offlineError instanceof Error
                ? offlineError.message
                : "An unknown error occurred";

            toast.error("Analysis failed", {
              description: `Offline OCR also failed: ${offlineErrorMessage}`,
              icon: <XCircle className="h-5 w-5" />,
              className: "border border-destructive",
            });
            return;
          }
        }
      }

      // Show the error
      toast.error("Analysis failed", {
        description: errorMessage,
        icon: <XCircle className="h-5 w-5" />,
        className: "border border-destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setPdfResult(null);
    setSettings(DEFAULT_OCR_SETTINGS);
  };

  const isPdf = file?.type === "application/pdf";
  // const hasResult = result !== null || pdfResult !== null;

  return (
    <div className="min-h-screen flex flex-col md:h-screen md:overflow-hidden">
      <Navbar />
      <main className="flex-1 grid grid-cols-1 lg:grid-cols-2 md:overflow-hidden">
        <PreviewPanel
          file={file}
          preview={preview}
          onFileSelect={handleFileSelect}
          onFileRemove={handleFileRemove}
        />
        {pdfResult ? (
          <PDFResultsPanel result={pdfResult} onReset={handleReset} />
        ) : result ? (
          <ResultsPanel result={result} onReset={handleReset} />
        ) : (
          <ControlsPanel
            settings={settings}
            onSettingsChange={setSettings}
            onAnalyze={handleAnalyze}
            disabled={!file}
            loading={loading}
            isPdf={isPdf}
          />
        )}
      </main>
    </div>
  );
}
