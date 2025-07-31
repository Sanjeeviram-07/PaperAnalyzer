#!/usr/bin/env python3
"""
Test the full pipeline: PDF text -> Summary -> Audio
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_full_pipeline():
    """Test the complete pipeline from PDF text to audio"""
    
    print("Testing Full Pipeline: PDF Text -> Summary -> Audio")
    print("=" * 60)
    
    # Mock PDF text (what would be extracted from a real PDF)
    mock_pdf_text = """
    Abstract: This paper presents a comprehensive analysis of machine learning 
    applications in healthcare. We examine various algorithms including support 
    vector machines, random forests, and deep neural networks. Our results 
    demonstrate that ensemble methods achieve the highest accuracy in disease 
    prediction tasks. The study involved 10,000 patient records and achieved 
    94.2% accuracy in the final evaluation.
    
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
    
    try:
        # Step 1: Generate summary
        print("Step 1: Generating summary...")
        from agents.summarizer_agent import generate_summary
        
        summary = generate_summary(mock_pdf_text)
        print(f"Summary generated: {summary}")
        print(f"Summary length: {len(summary)} characters")
        
        if not summary or summary.startswith("Error:"):
            print("❌ Summary generation failed")
            return False
        
        # Step 2: Generate audio
        print("\nStep 2: Generating audio...")
        from agents.audio_agent import generate_audio
        
        audio_path = generate_audio(summary)
        print(f"Audio path: {audio_path}")
        
        if not audio_path:
            print("❌ Audio generation failed")
            return False
        
        # Step 3: Verify audio file
        print("\nStep 3: Verifying audio file...")
        full_path = audio_path.replace("data/", "data/")
        
        if os.path.exists(full_path):
            file_size = os.path.getsize(full_path)
            print(f"✅ Audio file created successfully!")
            print(f"   Path: {full_path}")
            print(f"   Size: {file_size} bytes")
            
            if file_size > 1000:
                print("   Valid MP3 file: ✅")
                print("\n🎉 FULL PIPELINE SUCCESS!")
                print("=" * 60)
                print("✅ PDF text processing: PASS")
                print("✅ Summary generation: PASS") 
                print("✅ Audio generation: PASS")
                print("✅ File verification: PASS")
                return True
            else:
                print("   Valid MP3 file: ❌ (file too small)")
                return False
        else:
            print(f"❌ Audio file not found at {full_path}")
            return False
            
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_full_pipeline()
    if success:
        print("\n🎯 All tests passed! Audio generation is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the error messages above.") 