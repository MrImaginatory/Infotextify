import { createWorker } from 'tesseract.js';
import type { OCRRequest, OCRResponse } from '../types/ocr';

export async function analyzeImageWithTesseract(request: OCRRequest): Promise<OCRResponse> {
    const worker = await createWorker(request.lang);

    // Tesseract doesn't support file objects directly in all environments, 
    // but browser version usually handles File/Blob/URL.
    // Ideally convert File to URL for safety
    const imageUrl = URL.createObjectURL(request.file);

    try {
        const { data: { text } } = await worker.recognize(imageUrl);
        await worker.terminate();
        URL.revokeObjectURL(imageUrl);

        // Construct a fallback response compatible with OCRResponse
        // Since Tesseract doesn't provide NLP or AI correction, we'll fill with defaults
        return {
            text: text,
            corrected_text: text, // No auto-correction in raw Tesseract
            ai_corrected_text: text, // No AI correction
            summary: "Offline OCR fallback (Tesseract.js). AI analysis not available.",
            ai_score: 50, // Neutral score for offline mode
            nlp_analysis: {
                entities: [],
                tokens: [],
                num_sentences: text.split(/[.!?]+/).length - 1 || 1
            }
        };
    } catch (error) {
        await worker.terminate();
        URL.revokeObjectURL(imageUrl);
        throw new Error(`Offline OCR failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
}
