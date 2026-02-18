import type { OCRRequest, OCRResponse, PDFAnalysisResponse } from '../types/ocr';

const BACKEND_URL = import.meta.env.VITE_API_BACKEND_URL;

const API_ENDPOINT = `${BACKEND_URL}/ocr/analyze/ollama`;
const PDF_API_ENDPOINT = `${BACKEND_URL}/ocr/analyze/pdf-pages`;
const REQUEST_TIMEOUT = 300000; // 5 minutes

export async function analyzeImage(request: OCRRequest): Promise<OCRResponse> {
    const formData = new FormData();
    formData.append('file', request.file);
    formData.append('lang', request.lang);
    formData.append('autocorrect', String(request.autocorrect));
    formData.append('contrast', String(request.contrast));
    formData.append('brightness', String(request.brightness));
    formData.append('sharpness', String(request.sharpness));

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            body: formData,
            signal: controller.signal,
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            if (response.status >= 500) {
                throw new Error('Service temporarily unavailable. Please try again later.');
            } else if (response.status === 413) {
                throw new Error('File is too large. Please upload a smaller image.');
            } else if (response.status >= 400) {
                throw new Error('Invalid request. Please check your file and try again.');
            }
            throw new Error(`OCR API error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        clearTimeout(timeoutId);

        if (error instanceof Error) {
            if (error.name === 'AbortError') {
                throw new Error('Request timed out. Please try again.');
            }
            throw error;
        }

        throw new Error('Network error. Please check your connection and try again.');
    }
}

export async function analyzePdf(request: OCRRequest): Promise<PDFAnalysisResponse> {
    const formData = new FormData();
    formData.append('file', request.file);
    formData.append('lang', request.lang);
    formData.append('contrast', String(request.contrast));
    formData.append('brightness', String(request.brightness));
    formData.append('sharpness', String(request.sharpness));

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

    try {
        const response = await fetch(PDF_API_ENDPOINT, {
            method: 'POST',
            body: formData,
            signal: controller.signal,
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            if (response.status >= 500) {
                throw new Error('Service temporarily unavailable. Please try again later.');
            } else if (response.status === 413) {
                throw new Error('File is too large. Please upload a smaller PDF.');
            } else if (response.status >= 400) {
                throw new Error('Invalid request. Please check your file and try again.');
            }
            throw new Error(`PDF Analysis API error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        clearTimeout(timeoutId);

        if (error instanceof Error) {
            if (error.name === 'AbortError') {
                throw new Error('Request timed out. PDF analysis may take longer for large files. Please try again.');
            }
            throw error;
        }

        throw new Error('Network error. Please check your connection and try again.');
    }
}
