import { Sparkles, Loader2 } from "lucide-react";
import { Button } from "./ui/button";
import { Separator } from "./ui/separator";
import { AdvancedSettings } from "./AdvancedSettings";
import type { OCRSettings } from "../types/ocr";

interface ControlsPanelProps {
  settings: OCRSettings;
  onSettingsChange: (settings: OCRSettings) => void;
  onAnalyze: () => void;
  disabled: boolean;
  loading: boolean;
  isPdf?: boolean;
}

export function ControlsPanel({
  settings,
  onSettingsChange,
  onAnalyze,
  disabled,
  loading,
  isPdf,
}: ControlsPanelProps) {
  return (
    <div className="border-l p-8 flex flex-col justify-between overflow-y-auto">
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-semibold mb-2">OCR Options</h2>
          <p className="text-sm text-muted-foreground">
            Configure settings for optimal text extraction
          </p>
        </div>

        <Separator />

        <AdvancedSettings
          settings={settings}
          onSettingsChange={onSettingsChange}
        />
      </div>

      <div className="sticky bottom-0 bg-background pt-4 pb-2 mt-auto">
        <Button
          size="lg"
          className="w-full h-12 text-base"
          onClick={onAnalyze}
          disabled={disabled || loading}
        >
          {loading ? (
            <>
              <Loader2 className="mr-2 h-5 w-5 animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              <Sparkles className="mr-2 h-5 w-5" />
              {isPdf ? "Analyze PDF" : "Analyze Image"}
            </>
          )}
        </Button>
      </div>
    </div>
  );
}
