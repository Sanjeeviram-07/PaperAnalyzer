#!/usr/bin/env python3
"""
Simple test to generate audio from a real summary
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_real_audio():
    """Test audio generation with a realistic summary"""
    
    # This is what a typical summary looks like
    real_summary = "The research demonstrates significant improvements in machine learning performance using novel algorithms. Results show 25% better accuracy compared to baseline methods. The study contributes to the field by introducing innovative approaches to data processing."
    
    print("Testing audio generation with real summary...")
    print(f"Summary: {real_summary}")
    
    try:
        from agents.audio_agent import generate_audio
        
        print("\nCalling generate_audio...")
        audio_path = generate_audio(real_summary)
        
        print(f"\nResult: {audio_path}")
        
        if audio_path:
            full_path = audio_path.replace("data/", "data/")
            if os.path.exists(full_path):
                file_size = os.path.getsize(full_path)
                print(f"✅ SUCCESS! Audio file created:")
                print(f"   Path: {full_path}")
                print(f"   Size: {file_size} bytes")
                
                # Test if it's a valid MP3 file
                if file_size > 1000:  # MP3 files should be at least 1KB
                    print(f"   Valid MP3 file: ✅")
                else:
                    print(f"   Valid MP3 file: ❌ (too small)")
            else:
                print(f"❌ Audio file not found at {full_path}")
        else:
            print("❌ No audio path returned")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_real_audio() 