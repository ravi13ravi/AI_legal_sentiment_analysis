import re

def clean_legal_text(text):
    text = re.sub(r'\[\d+.*?\d+\)', '', text)  # Remove citations
    text = ' '.join(text.split())               # Normalize whitespace
    return text