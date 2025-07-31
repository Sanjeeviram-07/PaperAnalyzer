#!/usr/bin/env python3
"""
Test script for cross-paper synthesis functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.synthesizer_agent import (
    search_arxiv_papers,
    search_semantic_scholar_papers,
    synthesize_papers,
    extract_key_insights
)

def test_arxiv_search():
    """Test arXiv paper search"""
    print("Testing arXiv paper search...")
    papers = search_arxiv_papers("machine learning", max_results=3)
    print(f"Found {len(papers)} papers from arXiv")
    for i, paper in enumerate(papers):
        print(f"  {i+1}. {paper['title'][:60]}...")
    return papers

def test_semantic_scholar_search():
    """Test Semantic Scholar paper search"""
    print("\nTesting Semantic Scholar paper search...")
    papers = search_semantic_scholar_papers("deep learning", max_results=3)
    print(f"Found {len(papers)} papers from Semantic Scholar")
    for i, paper in enumerate(papers):
        print(f"  {i+1}. {paper['title'][:60]}...")
    return papers

def test_synthesis():
    """Test paper synthesis"""
    print("\nTesting paper synthesis...")
    
    # Create sample papers for testing
    sample_papers = [
        {
            'title': 'Machine Learning Approaches for Data Analysis',
            'authors': ['Author A', 'Author B'],
            'summary': 'This paper presents novel machine learning methods for analyzing large datasets. The findings show that deep learning models achieve 95% accuracy on benchmark datasets.',
            'year': '2023',
            'source': 'arxiv'
        },
        {
            'title': 'Deep Learning in Computer Vision',
            'authors': ['Author C', 'Author D'],
            'summary': 'This research explores convolutional neural networks for image recognition. The study demonstrates that CNN-based approaches outperform traditional methods by 15%.',
            'year': '2023',
            'source': 'semantic_scholar'
        },
        {
            'title': 'Neural Network Optimization Techniques',
            'authors': ['Author E', 'Author F'],
            'summary': 'This work investigates various optimization algorithms for training neural networks. Results indicate that Adam optimizer provides the best convergence rates.',
            'year': '2023',
            'source': 'arxiv'
        }
    ]
    
    # Test different synthesis types
    synthesis_types = ['comprehensive', 'comparative', 'thematic']
    
    for synthesis_type in synthesis_types:
        print(f"\n--- {synthesis_type.upper()} SYNTHESIS ---")
        result = synthesize_papers(sample_papers, synthesis_type)
        print(f"Total papers: {result['total_papers']}")
        print(f"Common themes: {result['common_themes']}")
        print(f"Synthesis preview: {result['synthesis'][:200]}...")

def test_key_insights():
    """Test key insights extraction"""
    print("\nTesting key insights extraction...")
    
    sample_text = """
    This study investigates machine learning applications in healthcare. 
    The findings demonstrate that our proposed model achieves 92% accuracy 
    in disease prediction. The research shows significant improvements over 
    existing methods. We conclude that deep learning approaches are highly 
    effective for medical diagnosis.
    """
    
    insights = extract_key_insights(sample_text)
    print(f"Extracted insights: {insights}")

if __name__ == "__main__":
    print("=== Cross-Paper Synthesis Test ===\n")
    
    try:
        # Test key insights extraction
        test_key_insights()
        
        # Test synthesis with sample data
        test_synthesis()
        
        # Test API searches (these might fail if no internet connection)
        try:
            test_arxiv_search()
        except Exception as e:
            print(f"arXiv search failed: {e}")
        
        try:
            test_semantic_scholar_search()
        except Exception as e:
            print(f"Semantic Scholar search failed: {e}")
        
        print("\n=== Test completed successfully! ===")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc() 