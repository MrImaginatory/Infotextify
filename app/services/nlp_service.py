from typing import Optional
from fastapi import HTTPException, status
from app.core.config import settings
from app.schemas.ocr import NLPAnalysisResult, Entity, TokenInfo

# Global variable to store loaded model
nlp_model = None
SPACY_AVAILABLE = False

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    pass

def get_nlp_model():
    """Lazily load the spaCy model."""
    global nlp_model
    if not SPACY_AVAILABLE:
         raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="spaCy is not installed on the server."
        )
    
    if nlp_model is None:
        try:
            nlp_model = spacy.load(settings.SPACY_MODEL)
        except OSError:
             raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"spaCy model '{settings.SPACY_MODEL}' not found. Please install it."
            )
    return nlp_model

def process_text(text: str) -> Optional[NLPAnalysisResult]:
    """
    Process text with spaCy and return structured analysis.
    
    Args:
        text: Text to process
        
    Returns:
        NLPAnalysisResult object or None if text is empty
    """
    if not text.strip():
        return None

    nlp = get_nlp_model()
    
    try:
        doc = nlp(text)
        
        entities = [
            Entity(text=ent.text, label=ent.label_) 
            for ent in doc.ents
        ]
        
        # Limit to first 50 tokens to avoid huge responses for large texts
        tokens = [
            TokenInfo(text=token.text, pos=token.pos_, lemma=token.lemma_)
            for token in list(doc)[:50]
        ]
        
        return NLPAnalysisResult(
            entities=entities,
            tokens=tokens,
            num_sentences=len(list(doc.sents))
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during NLP processing: {str(e)}"
        )
