import { useState } from "react";
import {
  Copy,
  CheckCheck,
  ChevronDown,
  ChevronUp,
  RotateCcw,
} from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { Button } from "./ui/button";
import { Separator } from "./ui/separator";
import { Badge } from "./ui/badge";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "./ui/collapsible";
import type { OCRResponse } from "../types/ocr";

interface ResultsPanelProps {
  result: OCRResponse;
  onReset: () => void;
}

export function ResultsPanel({ result, onReset }: ResultsPanelProps) {
  const [copied, setCopied] = useState<string | null>(null);
  const [showNLP, setShowNLP] = useState(false);

  const handleCopy = async (text: string, label: string) => {
    await navigator.clipboard.writeText(text);
    setCopied(label);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <div className="border-l p-8 flex flex-col h-screen md:h-[calc(100vh-3.5rem)] overflow-y-auto">
      <div className="space-y-6 flex-1">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold mb-2">OCR Results</h2>
            <div className="flex items-center gap-2">
              <Badge variant="secondary">AI Score: {result.ai_score}%</Badge>
            </div>
          </div>
          <Button variant="outline" size="sm" onClick={onReset}>
            <RotateCcw className="mr-2 h-4 w-4" />
            New Analysis
          </Button>
        </div>

        <Separator />

        {/* Summary Section */}
        <div className="space-y-2">
          <h3 className="text-sm font-semibold text-muted-foreground">
            Summary
          </h3>
          <p className="text-sm leading-relaxed">{result.summary}</p>
        </div>

        <Separator />

        {/* Tabs for different text versions */}
        <Tabs defaultValue="ai-corrected" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="ai-corrected">AI Corrected</TabsTrigger>
            <TabsTrigger value="corrected">Corrected</TabsTrigger>
            <TabsTrigger value="original">Original</TabsTrigger>
          </TabsList>

          <TabsContent value="ai-corrected" className="space-y-3">
            <div className="flex items-center justify-between">
              <p className="text-xs text-muted-foreground">
                AI-enhanced corrected text
              </p>
              <Button
                variant="ghost"
                size="sm"
                onClick={() =>
                  handleCopy(result.ai_corrected_text, "ai-corrected")
                }
              >
                {copied === "ai-corrected" ? (
                  <>
                    <CheckCheck className="mr-2 h-3 w-3" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="mr-2 h-3 w-3" />
                    Copy
                  </>
                )}
              </Button>
            </div>
            <div className="bg-muted p-4 rounded-lg max-h-[300px] overflow-auto">
              <pre className="whitespace-pre-wrap text-sm font-mono">
                {result.ai_corrected_text}
              </pre>
            </div>
          </TabsContent>

          <TabsContent value="corrected" className="space-y-3">
            <div className="flex items-center justify-between">
              <p className="text-xs text-muted-foreground">
                Auto-corrected text
              </p>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleCopy(result.corrected_text, "corrected")}
              >
                {copied === "corrected" ? (
                  <>
                    <CheckCheck className="mr-2 h-3 w-3" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="mr-2 h-3 w-3" />
                    Copy
                  </>
                )}
              </Button>
            </div>
            <div className="bg-muted p-4 rounded-lg max-h-[300px] overflow-auto">
              <pre className="whitespace-pre-wrap text-sm font-mono">
                {result.corrected_text}
              </pre>
            </div>
          </TabsContent>

          <TabsContent value="original" className="space-y-3">
            <div className="flex items-center justify-between">
              <p className="text-xs text-muted-foreground">Raw OCR output</p>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleCopy(result.text, "original")}
              >
                {copied === "original" ? (
                  <>
                    <CheckCheck className="mr-2 h-3 w-3" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="mr-2 h-3 w-3" />
                    Copy
                  </>
                )}
              </Button>
            </div>
            <div className="bg-muted p-4 rounded-lg max-h-[300px] overflow-auto">
              <pre className="whitespace-pre-wrap text-sm font-mono">
                {result.text}
              </pre>
            </div>
          </TabsContent>
        </Tabs>

        <Separator />

        {/* NLP Analysis Toggle */}
        <Collapsible open={showNLP} onOpenChange={setShowNLP}>
          <CollapsibleTrigger asChild>
            <Button
              variant="ghost"
              className="w-full justify-between p-0 h-auto hover:bg-transparent"
            >
              <span className="text-sm font-medium">NLP Analysis</span>
              {showNLP ? (
                <ChevronUp className="h-4 w-4" />
              ) : (
                <ChevronDown className="h-4 w-4" />
              )}
            </Button>
          </CollapsibleTrigger>
          <CollapsibleContent className="space-y-4 mt-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Number of Sentences</span>
                <Badge variant="outline">
                  {result.nlp_analysis.num_sentences}
                </Badge>
              </div>
            </div>

            <Separator />

            <div className="space-y-2">
              <h4 className="text-sm font-semibold">Tokens</h4>
              <div className="bg-muted p-4 rounded-lg max-h-[200px] overflow-auto">
                <div className="space-y-2">
                  {result.nlp_analysis.tokens.map((token, idx) => (
                    <div
                      key={idx}
                      className="flex items-center gap-3 text-xs border-b border-border/50 pb-2 last:border-0"
                    >
                      <span className="font-mono font-medium min-w-[100px]">
                        {token.text === "\n"
                          ? "\\n"
                          : token.text === "\n\n"
                            ? "\\n\\n"
                            : token.text === "\n\f"
                              ? "\\n\\f"
                              : token.text}
                      </span>
                      <Badge variant="secondary" className="text-xs">
                        {token.pos}
                      </Badge>
                      <span className="text-muted-foreground">
                        → {token.lemma}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {result.nlp_analysis.entities.length > 0 && (
              <>
                <Separator />
                <div className="space-y-2">
                  <h4 className="text-sm font-semibold">Entities</h4>
                  <div className="bg-muted p-4 rounded-lg">
                    <pre className="text-xs">
                      {JSON.stringify(result.nlp_analysis.entities, null, 2)}
                    </pre>
                  </div>
                </div>
              </>
            )}
          </CollapsibleContent>
        </Collapsible>
      </div>
    </div>
  );
}
