import spacy
from typing import List, Dict

nlp = spacy.load("en_core_web_sm")

def extract_scientist_info(article_text: str) -> Dict:
    """Extract named entities and sentences about the scientist."""
    doc = nlp(article_text)
    
    # Find person names (potential scientist)
    people = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    
    # Extract sentences for manual inspection
    sentences = [sent.text for sent in doc.sents]
    
    return {
        "potential_scientists": people[:5],  # Top 5 names
        "sentences": sentences,
        "num_sentences": len(sentences)
    }

def flag_baseline_phrases(text: str) -> List[Dict[str, str]]:
    """Simple rule-based flags for prof's 'blatant violations'."""
    red_flags = [
        "first woman to",
        "male-dominated field",
        "balances her research with",
        "as a woman in",
        "mother of",
        "first female"
    ]
    
    flags = []
    for phrase in red_flags:
        if phrase.lower() in text.lower():
            flags.append({
                "phrase": phrase,
                "context": text.lower().find(phrase.lower())
            })
    return flags