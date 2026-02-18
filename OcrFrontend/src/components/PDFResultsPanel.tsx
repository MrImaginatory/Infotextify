import { useState } from "react";
import {
  Copy,
  CheckCheck,
  ChevronDown,
  ChevronUp,
  RotateCcw,
  FileText,
  Lightbulb,
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
import type { PDFAnalysisResponse } from "../types/ocr";

interface PDFResultsPanelProps {
  result: PDFAnalysisResponse;
  onReset: () => void;
}

function getScoreColor(score: number | null): string {
  if (score === null) return "bg-muted text-muted-foreground";
  if (score >= 70)
    return "bg-emerald-500/15 text-emerald-600 border-emerald-500/30";
  if (score >= 40) return "bg-amber-500/15 text-amber-600 border-amber-500/30";
  return "bg-red-500/15 text-red-600 border-red-500/30";
}

function getScoreLabel(score: number | null): string {
  if (score === null) return "N/A";
  return `${score}%`;
}

export function PDFResultsPanel({ result, onReset }: PDFResultsPanelProps) {
  const [copied, setCopied] = useState<string | null>(null);
  const [openPages, setOpenPages] = useState<Set<number>>(new Set([0]));
  const [showOverallSummary, setShowOverallSummary] = useState(true);
  const [showEnhancements, setShowEnhancements] = useState(true);

  const handleCopy = async (text: string, label: string) => {
    await navigator.clipboard.writeText(text);
    setCopied(label);
    setTimeout(() => setCopied(null), 2000);
  };

  const togglePage = (index: number) => {
    setOpenPages((prev) => {
      const next = new Set(prev);
      if (next.has(index)) {
        next.delete(index);
      } else {
        next.add(index);
      }
      return next;
    });
  };

  return (
    <div className="border-l p-8 flex flex-col h-screen md:h-[calc(100vh-3.5rem)] overflow-y-auto">
      <div className="space-y-6 flex-1">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold mb-2">
              PDF Analysis Results
            </h2>
            <div className="flex items-center gap-2 flex-wrap">
              <Badge variant="secondary">
                <FileText className="mr-1 h-3 w-3" />
                {result.total_pages}{" "}
                {result.total_pages === 1 ? "Page" : "Pages"}
              </Badge>
              {result.overall_score !== null && (
                <Badge className={getScoreColor(result.overall_score)}>
                  Overall Score: {getScoreLabel(result.overall_score)}
                </Badge>
              )}
            </div>
          </div>
          <Button variant="outline" size="sm" onClick={onReset}>
            <RotateCcw className="mr-2 h-4 w-4" />
            New Analysis
          </Button>
        </div>

        <Separator />

        {/* Overall Summary */}
        {result.overall_summary && (
          <>
            <Collapsible
              open={showOverallSummary}
              onOpenChange={setShowOverallSummary}
            >
              <CollapsibleTrigger asChild>
                <Button
                  variant="ghost"
                  className="w-full justify-between p-0 h-auto hover:bg-transparent"
                >
                  <span className="text-sm font-semibold text-muted-foreground">
                    Overall Summary
                  </span>
                  {showOverallSummary ? (
                    <ChevronUp className="h-4 w-4" />
                  ) : (
                    <ChevronDown className="h-4 w-4" />
                  )}
                </Button>
              </CollapsibleTrigger>
              <CollapsibleContent className="mt-3">
                <div className="bg-muted p-4 rounded-lg max-h-[200px] overflow-auto">
                  <pre className="whitespace-pre-wrap text-sm leading-relaxed">
                    {result.overall_summary}
                  </pre>
                </div>
              </CollapsibleContent>
            </Collapsible>
            <Separator />
          </>
        )}

        {/* Per-Page Results */}
        {result.potential_enhancements && (
          <>
            <Collapsible
              open={showEnhancements}
              onOpenChange={setShowEnhancements}
            >
              <CollapsibleTrigger asChild>
                <Button
                  variant="ghost"
                  className="w-full justify-between p-0 h-auto hover:bg-transparent"
                >
                  <span className="text-sm font-semibold text-muted-foreground flex items-center gap-1.5">
                    <Lightbulb className="h-4 w-4 text-amber-500" />
                    Potential Enhancements
                  </span>
                  {showEnhancements ? (
                    <ChevronUp className="h-4 w-4" />
                  ) : (
                    <ChevronDown className="h-4 w-4" />
                  )}
                </Button>
              </CollapsibleTrigger>
              <CollapsibleContent className="mt-3">
                <div className="bg-amber-500/5 border border-amber-500/20 p-4 rounded-lg max-h-[300px] overflow-auto">
                  <div className="flex items-center justify-end mb-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() =>
                        handleCopy(
                          result.potential_enhancements!,
                          "enhancements",
                        )
                      }
                    >
                      {copied === "enhancements" ? (
                        <>
                          <CheckCheck className="mr-1 h-3 w-3" />
                          Copied!
                        </>
                      ) : (
                        <>
                          <Copy className="mr-1 h-3 w-3" />
                          Copy
                        </>
                      )}
                    </Button>
                  </div>
                  <pre className="whitespace-pre-wrap text-sm leading-relaxed">
                    {result.potential_enhancements}
                  </pre>
                </div>
              </CollapsibleContent>
            </Collapsible>
            <Separator />
          </>
        )}

        {/* Per-Page Results */}
        <div className="space-y-3">
          <h3 className="text-sm font-semibold text-muted-foreground">
            Page-by-Page Analysis
          </h3>

          <div className="space-y-2">
            {result.pages.map((page, index) => (
              <Collapsible
                key={page.page_number}
                open={openPages.has(index)}
                onOpenChange={() => togglePage(index)}
              >
                <CollapsibleTrigger asChild>
                  <Button
                    variant="outline"
                    className="w-full justify-between h-auto py-3 px-4"
                  >
                    <div className="flex items-center gap-3">
                      <span className="font-medium text-sm">
                        Page {page.page_number}
                      </span>
                      <Badge
                        variant="outline"
                        className={`text-xs ${getScoreColor(page.ai_score)}`}
                      >
                        Score: {getScoreLabel(page.ai_score)}
                      </Badge>
                    </div>
                    {openPages.has(index) ? (
                      <ChevronUp className="h-4 w-4 shrink-0" />
                    ) : (
                      <ChevronDown className="h-4 w-4 shrink-0" />
                    )}
                  </Button>
                </CollapsibleTrigger>

                <CollapsibleContent className="mt-2 space-y-4 pl-2 pr-1 pb-2">
                  {/* Page Summary */}
                  {page.summary && (
                    <div className="space-y-1">
                      <p className="text-xs font-medium text-muted-foreground">
                        Summary
                      </p>
                      <p className="text-sm leading-relaxed bg-muted/50 p-3 rounded-md">
                        {page.summary}
                      </p>
                    </div>
                  )}

                  {/* Page Text Tabs */}
                  <Tabs defaultValue="ai-corrected" className="w-full">
                    <TabsList className="grid w-full grid-cols-2">
                      <TabsTrigger value="ai-corrected">
                        AI Corrected
                      </TabsTrigger>
                      <TabsTrigger value="original">Original</TabsTrigger>
                    </TabsList>

                    <TabsContent value="ai-corrected" className="space-y-2">
                      <div className="flex items-center justify-between">
                        <p className="text-xs text-muted-foreground">
                          AI-enhanced corrected text
                        </p>
                        {page.ai_corrected_text && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() =>
                              handleCopy(
                                page.ai_corrected_text!,
                                `ai-corrected-${page.page_number}`,
                              )
                            }
                          >
                            {copied === `ai-corrected-${page.page_number}` ? (
                              <>
                                <CheckCheck className="mr-1 h-3 w-3" />
                                Copied!
                              </>
                            ) : (
                              <>
                                <Copy className="mr-1 h-3 w-3" />
                                Copy
                              </>
                            )}
                          </Button>
                        )}
                      </div>
                      <div className="bg-muted p-3 rounded-lg max-h-[200px] overflow-auto">
                        <pre className="whitespace-pre-wrap text-sm font-mono">
                          {page.ai_corrected_text ||
                            "No corrected text available"}
                        </pre>
                      </div>
                    </TabsContent>

                    <TabsContent value="original" className="space-y-2">
                      <div className="flex items-center justify-between">
                        <p className="text-xs text-muted-foreground">
                          Raw OCR output
                        </p>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() =>
                            handleCopy(
                              page.text,
                              `original-${page.page_number}`,
                            )
                          }
                        >
                          {copied === `original-${page.page_number}` ? (
                            <>
                              <CheckCheck className="mr-1 h-3 w-3" />
                              Copied!
                            </>
                          ) : (
                            <>
                              <Copy className="mr-1 h-3 w-3" />
                              Copy
                            </>
                          )}
                        </Button>
                      </div>
                      <div className="bg-muted p-3 rounded-lg max-h-[200px] overflow-auto">
                        <pre className="whitespace-pre-wrap text-sm font-mono">
                          {page.text}
                        </pre>
                      </div>
                    </TabsContent>
                  </Tabs>
                </CollapsibleContent>
              </Collapsible>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
