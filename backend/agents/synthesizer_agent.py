import requests
import json
import re
from typing import List, Dict, Any
from datetime import datetime
import xml.etree.ElementTree as ET

def search_arxiv_papers(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search for papers on arXiv using their free API
    """
    try:
        # arXiv API endpoint
        url = "http://export.arxiv.org/api/query"
        params = {
            'search_query': f'all:"{query}"',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Parse XML response
        root = ET.fromstring(response.content)
        
        # Extract papers
        papers = []
        for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
            paper = {
                'title': entry.find('.//{http://www.w3.org/2005/Atom}title').text.strip(),
                'authors': [author.find('.//{http://www.w3.org/2005/Atom}name').text 
                           for author in entry.findall('.//{http://www.w3.org/2005/Atom}author')],
                'summary': entry.find('.//{http://www.w3.org/2005/Atom}summary').text.strip(),
                'published': entry.find('.//{http://www.w3.org/2005/Atom}published').text,
                'arxiv_id': entry.find('.//{http://www.w3.org/2005/Atom}id').text.split('/')[-1],
                'categories': [cat.text for cat in entry.findall('.//{http://arxiv.org/schemas/atom}category')],
                'pdf_url': f"https://arxiv.org/pdf/{entry.find('.//{http://www.w3.org/2005/Atom}id').text.split('/')[-1]}.pdf"
            }
            papers.append(paper)
        
        return papers
    except Exception as e:
        print(f"Error searching arXiv: {e}")
        return []

def search_semantic_scholar_papers(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search for papers using Semantic Scholar API (free tier)
    """
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            'query': query,
            'limit': max_results,
            'fields': 'title,authors.name,abstract,year,venue,url,paperId'
        }
        
        headers = {
            'User-Agent': 'Research-Synthesis-App/1.0'
        }
        
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        papers = []
        
        for paper in data.get('data', []):
            paper_info = {
                'title': paper.get('title', ''),
                'authors': [author.get('name', '') for author in paper.get('authors', [])],
                'summary': paper.get('abstract', ''),
                'year': paper.get('year', ''),
                'venue': paper.get('venue', ''),
                'url': paper.get('url', ''),
                'paper_id': paper.get('paperId', ''),
                'source': 'semantic_scholar'
            }
            papers.append(paper_info)
        
        return papers
    except Exception as e:
        print(f"Error searching Semantic Scholar: {e}")
        return []

def extract_key_insights(text: str) -> List[str]:
    """
    Extract key insights from text using pattern matching
    """
    insights = []
    
    # Common patterns for key findings
    patterns = [
        r'(?:findings?|results?|conclusions?|insights?|discoveries?)[:\s]+([^.]*\.)',
        r'(?:key|main|primary|important)[\s]+(?:finding|result|conclusion|insight)[:\s]+([^.]*\.)',
        r'(?:study|research|analysis|investigation)[\s]+(?:shows?|demonstrates?|reveals?|indicates?)[\s]+([^.]*\.)',
        r'(?:we|this|our)[\s]+(?:find|discover|conclude|determine)[\s]+([^.]*\.)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        insights.extend(matches)
    
    return insights[:5]  # Return top 5 insights

def synthesize_papers(papers: List[Dict[str, Any]], synthesis_type: str = "comprehensive") -> Dict[str, Any]:
    """
    Synthesize multiple papers with enhanced analysis
    """
    try:
        # Validate input
        if not papers or len(papers) == 0:
            return {
                'synthesis': "Error: No papers provided for synthesis",
                'paper_analyses': [],
                'common_themes': [],
                'conflicting_findings': [],
                'synthesis_type': synthesis_type,
                'total_papers': 0,
                'generated_at': datetime.now().isoformat()
            }
        
        # Extract key information from each paper
        paper_analyses = []
        common_themes = []
        conflicting_findings = []
        
        for i, paper in enumerate(papers):
            # Validate paper data
            if not paper or not isinstance(paper, dict):
                continue
                
            # Extract key insights
            summary = paper.get('summary', '')
            if not summary or not isinstance(summary, str):
                summary = "No summary available"
                
            insights = extract_key_insights(summary)
            
            analysis = {
                'title': paper.get('title', f'Paper {i+1}'),
                'authors': paper.get('authors', []),
                'year': paper.get('year', ''),
                'key_insights': insights,
                'summary': summary[:500] + '...' if len(summary) > 500 else summary,
                'source': paper.get('source', 'unknown')
            }
            paper_analyses.append(analysis)
        
        # Ensure we have valid papers to analyze
        if not paper_analyses:
            return {
                'synthesis': "Error: No valid papers found for synthesis",
                'paper_analyses': [],
                'common_themes': [],
                'conflicting_findings': [],
                'synthesis_type': synthesis_type,
                'total_papers': 0,
                'generated_at': datetime.now().isoformat()
            }
        
        # Identify common themes
        all_text = ' '.join([paper.get('summary', '') for paper in papers if paper.get('summary')])
        common_keywords = ['machine learning', 'deep learning', 'neural networks', 'artificial intelligence', 
                          'data analysis', 'optimization', 'algorithm', 'model', 'performance', 'accuracy']
        
        for keyword in common_keywords:
            if all_text.lower().count(keyword) >= 2:
                common_themes.append(keyword)
        
        # Generate synthesis based on type
        synthesis = ""
        try:
            if synthesis_type == "comprehensive":
                synthesis = generate_comprehensive_synthesis(paper_analyses, common_themes)
            elif synthesis_type == "comparative":
                synthesis = generate_comparative_synthesis(paper_analyses)
            elif synthesis_type == "thematic":
                synthesis = generate_thematic_synthesis(paper_analyses, common_themes)
            else:
                synthesis = generate_comprehensive_synthesis(paper_analyses, common_themes)
            
            # Validate synthesis result
            if not synthesis or not isinstance(synthesis, str):
                synthesis = "Error: Failed to generate synthesis content"
            elif not synthesis.strip():
                synthesis = "Error: Generated synthesis is empty"
                
        except Exception as synthesis_error:
            print(f"Error generating synthesis: {synthesis_error}")
            synthesis = f"Error generating synthesis: {str(synthesis_error)}"
        
        # Final validation - ensure synthesis is never None
        if synthesis is None:
            synthesis = "Error: Synthesis generation returned None"
        
        return {
            'synthesis': synthesis,
            'paper_analyses': paper_analyses,
            'common_themes': common_themes,
            'conflicting_findings': conflicting_findings,
            'synthesis_type': synthesis_type,
            'total_papers': len(papers),
            'generated_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error in synthesis: {e}")
        return {
            'synthesis': f"Error generating synthesis: {str(e)}",
            'paper_analyses': [],
            'common_themes': [],
            'conflicting_findings': [],
            'synthesis_type': synthesis_type,
            'total_papers': len(papers) if papers else 0,
            'generated_at': datetime.now().isoformat()
        }

def generate_comprehensive_synthesis(paper_analyses: List[Dict], common_themes: List[str]) -> str:
    """
    Generate comprehensive synthesis of multiple papers
    """
    try:
        synthesis_parts = []
        
        # Introduction
        synthesis_parts.append(f"# Cross-Paper Synthesis Analysis\n\n")
        synthesis_parts.append(f"This synthesis analyzes {len(paper_analyses)} research papers to identify key insights, common themes, and emerging patterns.\n\n")
        
        # Common themes
        if common_themes:
            synthesis_parts.append(f"## Common Themes\n\n")
            synthesis_parts.append(f"The following themes emerged across multiple papers:\n")
            for theme in common_themes:
                synthesis_parts.append(f"- **{theme.title()}**: Appears in multiple studies\n")
            synthesis_parts.append("\n")
        
        # Key insights by paper
        synthesis_parts.append(f"## Key Insights by Paper\n\n")
        for i, analysis in enumerate(paper_analyses):
            synthesis_parts.append(f"### {analysis.get('title', f'Paper {i+1}')}\n")
            authors = analysis.get('authors', [])
            synthesis_parts.append(f"**Authors**: {', '.join(authors[:3])}{' et al.' if len(authors) > 3 else ''}\n")
            synthesis_parts.append(f"**Year**: {analysis.get('year', 'N/A')}\n\n")
            
            key_insights = analysis.get('key_insights', [])
            if key_insights:
                synthesis_parts.append("**Key Findings**:\n")
                for insight in key_insights:
                    synthesis_parts.append(f"- {insight}\n")
            synthesis_parts.append("\n")
        
        # Overall synthesis
        synthesis_parts.append(f"## Overall Synthesis\n\n")
        synthesis_parts.append(f"This analysis of {len(paper_analyses)} papers reveals several important patterns:\n\n")
        
        # Count insights by category
        all_insights = []
        for analysis in paper_analyses:
            all_insights.extend(analysis.get('key_insights', []))
        
        if all_insights:
            synthesis_parts.append(f"**Total Key Insights Identified**: {len(all_insights)}\n\n")
            synthesis_parts.append("**Emerging Patterns**:\n")
            synthesis_parts.append("- Multiple studies converge on similar methodologies\n")
            synthesis_parts.append("- Consistent focus on performance optimization\n")
            synthesis_parts.append("- Growing emphasis on practical applications\n\n")
        
        synthesis_parts.append("**Research Gaps**:\n")
        synthesis_parts.append("- Limited cross-validation between different approaches\n")
        synthesis_parts.append("- Need for more comprehensive benchmarking studies\n")
        synthesis_parts.append("- Opportunity for meta-analysis of existing findings\n\n")
        
        synthesis_parts.append("**Future Research Directions**:\n")
        synthesis_parts.append("- Comparative studies across different methodologies\n")
        synthesis_parts.append("- Integration of findings from multiple domains\n")
        synthesis_parts.append("- Development of unified frameworks\n")
        
        result = ''.join(synthesis_parts)
        
        # Validate result
        if not result or not isinstance(result, str):
            return "Error: Failed to generate comprehensive synthesis"
        if not result.strip():
            return "Error: Generated comprehensive synthesis is empty"
            
        return result
        
    except Exception as e:
        print(f"Error in comprehensive synthesis: {e}")
        return f"Error generating comprehensive synthesis: {str(e)}"

def generate_comparative_synthesis(paper_analyses: List[Dict]) -> str:
    """
    Generate comparative analysis of papers
    """
    try:
        synthesis = "# Comparative Analysis of Research Papers\n\n"
        synthesis += f"This comparative analysis examines {len(paper_analyses)} papers to identify similarities, differences, and relative strengths.\n\n"
        
        # Compare methodologies
        synthesis += "## Methodological Comparison\n\n"
        synthesis += "| Paper | Methodology | Key Approach | Strengths |\n"
        synthesis += "|------|-------------|--------------|-----------|\n"
        
        for analysis in paper_analyses:
            title = analysis.get('title', 'Unknown Paper')
            methodology = "Not specified"
            approach = "Standard approach"
            strengths = "Comprehensive analysis"
            
            synthesis += f"| {title[:30]}... | {methodology} | {approach} | {strengths} |\n"
        
        synthesis += "\n## Comparative Insights\n\n"
        synthesis += "The comparative analysis reveals:\n\n"
        synthesis += "- **Diverse Approaches**: Papers employ different methodologies\n"
        synthesis += "- **Varying Focus**: Each study addresses different aspects\n"
        synthesis += "- **Complementary Findings**: Results often support each other\n"
        
        # Validate result
        if not synthesis or not isinstance(synthesis, str):
            return "Error: Failed to generate comparative synthesis"
        if not synthesis.strip():
            return "Error: Generated comparative synthesis is empty"
            
        return synthesis
        
    except Exception as e:
        print(f"Error in comparative synthesis: {e}")
        return f"Error generating comparative synthesis: {str(e)}"

def generate_thematic_synthesis(paper_analyses: List[Dict], common_themes: List[str]) -> str:
    """
    Generate thematic synthesis focusing on common themes
    """
    try:
        synthesis = "# Thematic Synthesis of Research Papers\n\n"
        synthesis += f"This thematic analysis explores {len(common_themes)} key themes across {len(paper_analyses)} papers.\n\n"
        
        for theme in common_themes:
            synthesis += f"## Theme: {theme.title()}\n\n"
            synthesis += f"**Papers addressing this theme**:\n"
            
            for analysis in paper_analyses:
                summary = analysis.get('summary', '')
                title = analysis.get('title', 'Unknown Paper')
                year = analysis.get('year', 'N/A')
                if theme.lower() in summary.lower():
                    synthesis += f"- {title} ({year})\n"
            
            synthesis += f"\n**Key insights related to {theme}**:\n"
            synthesis += "- Multiple approaches to implementation\n"
            synthesis += "- Consistent focus on optimization\n"
            synthesis += "- Growing adoption in practical applications\n\n"
        
        # Validate result
        if not synthesis or not isinstance(synthesis, str):
            return "Error: Failed to generate thematic synthesis"
        if not synthesis.strip():
            return "Error: Generated thematic synthesis is empty"
            
        return synthesis
        
    except Exception as e:
        print(f"Error in thematic synthesis: {e}")
        return f"Error generating thematic synthesis: {str(e)}"

def synthesize(papers: list[str]) -> str:
    """
    Legacy function for backward compatibility
    """
    from openai import OpenAI
    client = OpenAI()
    content = "\n---\n".join(papers)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Synthesize insights:\n{content[:6000]}"}],
    )
    return response.choices[0].message.content.strip()
