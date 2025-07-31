#!/usr/bin/env python3
"""
Test script to verify PDF parsing and audio generation fixes
"""

import asyncio
import os
import sys
from io import BytesIO

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.parser_agent import read_pdf, is_valid_text
from agents.summarizer_agent import generate_summary, is_garbled_text
from agents.audio_agent import generate_audio

class MockUploadFile:
    """Mock UploadFile for testing"""
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content
    
    async def read(self):
        return self.content

async def test_pdf_parsing():
    """Test PDF parsing with various scenarios"""
    print("Testing PDF parsing improvements...")
    
    # Test 1: Valid PDF content
    print("\n1. Testing with valid text content...")
    valid_content = b"This is a test PDF content with meaningful text that should be parsed correctly."
    mock_file = MockUploadFile("test.pdf", valid_content)
    
    try:
        result = await read_pdf(mock_file)
        print(f"Result: {result[:100]}...")
        print(f"Valid text: {is_valid_text(result)}")
        print(f"Garbled text: {is_garbled_text(result)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Binary/garbled content
    print("\n2. Testing with binary content...")
    binary_content = b"%PDF-1.5\n%binary content here..."
    mock_file = MockUploadFile("binary.pdf", binary_content)
    
    try:
        result = await read_pdf(mock_file)
        print(f"Result: {result[:100]}...")
        print(f"Valid text: {is_valid_text(result)}")
        print(f"Garbled text: {is_garbled_text(result)}")
    except Exception as e:
        print(f"Error: {e}")

def test_summarization():
    """Test summarization with various text types"""
    print("\nTesting summarization improvements...")
    
    # Test 1: Valid text
    print("\n1. Testing with valid text...")
    valid_text = """
    This is a research paper about machine learning and artificial intelligence. 
    The paper discusses various algorithms and their applications in real-world scenarios.
    Machine learning has become increasingly important in modern technology.
    """
    
    try:
        summary = generate_summary(valid_text)
        print(f"Summary: {summary}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Garbled text
    print("\n2. Testing with garbled text...")
    garbled_text = "%PDF-1.5 %binary content here..."
    
    try:
        summary = generate_summary(garbled_text)
        print(f"Summary: {summary}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Error message
    print("\n3. Testing with error message...")
    error_text = "Error: Unable to extract text from PDF"
    
    try:
        summary = generate_summary(error_text)
        print(f"Summary: {summary}")
    except Exception as e:
        print(f"Error: {e}")

def test_audio_generation():
    """Test audio generation with various text types"""
    print("\nTesting audio generation improvements...")
    
    # Test 1: Valid text
    print("\n1. Testing with valid text...")
    valid_text = "This is a test summary for audio generation. It should work correctly."
    
    try:
        audio_path = generate_audio(valid_text)
        print(f"Audio path: {audio_path}")
        if audio_path and os.path.exists(audio_path.replace("data/", "data/")):
            print("Audio file created successfully!")
        else:
            print("Audio file not created")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Error text
    print("\n2. Testing with error text...")
    error_text = "Error: Document contains unreadable content"
    
    try:
        audio_path = generate_audio(error_text)
        print(f"Audio path: {audio_path}")
        if not audio_path:
            print("Audio generation correctly skipped for error text")
        else:
            print("Audio generation should have been skipped")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    """Run all tests"""
    print("Starting PDF and Audio Generation Tests")
    print("=" * 50)
    
    # Test PDF parsing
    await test_pdf_parsing()
    
    # Test summarization
    test_summarization()
    
    # Test audio generation
    test_audio_generation()
    
    print("\n" + "=" * 50)
    print("Tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 