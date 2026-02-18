import { useState } from "react";
import { Settings } from "lucide-react";
import { Label } from "./ui/label";
import { Switch } from "./ui/switch";
import { Slider } from "./ui/slider";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./ui/dialog";
import { Button } from "./ui/button";
import { Separator } from "./ui/separator";
import type { OCRSettings } from "../types/ocr";

interface AdvancedSettingsProps {
  settings: OCRSettings;
  onSettingsChange: (settings: OCRSettings) => void;
}

export function AdvancedSettings({
  settings,
  onSettingsChange,
}: AdvancedSettingsProps) {
  const [open, setOpen] = useState(false);

  const updateSetting = <K extends keyof OCRSettings>(
    key: K,
    value: OCRSettings[K],
  ) => {
    onSettingsChange({ ...settings, [key]: value });
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <div className="flex items-center justify-between ">
        <span className="text-sm font-medium">Advanced Settings</span>
        <DialogTrigger asChild>
          <Button variant="ghost" size="icon" className="h-8 w-8">
            <Settings className="h-4 w-4" />
          </Button>
        </DialogTrigger>
      </div>

      <DialogContent className="max-w-md max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Advanced Settings</DialogTitle>
          <DialogDescription>
            Configure advanced OCR options for optimal text extraction
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          <div className="space-y-2">
            <Label htmlFor="language">Language</Label>
            <Select
              value={settings.lang}
              onValueChange={(value) => updateSetting("lang", value)}
            >
              <SelectTrigger id="language" className="w-full">
                <SelectValue placeholder="Select language" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="eng">English</SelectItem>
                <SelectItem value="spa">Spanish</SelectItem>
                <SelectItem value="fra">French</SelectItem>
                <SelectItem value="deu">German</SelectItem>
                <SelectItem value="ita">Italian</SelectItem>
                <SelectItem value="por">Portuguese</SelectItem>
                <SelectItem value="rus">Russian</SelectItem>
                <SelectItem value="jpn">Japanese</SelectItem>
                <SelectItem value="chi_sim">Chinese (Simplified)</SelectItem>
                <SelectItem value="chi_tra">Chinese (Traditional)</SelectItem>
                <SelectItem value="ara">Arabic</SelectItem>
                <SelectItem value="hin">Hindi</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Separator />

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="autocorrect">Autocorrect</Label>
              <Switch
                id="autocorrect"
                checked={settings.autocorrect}
                onCheckedChange={(checked) =>
                  updateSetting("autocorrect", checked)
                }
              />
            </div>
            <p className="text-xs text-muted-foreground">
              Automatically correct spelling errors in extracted text
            </p>
          </div>

          <Separator />

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="contrast">Contrast</Label>
              <span className="text-sm text-muted-foreground">
                {settings.contrast.toFixed(1)}
              </span>
            </div>
            <Slider
              id="contrast"
              min={0}
              max={2}
              step={0.1}
              value={[settings.contrast]}
              onValueChange={([value]) => updateSetting("contrast", value)}
            />
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="brightness">Brightness</Label>
              <span className="text-sm text-muted-foreground">
                {settings.brightness.toFixed(1)}
              </span>
            </div>
            <Slider
              id="brightness"
              min={0}
              max={2}
              step={0.1}
              value={[settings.brightness]}
              onValueChange={([value]) => updateSetting("brightness", value)}
            />
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="sharpness">Sharpness</Label>
              <span className="text-sm text-muted-foreground">
                {settings.sharpness.toFixed(1)}
              </span>
            </div>
            <Slider
              id="sharpness"
              min={0}
              max={2}
              step={0.1}
              value={[settings.sharpness]}
              onValueChange={([value]) => updateSetting("sharpness", value)}
            />
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
