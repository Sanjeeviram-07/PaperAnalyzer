#!/usr/bin/env python3
"""
Debug script for audio generation issues
"""

import os
import sys
import traceback

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_gtts_installation():
    """Test if gTTS is properly installed"""
    print("Testing gTTS installation...")
    try:
        from gtts import gTTS
        print("✅ gTTS imported successfully")
        
        # Test basic TTS functionality
        test_text = "Hello, this is a test."
        tts = gTTS(text=test_text, lang='en', slow=False)
        print("✅ gTTS object created successfully")
        
        # Test saving to a temporary file
        temp_path = "temp_test.mp3"
        tts.save(temp_path)
        
        if os.path.exists(temp_path):
            print(f"✅ Test audio file created: {temp_path}")
            file_size = os.path.getsize(temp_path)
            print(f"   File size: {file_size} bytes")
            os.remove(temp_path)  # Clean up
            print("✅ Test audio file cleaned up")
            return True
        else:
            print("❌ Test audio file was not created")
            return False
            
    except ImportError as e:
        print(f"❌ gTTS import failed: {e}")
        print("Please install gTTS: pip install gTTS")
        return False
    except Exception as e:
        print(f"❌ gTTS test failed: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_audio_agent():
    """Test the audio agent with various inputs"""
    print("\nTesting Audio Agent...")
    
    try:
        from agents.audio_agent import generate_audio
        
        # Test 1: Simple valid text
        print("\n1. Testing with simple valid text...")
        simple_text = "This is a simple test summary for audio generation."
        result = generate_audio(simple_text)
        print(f"Result: {result}")
        
        # Test 2: Longer valid text
        print("\n2. Testing with longer valid text...")
        longer_text = """
        This research paper examines the effectiveness of machine learning algorithms 
        in natural language processing tasks. The study demonstrates significant 
        improvements in accuracy compared to traditional methods. Results show 
        that deep learning approaches achieve better performance across multiple 
        evaluation metrics.
        """
        result = generate_audio(longer_text)
        print(f"Result: {result}")
        
        # Test 3: Error text (should be skipped)
        print("\n3. Testing with error text (should be skipped)...")
        error_text = "Error: Unable to extract text from PDF"
        result = generate_audio(error_text)
        print(f"Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Audio agent test failed: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_full_pipeline():
    """Test the full pipeline with a mock summary"""
    print("\nTesting Full Pipeline...")
    
    try:
        from agents.summarizer_agent import generate_summary
        from agents.audio_agent import generate_audio
        
        # Create a mock research paper text
        mock_paper_text = """
        Abstract: This paper presents a comprehensive study of machine learning 
        applications in healthcare. We analyze various algorithms including 
        support vector machines, random forests, and deep neural networks. 
        Our results demonstrate that ensemble methods achieve the highest 
        accuracy in disease prediction tasks. The study involved 10,000 
        patient records and achieved 94.2% accuracy in the final evaluation.
        
        Introduction: Machine learning has revolutionized healthcare by enabling 
        early disease detection and personalized treatment plans. Recent advances 
        in deep learning have shown promising results in medical image analysis 
        and patient outcome prediction.
        
        Methods: We collected data from multiple hospitals and applied various 
        preprocessing techniques. Feature engineering was performed using domain 
        expertise and statistical analysis. Cross-validation was used to ensure 
        robust model evaluation.
        
        Results: Our experiments show that random forest algorithms achieve 
        94.2% accuracy in disease prediction, outperforming other methods. 
        Deep learning models show similar performance but require more 
        computational resources.
        
        Conclusion: Machine learning algorithms show great promise in healthcare 
        applications. Future work will focus on real-time deployment and 
        integration with existing medical systems.
        """
        
        print("1. Generating summary...")
        summary = generate_summary(mock_paper_text)
        print(f"Summary: {summary}")
        
        print("\n2. Generating audio from summary...")
        audio_path = generate_audio(summary)
        print(f"Audio path: {audio_path}")
        
        if audio_path:
            full_path = audio_path.replace("data/", "data/")
            if os.path.exists(full_path):
                file_size = os.path.getsize(full_path)
                print(f"✅ Audio file created successfully!")
                print(f"   Path: {full_path}")
                print(f"   Size: {file_size} bytes")
                return True
            else:
                print(f"❌ Audio file not found at {full_path}")
                return False
        else:
            print("❌ No audio path returned")
            return False
            
    except Exception as e:
        print(f"❌ Full pipeline test failed: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def main():
    """Run all tests"""
    print("Audio Generation Debug Tests")
    print("=" * 50)
    
    # Test 1: gTTS installation
    gtts_ok = test_gtts_installation()
    
    # Test 2: Audio agent
    agent_ok = test_audio_agent()
    
    # Test 3: Full pipeline
    pipeline_ok = test_full_pipeline()
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print(f"gTTS Installation: {'✅ PASS' if gtts_ok else '❌ FAIL'}")
    print(f"Audio Agent: {'✅ PASS' if agent_ok else '❌ FAIL'}")
    print(f"Full Pipeline: {'✅ PASS' if pipeline_ok else '❌ FAIL'}")
    
    if not gtts_ok:
        print("\n🔧 Fix: Install gTTS with: pip install gTTS")
    
    if not agent_ok:
        print("\n🔧 Fix: Check audio agent implementation")
    
    if not pipeline_ok:
        print("\n🔧 Fix: Check summary generation or audio agent")

if __name__ == "__main__":
    main() 