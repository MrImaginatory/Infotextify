from app.schemas.ocr import NLPAnalysisResult
from typing import Optional
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

def generate_report(text: str, nlp_result: Optional[NLPAnalysisResult], corrected_text: Optional[str] = None) -> str:
    """
    Generate a text report that mimics the original CLI output layout.
    """
    output = []
    
    # Extracted Text Section
    output.append("\n" + "="*50)
    output.append("EXTRACTED TEXT")
    output.append("="*50)
    output.append(text)
    
    # Corrected Text Section
    if corrected_text:
        output.append("\n" + "="*50)
        output.append("CORRECTED TEXT")
        output.append("="*50)
        output.append(corrected_text)
    
    # NLP Analysis Section
    if nlp_result:
        output.append("\n" + "="*50)
        output.append("SPACY NLP ANALYSIS")
        output.append("="*50)
        
        # Entities
        if nlp_result.entities:
            output.append("\nNamed Entities:")
            for ent in nlp_result.entities:
                output.append(f"  - {ent.text}: {ent.label}")
        
        # Part of Speech (Original script showed first 20)
        output.append("\nTokens (first 20):")
        # In schemas/ocr.py TokenInfo has text, pos, lemma
        # We need to access attributes of TokenInfo objects
        count = 0
        for token in nlp_result.tokens:
            if count >= 20: 
                break
            output.append(f"  {token.text:15} | POS: {token.pos:10} | Lemma: {token.lemma}")
            count += 1
            
        # Sentences
        output.append(f"\nNumber of sentences: {nlp_result.num_sentences}")
        
    return "\n".join(output) + "\n"

def generate_html_report(text: str, nlp_result: Optional[NLPAnalysisResult], lang: str, corrected_text: Optional[str] = None) -> str:
    """
    Generate an HTML report using the Jinja2 template.
    """
    # Setup Jinja2 environment
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report.html')
    
    # Render template
    return template.render(
        text=text,
        corrected_text=corrected_text,
        nlp_result=nlp_result,
        lang=lang,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
