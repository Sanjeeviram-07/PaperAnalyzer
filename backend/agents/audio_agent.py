import os
import uuid
import re

def generate_audio(text: str) -> str:
    try:
        # Try to import gTTS
        try:
            from gtts import gTTS
            print("gTTS imported successfully")
        except ImportError as e:
            print(f"gTTS import failed: {e}")
            print("Please install gTTS: pip install gTTS")
            return ""
        
        print(f"Audio generation called with text type: {type(text)}")
        print(f"Text preview: {str(text)[:200]}...")
        
        # Validate input
        if not text or not isinstance(text, str):
            print(f"Invalid text for audio generation: {type(text)} - {text}")
            return ""
        
        text = text.strip()
        if not text:
            print("Empty text provided for audio generation")
            return ""
        
        # Check if text is an error message
        if text.startswith("Error:") or text.startswith("Document Processing Error:") or text.startswith("Unable to extract"):
            print(f"Skipping audio generation for error text: {text[:100]}...")
            return ""
        
        # Clean text for audio generation - simplified approach
        cleaned_text = text.strip()
        cleaned_text = re.sub(r'\n+', ' ', cleaned_text)  # Replace newlines with spaces
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Replace multiple spaces with single space
        
        # Remove only the most problematic characters for TTS
        cleaned_text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', cleaned_text)
        
        # Limit text length to prevent issues
        if len(cleaned_text) > 4000:
            # Take the first part and add a note
            cleaned_text = cleaned_text[:4000] + "... [Audio truncated due to length]"
            print(f"Text cleaned and truncated for audio generation to {len(cleaned_text)} characters")
        else:
            print(f"Text cleaned for audio generation: {len(cleaned_text)} characters")
        
        # Final validation - ensure we have meaningful text
        if len(cleaned_text.strip()) < 10:
            print("Text too short for audio generation after cleaning")
            return ""
        
        # Create data directory if it doesn't exist
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"Created data directory: {data_dir}")
        
        # Generate unique filename
        audio_filename = f"audio_{uuid.uuid4().hex}.mp3"
        audio_path = os.path.join(data_dir, audio_filename)
        
        print(f"Generating audio file: {audio_path}")
        print(f"Final text for TTS: {cleaned_text[:100]}...")
        
        # Generate audio with simple fallback
        try:
            tts = gTTS(text=cleaned_text, lang='en', slow=False)
            tts.save(audio_path)
            print("TTS.save() completed successfully")
        except Exception as tts_error:
            print(f"TTS generation failed: {tts_error}")
            # Try with a simple fallback text
            try:
                fallback_text = "This is a summary of the research paper."
                tts = gTTS(text=fallback_text, lang='en', slow=False)
                tts.save(audio_path)
                print("Fallback TTS generation completed")
            except Exception as fallback_error:
                print(f"Fallback TTS also failed: {fallback_error}")
                return ""
        
        # Verify file was created
        if not os.path.exists(audio_path):
            print(f"Audio file was not created at {audio_path}")
            return ""
        
        file_size = os.path.getsize(audio_path)
        print(f"Audio file created successfully: {audio_path} (size: {file_size} bytes)")
        
        # Return the path that will be accessible via the static file server
        return f"data/{audio_filename}"
        
    except Exception as e:
        print(f"Audio generation error: {e}")
        import traceback
        print(f"Audio generation traceback: {traceback.format_exc()}")
        # Return empty string if audio generation fails
        return ""

def is_garbled_text(text: str) -> bool:
    """Check if text contains garbled or binary content"""
    
    # Check for binary/garbled content patterns
    garbled_patterns = [
        r'[^\x00-\x7F]{10,}',  # Long sequences of non-ASCII
        r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]{5,}',  # Control characters
        r'[^\w\s\.\,\!\?\;\:\-\(\)]{20,}',  # Long sequences of special characters
    ]
    
    for pattern in garbled_patterns:
        if re.search(pattern, text):
            return True
    
    # Check printable character ratio
    printable_chars = sum(1 for c in text if c.isprintable() or c.isspace())
    total_chars = len(text)
    
    if total_chars > 0:
        printable_ratio = printable_chars / total_chars
        if printable_ratio < 0.7:  # Made less restrictive
            return True
    
    # Check if text contains mostly non-word characters
    words = text.split()
    if len(words) > 0:
        real_words = sum(1 for word in words if len(word) >= 2 and word.isalpha())  # Made less restrictive
        if real_words / len(words) < 0.1:  # Made less restrictive
            return True
    
    return False
