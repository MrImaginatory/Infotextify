export interface OCRRequest {
    file: File;
    lang: string;
    autocorrect: boolean;
    contrast: number;
    brightness: number;
    sharpness: number;
}

export interface NLPToken {
    text: string;
    pos: string;
    lemma: string;
}

export interface NLPAnalysis {
    entities: unknown[];
    tokens: NLPToken[];
    num_sentences: number;
}

export interface OCRResponse {
    text: string;
    corrected_text: string;
    nlp_analysis: NLPAnalysis;
    ai_corrected_text: string;
    summary: string;
    ai_score: number;
    error?: string;
    confidence?: number;
}

export interface PDFPageResult {
    page_number: number;
    text: string;
    summary: string | null;
    ai_score: number | null;
    ai_corrected_text: string | null;
}

export interface PDFAnalysisResponse {
    total_pages: number;
    pages: PDFPageResult[];
    overall_summary: string | null;
    overall_score: number | null;
    potential_enhancements: string | null;
}

export interface OCRSettings {
    lang: string;
    autocorrect: boolean;
    contrast: number;
    brightness: number;
    sharpness: number;
}

export const DEFAULT_OCR_SETTINGS: OCRSettings = {
    lang: 'eng',
    autocorrect: true,
    contrast: 1.8,
    brightness: 1.8,
    sharpness: 1.8,
};
