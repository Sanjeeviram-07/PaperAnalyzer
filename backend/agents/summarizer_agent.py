import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

def generate_summary(text: str) -> str:
    try:
        # Validate input text
        if not text or not isinstance(text, str):
            return "Error: Invalid text provided for summarization."
        
        # Check if text is an error message or contains garbled content
        if text.startswith("Error:") or text.startswith("Unable to extract"):
            return f"Document Processing Error: {text}"
        
        # Check for garbled or binary content
        if is_garbled_text(text):
            return "Error: The document contains unreadable or binary content that cannot be summarized."
        
        # Clean the text for better summarization
        cleaned_text = clean_text_for_summarization(text)
        
        if len(cleaned_text.strip()) < 100:
            return "Error: The document contains insufficient readable text for summarization."
        
        from transformers import pipeline
        
        # Initialize the summarization pipeline with caching
        cache_dir = Config.get_model_cache_dir()
        summarizer = pipeline(
            "summarization", 
            model="facebook/bart-large-cnn",
            cache_dir=cache_dir
        )
        
        # Truncate text if it's too long (BART has input length limits)
        max_input_length = 1024
        if len(cleaned_text) > max_input_length:
            cleaned_text = cleaned_text[:max_input_length]
        
        # Generate summary
        result = summarizer(cleaned_text, max_length=130, min_length=30, do_sample=False)
        summary = result[0]['summary_text']
        
        # Validate the generated summary
        if len(summary.strip()) < 20:
            return "Error: Generated summary is too short or empty."
        
        return summary
        
    except Exception as e:
        # Fallback to simple text analysis if summarization fails
        print(f"Summarization error: {e}")
        return create_fallback_summary(text)

def clean_text_for_summarization(text: str) -> str:
    """Clean text for better summarization results"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove common PDF artifacts
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)  # Remove control characters
    
    # Remove page numbers and headers/footers
    text = re.sub(r'\b\d+\s*of\s*\d+\b', '', text)  # "Page X of Y"
    text = re.sub(r'\bpage\s+\d+\b', '', text, flags=re.IGNORECASE)  # "Page X"
    
    # Remove excessive punctuation
    text = re.sub(r'[.!?]{3,}', '.', text)  # Multiple punctuation marks
    
    return text.strip()

def is_garbled_text(text: str) -> bool:
    """Check if text contains garbled or binary content"""
    if not text or not isinstance(text, str):
        return True
    
    # Check for binary/garbled content patterns
    if text.startswith('%PDF-1.') or text.startswith('%PDF-2.'):
        return True
    
    # Check for excessive binary characters
    binary_chars = sum(1 for c in text if ord(c) < 32 and c not in '\n\r\t')
    if binary_chars > len(text) * 0.1:  # More than 10% binary chars
        return True
    
    # Check printable character ratio
    printable_chars = sum(1 for c in text if c.isprintable() or c.isspace())
    if len(text) > 0 and printable_chars / len(text) < 0.8:
        return True
    
    # Check if text contains mostly non-word characters
    words = text.split()
    if len(words) > 0:
        real_words = sum(1 for word in words if len(word) >= 3 and word.isalpha())
        if real_words / len(words) < 0.2:
            return True
    
    return False

def create_fallback_summary(text: str) -> str:
    """Create a simple fallback summary when AI summarization fails"""
    try:
        # Clean the text
        cleaned_text = clean_text_for_summarization(text)
        
        if len(cleaned_text) < 100:
            return "Error: Document contains insufficient readable content for summarization."
        
        # Take the first few sentences as a simple summary
        sentences = re.split(r'[.!?]+', cleaned_text)
        meaningful_sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if not meaningful_sentences:
            return "Error: No meaningful sentences found in the document."
        
        # Take first 2-3 meaningful sentences
        summary_sentences = meaningful_sentences[:3]
        fallback_summary = '. '.join(summary_sentences) + '.'
        
        # Truncate if too long
        if len(fallback_summary) > 500:
            fallback_summary = fallback_summary[:500] + "..."
        
        return f"Document Summary (extracted from beginning): {fallback_summary}"
        
    except Exception as e:
        return f"Error: Unable to create summary due to processing error: {str(e)}"
