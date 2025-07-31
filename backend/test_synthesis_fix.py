#!/usr/bin/env python3
"""
Test script to verify the synthesis error fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.synthesizer_agent import synthesize_papers
from agents.audio_agent import generate_audio

def test_synthesis_with_none():
    """Test synthesis with None values"""
    print("Testing synthesis with None values...")
    
    # Test with empty papers list
    try:
        result = synthesize_papers([], "comprehensive")
        print(f"Empty papers result: {result['synthesis'][:100]}...")
        assert result['synthesis'] is not None
        print("✓ Empty papers test passed")
    except Exception as e:
        print(f"✗ Empty papers test failed: {e}")
    
    # Test with None values in papers
    try:
        papers_with_none = [
            {
                'title': None,
                'authors': None,
                'summary': None,
                'year': None,
                'source': 'test'
            }
        ]
        result = synthesize_papers(papers_with_none, "comprehensive")
        print(f"None values result: {result['synthesis'][:100]}...")
        assert result['synthesis'] is not None
        print("✓ None values test passed")
    except Exception as e:
        print(f"✗ None values test failed: {e}")

def test_audio_with_none():
    """Test audio generation with None values"""
    print("\nTesting audio generation with None values...")
    
    # Test with None
    try:
        result = generate_audio(None)
        print(f"None input result: '{result}'")
        assert result == ""
        print("✓ None input test passed")
    except Exception as e:
        print(f"✗ None input test failed: {e}")
    
    # Test with empty string
    try:
        result = generate_audio("")
        print(f"Empty string result: '{result}'")
        assert result == ""
        print("✓ Empty string test passed")
    except Exception as e:
        print(f"✗ Empty string test failed: {e}")
    
    # Test with valid text
    try:
        result = generate_audio("This is a test synthesis.")
        print(f"Valid text result: '{result}'")
        assert result == "" or result.startswith("data/")
        print("✓ Valid text test passed")
    except Exception as e:
        print(f"✗ Valid text test failed: {e}")

def test_normal_synthesis():
    """Test normal synthesis functionality"""
    print("\nTesting normal synthesis functionality...")
    
    try:
        papers = [
            {
                'title': 'Test Paper 1',
                'authors': ['Author A'],
                'summary': 'This paper discusses machine learning. The findings show that deep learning is effective.',
                'year': '2023',
                'source': 'test'
            },
            {
                'title': 'Test Paper 2',
                'authors': ['Author B'],
                'summary': 'This research explores neural networks. The study demonstrates improved performance.',
                'year': '2023',
                'source': 'test'
            }
        ]
        
        result = synthesize_papers(papers, "comprehensive")
        print(f"Normal synthesis result: {result['synthesis'][:200]}...")
        assert result['synthesis'] is not None and len(result['synthesis']) > 0
        print("✓ Normal synthesis test passed")
        
    except Exception as e:
        print(f"✗ Normal synthesis test failed: {e}")

if __name__ == "__main__":
    print("=== Synthesis Error Fix Test ===\n")
    
    try:
        test_synthesis_with_none()
        test_audio_with_none()
        test_normal_synthesis()
        
        print("\n=== All tests completed! ===")
        
    except Exception as e:
        print(f"Test suite failed with error: {e}")
        import traceback
        traceback.print_exc() 