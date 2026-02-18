import { Copy, CheckCheck } from "lucide-react";
import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "./ui/dialog";
import { Button } from "./ui/button";
import { Alert, AlertDescription } from "./ui/alert";
import type { OCRResponse } from "../types/ocr";

interface ResultsModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  result: OCRResponse | null;
  onReset: () => void;
}

export function ResultsModal({
  open,
  onOpenChange,
  result,
  onReset,
}: ResultsModalProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    if (result?.text) {
      await navigator.clipboard.writeText(result.text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleClose = () => {
    onOpenChange(false);
    onReset();
    setCopied(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl max-h-[80vh] flex flex-col">
        <DialogHeader>
          <DialogTitle>OCR Results</DialogTitle>
          <DialogDescription>Extracted text from your image</DialogDescription>
        </DialogHeader>

        <div className="flex-1 overflow-auto space-y-4">
          {result?.error ? (
            <Alert variant="destructive">
              <AlertDescription>{result.error}</AlertDescription>
            </Alert>
          ) : (
            <>
              {result?.confidence !== undefined && (
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Confidence:</span>
                  <span className="font-medium">
                    {(result.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              )}

              <div className="bg-muted p-4 rounded-lg">
                <pre className="whitespace-pre-wrap text-sm font-mono">
                  {result?.text || "No text extracted"}
                </pre>
              </div>
            </>
          )}
        </div>

        <div className="flex gap-2 pt-4 border-t">
          <Button
            variant="default"
            onClick={handleCopy}
            disabled={!result?.text || !!result?.error}
            className="flex-1"
          >
            {copied ? (
              <>
                <CheckCheck className="mr-2 h-4 w-4" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="mr-2 h-4 w-4" />
                Copy Text
              </>
            )}
          </Button>
          <Button variant="outline" onClick={handleClose} className="flex-1">
            Close & Reset
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
