import { Upload, X } from "lucide-react";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";

interface PreviewPanelProps {
  file: File | null;
  preview: string | null;
  onFileSelect: (file: File) => void;
  onFileRemove: () => void;
}

export function PreviewPanel({
  file,
  preview,
  onFileSelect,
  onFileRemove,
}: PreviewPanelProps) {
  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();

    const droppedFile = e.dataTransfer.files[0];
    if (
      droppedFile &&
      (droppedFile.type.startsWith("image/") ||
        droppedFile.type === "application/pdf")
    ) {
      onFileSelect(droppedFile);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      onFileSelect(selectedFile);
    }
  };

  return (
    <div
      className="flex items-center justify-center bg-muted/30 p-8 "
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      {!file ? (
        <Card className="border-dashed border-2 hover:border-primary/50 transition-colors cursor-pointer max-w-md w-full relative">
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <Upload className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">Upload File</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Drag & drop or click to select a file
            </p>
            <p className="text-xs text-muted-foreground">
              Supports: Images (PNG, JPEG, JPG, WebP) & PDF (Max 10MB)
            </p>
            <input
              type="file"
              accept="image/png,image/jpeg,image/jpg,image/webp,application/pdf"
              onChange={handleFileInput}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
            />
          </CardContent>
        </Card>
      ) : (
        <Card className="max-w-2xl w-full animate-fade-in">
          <CardContent className="p-6">
            <div className="relative">
              <Button
                variant="ghost"
                size="icon"
                className="absolute -top-2 -right-2 h-8 w-8 rounded-full bg-background shadow-md hover:bg-destructive hover:text-destructive-foreground z-10"
                onClick={onFileRemove}
              >
                <X className="h-4 w-4" />
              </Button>
              {preview ? (
                <img
                  src={preview}
                  alt="Preview"
                  className="w-full h-auto rounded-lg max-h-[60vh] object-contain"
                />
              ) : (
                <div className="flex flex-col items-center justify-center p-12 bg-muted/30 rounded-lg">
                  <Upload className="h-16 w-16 text-muted-foreground mb-4" />
                  <p className="text-sm font-medium text-muted-foreground">
                    PDF File
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Preview not available
                  </p>
                </div>
              )}
              <div className="mt-4 flex items-center justify-between">
                <p className="text-sm font-medium truncate">{file.name}</p>
                <p className="text-xs text-muted-foreground ml-2">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
