from pydantic import BaseModel
from typing import List, Optional

class OCRRequest(BaseModel):
    lang: str = "eng"

class OCRResponse(BaseModel):
    text: str
    corrected_text: Optional[str] = None

class Entity(BaseModel):
    text: str
    label: str

class TokenInfo(BaseModel):
    text: str
    pos: str
    lemma: str

class NLPAnalysisResult(BaseModel):
    entities: List[Entity]
    tokens: List[TokenInfo]
    num_sentences: int

class FullAnalysisResponse(BaseModel):
    text: str
    corrected_text: Optional[str] = None
    nlp_analysis: Optional[NLPAnalysisResult] = None

class AIAnalysisResponse(BaseModel):
    text: str
    corrected_text: Optional[str] = None
    nlp_analysis: Optional[NLPAnalysisResult] = None
    ai_corrected_text: Optional[str] = None
    summary: Optional[str] = None
    ai_score: Optional[float] = None


class PageAnalysis(BaseModel):
    page_number: int
    text: str
    summary: Optional[str] = None
    ai_score: Optional[float] = None
    ai_corrected_text: Optional[str] = None

class PDFPageAnalysisResponse(BaseModel):
    total_pages: int
    pages: List[PageAnalysis]
    overall_summary: Optional[str] = None
    overall_score: Optional[float] = None
