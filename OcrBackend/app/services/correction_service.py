from textblob import TextBlob
from functools import lru_cache

class GrammarCorrector:
    def __init__(self):
        # TextBlob doesn't require explicit initialization for simple correction
        pass

    def correct_text(self, text: str) -> str:
        """
        Corrects grammatical and spelling errors in the text.
        """
        if not text or not text.strip():
             return text
        
        # Split but keep whitespace to preserve formatting
        import re
        tokens = re.split(r'(\s+)', text)
        corrected_tokens = []
        
        for token in tokens:
            # Skip whitespace
            if not token.strip():
                corrected_tokens.append(token)
                continue
            
            # Correct word
            blob = TextBlob(token)
            corrected_word = str(blob.correct())
            
            if token != corrected_word:
                corrected_tokens.append(f"{corrected_word}*")
            else:
                corrected_tokens.append(token)
                
        return "".join(corrected_tokens)

# Singleton instance
_corrector_instance = None

def get_corrector():
    global _corrector_instance
    if _corrector_instance is None:
        _corrector_instance = GrammarCorrector()
    return _corrector_instance

def correct_text(text: str) -> str:
    """
    Convenience function to correct text using the singleton instance.
    """
    corrector = get_corrector()
    return corrector.correct_text(text)
