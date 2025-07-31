#!/usr/bin/env python3
"""
Test script specifically for audio generation fixes
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.audio_agent import generate_audio

def test_audio_generation():
    """Test audio generation with various valid summaries"""
    print("Testing Audio Generation Fixes")
    print("=" * 50)
    
    # Test cases with valid summaries
    test_cases = [
        {
            "name": "Simple Summary",
            "text": "This research paper discusses machine learning algorithms and their applications in real-world scenarios."
        },
        {
            "name": "Longer Summary",
            "text": "The study examines the effectiveness of deep learning models in natural language processing tasks. Results show significant improvements in accuracy compared to traditional methods. The research contributes to the field by introducing novel approaches to text classification."
        },
        {
            "name": "Summary with Special Characters",
            "text": "This paper presents findings on AI & ML applications in healthcare. The study (2023) shows 95% accuracy in disease detection. Results indicate: improved diagnosis, reduced costs, and better patient outcomes."
        },
        {
            "name": "Summary with Numbers",
            "text": "The research demonstrates a 25% improvement in performance using the proposed algorithm. The study involved 1,000 participants and achieved 92.5% accuracy in the final results."
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print(f"Input text: {test_case['text'][:100]}...")
        
        try:
            audio_path = generate_audio(test_case['text'])
            
            if audio_path:
                print(f"✅ Audio generated successfully!")
                print(f"   Path: {audio_path}")
                
                # Check if file exists
                full_path = audio_path.replace("data/", "data/")
                if os.path.exists(full_path):
                    file_size = os.path.getsize(full_path)
                    print(f"   File size: {file_size} bytes")
                    print(f"   File exists: ✅")
                else:
                    print(f"   File exists: ❌")
            else:
                print(f"❌ Audio generation failed - returned empty path")
                
        except Exception as e:
            print(f"❌ Error during audio generation: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")

def test_error_handling():
    """Test that audio generation correctly skips error messages"""
    print("\n" + "=" * 50)
    print("Testing Error Handling")
    print("=" * 50)
    
    error_cases = [
        {
            "name": "Error Message",
            "text": "Error: Unable to extract text from PDF"
        },
        {
            "name": "Document Processing Error",
            "text": "Document Processing Error: The file may be corrupted"
        },
        {
            "name": "Insufficient Content",
            "text": "Document contains insufficient readable content for summarization"
        }
    ]
    
    for i, test_case in enumerate(error_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print(f"Input text: {test_case['text']}")
        
        try:
            audio_path = generate_audio(test_case['text'])
            
            if not audio_path:
                print(f"✅ Correctly skipped audio generation for error text")
            else:
                print(f"❌ Should have skipped audio generation but didn't")
                print(f"   Returned path: {audio_path}")
                
        except Exception as e:
            print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    test_audio_generation()
    test_error_handling()
    print("\n" + "=" * 50)
    print("Audio generation tests completed!") 