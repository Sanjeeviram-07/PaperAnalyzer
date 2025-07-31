# backend/main.py
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from agents import (
    search_agent, parser_agent,
    classifier_agent, summarizer_agent,
    synthesizer_agent, audio_agent
)
import uuid
import traceback
import os
from datetime import datetime
import re

app = FastAPI(title="Research Summarization API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Allow both ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create data directory if it doesn't exist and mount static files
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
app.mount("/data", StaticFiles(directory=data_dir), name="data")

def extract_metadata_from_content(content: str, url: str = "") -> dict:
    """Extract metadata from paper content"""
    metadata = {
        'title': 'Unknown Title',
        'authors': ['Unknown Author'],
        'year': 'Unknown Year',
        'journal': 'Unknown Journal',
        'doi': '',
        'url': url
    }
    
    try:
        # Try to extract DOI from URL or content
        doi_pattern = r'10\.\d{4,}/[-._;()/:\w]+'
        doi_match = re.search(doi_pattern, url) or re.search(doi_pattern, content)
        if doi_match:
            metadata['doi'] = doi_match.group()
        
        # Try to extract title (look for common patterns)
        title_patterns = [
            r'<title[^>]*>(.*?)</title>',
            r'<h1[^>]*>(.*?)</h1>',
            r'"title":\s*"([^"]+)"',
            r'title:\s*([^\n]+)',
            r'<meta[^>]*name=["\']title["\'][^>]*content=["\']([^"\']+)["\']',
            r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match and match.group(1).strip():
                title = match.group(1).strip()
                # Clean up title
                title = re.sub(r'<[^>]+>', '', title)  # Remove HTML tags
                title = re.sub(r'&[a-zA-Z]+;', ' ', title)  # Replace HTML entities
                if len(title) > 10 and len(title) < 200:  # Reasonable title length
                    metadata['title'] = title
                    break
        
        # Try to extract year
        year_pattern = r'\b(19|20)\d{2}\b'
        year_match = re.search(year_pattern, content)
        if year_match:
            metadata['year'] = year_match.group()
        
        # Enhanced author extraction with multiple strategies
        authors = extract_authors_enhanced(content)
        if authors:
            metadata['authors'] = authors
            print(f"Extracted authors: {authors}")
        else:
            print("No authors extracted, using default")
        
        # Try to extract journal name
        journal_patterns = [
            r'"journal":\s*"([^"]+)"',
            r'journal:\s*([^\n]+)',
            r'published in\s+([^,\n]+)',
            r'<meta[^>]*name=["\']citation_journal_title["\'][^>]*content=["\']([^"\']+)["\']',
            r'<meta[^>]*name=["\']citation_publication["\'][^>]*content=["\']([^"\']+)["\']'
        ]
        
        for pattern in journal_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                journal = match.group(1).strip()
                if len(journal) > 3 and len(journal) < 100:
                    metadata['journal'] = journal
                    break
                    
    except Exception as e:
        print(f"Error extracting metadata: {e}")
    
    return metadata

def extract_authors_enhanced(content: str) -> list:
    """Enhanced author extraction with multiple strategies"""
    authors = []
    
    try:
        print("Starting enhanced author extraction...")
        
        # Strategy 1: JSON-LD structured data
        json_ld_pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
        json_ld_matches = re.findall(json_ld_pattern, content, re.DOTALL | re.IGNORECASE)
        
        for json_ld in json_ld_matches:
            try:
                import json
                data = json.loads(json_ld)
                if isinstance(data, dict):
                    # Handle different JSON-LD structures
                    if 'author' in data:
                        author_data = data['author']
                        if isinstance(author_data, list):
                            for author in author_data:
                                if isinstance(author, dict) and 'name' in author:
                                    authors.append(author['name'])
                        elif isinstance(author_data, dict) and 'name' in author_data:
                            authors.append(author_data['name'])
                    elif '@graph' in data:
                        for item in data['@graph']:
                            if isinstance(item, dict) and item.get('@type') == 'Person' and 'name' in item:
                                authors.append(item['name'])
            except json.JSONDecodeError:
                continue
        
        if authors:
            print(f"Strategy 1 (JSON-LD) found authors: {authors}")
        
        # Strategy 2: Meta tags
        meta_author_patterns = [
            r'<meta[^>]*name=["\']author["\'][^>]*content=["\']([^"\']+)["\']',
            r'<meta[^>]*name=["\']citation_author["\'][^>]*content=["\']([^"\']+)["\']',
            r'<meta[^>]*name=["\']dc\.creator["\'][^>]*content=["\']([^"\']+)["\']',
            r'<meta[^>]*property=["\']article:author["\'][^>]*content=["\']([^"\']+)["\']'
        ]
        
        meta_authors = []
        for pattern in meta_author_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if match.strip():
                    meta_authors.extend([author.strip() for author in match.split(',')])
        
        if meta_authors:
            authors.extend(meta_authors)
            print(f"Strategy 2 (Meta tags) found authors: {meta_authors}")
        
        # Strategy 3: JSON patterns in content
        json_author_patterns = [
            r'"author":\s*\[(.*?)\]',
            r'"authors":\s*\[(.*?)\]',
            r'"creator":\s*\[(.*?)\]',
            r'"authors?":\s*"([^"]+)"',
            r'"author":\s*"([^"]+)"'
        ]
        
        json_authors = []
        for pattern in json_author_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                authors_str = match.group(1).strip()
                # Handle both array and string formats
                if authors_str.startswith('"') or not authors_str.startswith('['):
                    # String format
                    json_authors.extend([author.strip().strip('"\'') for author in authors_str.split(',')])
                else:
                    # Array format
                    authors_str = authors_str.strip('[]')
                    json_authors.extend([author.strip().strip('"\'') for author in authors_str.split(',')])
        
        if json_authors:
            authors.extend(json_authors)
            print(f"Strategy 3 (JSON patterns) found authors: {json_authors}")
        
        # Strategy 4: Text-based patterns
        text_author_patterns = [
            r'authors?:\s*([^,\n]+(?:,\s*[^,\n]+)*)',
            r'by\s+([^,\n]+(?:,\s*[^,\n]+)*)',
            r'written by\s+([^,\n]+(?:,\s*[^,\n]+)*)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s*,\s*[A-Z][a-z]+\s+[A-Z][a-z]+)*)',
            r'([A-Z][a-z]+,\s*[A-Z]\.(?:\s*,\s*[A-Z][a-z]+,\s*[A-Z]\.)*)'
        ]
        
        text_authors = []
        for pattern in text_author_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                authors_str = match.group(1).strip()
                # Clean up authors string
                potential_authors = [author.strip().strip('"\'') for author in authors_str.split(',')]
                for author in potential_authors:
                    if len(author) > 3 and not any(skip in author.lower() for skip in [
                        'university', 'department', 'institute', 'email', 'http', 'www', 
                        'abstract', 'introduction', 'references', 'table', 'figure'
                    ]):
                        text_authors.append(author)
        
        if text_authors:
            authors.extend(text_authors)
            print(f"Strategy 4 (Text patterns) found authors: {text_authors}")
        
        # Strategy 5: HTML structure patterns
        html_author_patterns = [
            r'<span[^>]*class=["\'][^"\']*author[^"\']*["\'][^>]*>(.*?)</span>',
            r'<div[^>]*class=["\'][^"\']*author[^"\']*["\'][^>]*>(.*?)</div>',
            r'<p[^>]*class=["\'][^"\']*author[^"\']*["\'][^>]*>(.*?)</p>'
        ]
        
        html_authors = []
        for pattern in html_author_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Clean HTML tags
                clean_text = re.sub(r'<[^>]+>', '', match)
                if clean_text.strip():
                    html_authors.extend([author.strip() for author in clean_text.split(',')])
        
        if html_authors:
            authors.extend(html_authors)
            print(f"Strategy 5 (HTML structure) found authors: {html_authors}")
        
        # Clean and validate authors
        cleaned_authors = []
        for author in authors:
            author = author.strip()
            # Remove HTML entities and tags
            author = re.sub(r'<[^>]+>', '', author)
            author = re.sub(r'&[a-zA-Z]+;', ' ', author)
            author = re.sub(r'\s+', ' ', author)
            
            # Validation criteria
            if (len(author) > 2 and 
                len(author) < 100 and 
                not any(skip in author.lower() for skip in [
                    'university', 'department', 'institute', 'email', 'http', 'www',
                    'abstract', 'introduction', 'references', 'table', 'figure',
                    'unknown', 'anonymous', 'et al', 'and others'
                ]) and
                not re.match(r'^\d+$', author) and  # Not just numbers
                not re.match(r'^[A-Z\s]+$', author) and  # Not all caps
                author not in cleaned_authors):  # No duplicates
                cleaned_authors.append(author)
        
        print(f"Final cleaned authors: {cleaned_authors}")
        
        # Limit to first 5 authors and return
        return cleaned_authors[:5] if cleaned_authors else []
        
    except Exception as e:
        print(f"Error in enhanced author extraction: {e}")
        return []

def generate_citation(source_info, citation_type="apa"):
    """Generate citations in different formats"""
    if not source_info:
        return {}
    
    title = source_info.get('title', 'Unknown Title')
    authors = source_info.get('authors', ['Unknown Author'])
    year = source_info.get('year', 'Unknown Year')
    journal = source_info.get('journal', 'Unknown Journal')
    doi = source_info.get('doi', '')
    url = source_info.get('url', '')
    
    citations = {}
    
    # APA Format
    if citation_type == "apa" or citation_type == "all":
        author_str = ", ".join(authors) if len(authors) <= 2 else f"{authors[0]} et al."
        citations["apa"] = f"{author_str}. ({year}). {title}. {journal}."
        if doi:
            citations["apa"] += f" https://doi.org/{doi}"
    
    # MLA Format
    if citation_type == "mla" or citation_type == "all":
        author_str = ", ".join(authors) if len(authors) <= 2 else f"{authors[0]} et al."
        citations["mla"] = f"{author_str}. \"{title}.\" {journal}, {year}."
        if doi:
            citations["mla"] += f" doi:{doi}"
    
    # Chicago Format
    if citation_type == "chicago" or citation_type == "all":
        author_str = ", ".join(authors) if len(authors) <= 2 else f"{authors[0]} et al."
        citations["chicago"] = f"{author_str}. \"{title}.\" {journal} ({year})."
        if doi:
            citations["chicago"] += f" https://doi.org/{doi}"
    
    # BibTeX Format
    if citation_type == "bibtex" or citation_type == "all":
        bibtex_id = f"{authors[0].split()[-1].lower()}{year}" if authors and authors[0] else "unknown"
        citations["bibtex"] = f"""@article{{{bibtex_id},
  title={{{title}}},
  author={{{" and ".join(authors)}}},
  journal={{{journal}}},
  year={{{year}}},
  doi={{{doi}}}
}}"""
    
    return citations

@app.get("/")
async def ping():
    return {
        "message": "Research Summarization System Running",
        "version": "1.0.0",
        "summarization": "BART (Hugging Face)",
        "status": "ready"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "data_directory": os.path.exists(data_dir),
        "audio_files": len([f for f in os.listdir(data_dir) if f.endswith('.mp3')]) if os.path.exists(data_dir) else 0
    }

@app.post("/process-url/")
async def process_url(url: str, topics: str = Form(...)):
    try:
        paper_content = search_agent.fetch_paper(url)
        parsed = parser_agent.extract_text(paper_content)
        classification = classifier_agent.classify(parsed, topics.split(","))
        summary = summarizer_agent.generate_summary(parsed)
        audio_path = audio_agent.generate_audio(summary)
        
        # Extract source information
        source_info = extract_metadata_from_content(paper_content, url)
        source_info['access_date'] = datetime.now().strftime("%Y-%m-%d")
        
        # Generate citations
        citations = generate_citation(source_info, "all")
        
        # Verify audio file was created
        audio_file_path = os.path.join(data_dir, audio_path.replace("data/", ""))
        if not os.path.exists(audio_file_path):
            print(f"Warning: Audio file not found at {audio_file_path}")
            audio_path = ""
        
        return {
            "summary": summary,
            "classification": classification,
            "audio": audio_path,
            "source_info": source_info,
            "citations": citations
        }
    except Exception as e:
        error_msg = f"Error processing URL: {str(e)}"
        print(f"Error: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "error": error_msg,
                "summary": "Error occurred while processing the paper",
                "classification": "Error",
                "audio": "",
                "source_info": {},
                "citations": {}
            }
        )

@app.post("/search-papers/")
async def search_papers(query: str = Form(...), source: str = Form("arxiv"), max_results: int = Form(10)):
    """Search for papers using free APIs"""
    try:
        if source.lower() == "arxiv":
            papers = synthesizer_agent.search_arxiv_papers(query, max_results)
        elif source.lower() == "semantic_scholar":
            papers = synthesizer_agent.search_semantic_scholar_papers(query, max_results)
        else:
            # Try both sources
            arxiv_papers = synthesizer_agent.search_arxiv_papers(query, max_results // 2)
            semantic_papers = synthesizer_agent.search_semantic_scholar_papers(query, max_results // 2)
            papers = arxiv_papers + semantic_papers
        
        return {
            "papers": papers,
            "query": query,
            "source": source,
            "total_found": len(papers)
        }
    except Exception as e:
        error_msg = f"Error searching papers: {str(e)}"
        print(f"Error: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "error": error_msg,
                "papers": [],
                "query": query,
                "source": source,
                "total_found": 0
            }
        )

@app.post("/synthesize-papers/")
async def synthesize_papers_endpoint(
    paper_ids: str = Form(...), 
    synthesis_type: str = Form("comprehensive"),
    query: str = Form("")
):
    """Synthesize multiple papers"""
    try:
        # Parse paper IDs (comma-separated)
        paper_id_list = [pid.strip() for pid in paper_ids.split(",") if pid.strip()]
        
        # For now, we'll use the query to search for papers and synthesize them
        # In a full implementation, you'd store paper data and retrieve by IDs
        if query:
            # Search for papers using the query
            papers = synthesizer_agent.search_arxiv_papers(query, len(paper_id_list) or 5)
            papers.extend(synthesizer_agent.search_semantic_scholar_papers(query, len(paper_id_list) or 5))
        else:
            # Use dummy data for demonstration
            papers = [
                {
                    'title': 'Sample Research Paper 1',
                    'authors': ['Author A', 'Author B'],
                    'summary': 'This paper discusses machine learning approaches for data analysis.',
                    'year': '2023',
                    'source': 'arxiv'
                },
                {
                    'title': 'Sample Research Paper 2', 
                    'authors': ['Author C', 'Author D'],
                    'summary': 'This research explores deep learning methods and their applications.',
                    'year': '2023',
                    'source': 'semantic_scholar'
                }
            ]
        
        # Generate synthesis
        synthesis_result = synthesizer_agent.synthesize_papers(papers, synthesis_type)
        
        # Validate synthesis result
        if not synthesis_result or not synthesis_result.get('synthesis'):
            raise Exception("Failed to generate synthesis content")
        
        synthesis_text = synthesis_result['synthesis']
        if not isinstance(synthesis_text, str) or not synthesis_text.strip():
            raise Exception("Generated synthesis is empty or invalid")
        
        # Additional validation to prevent NoneType errors
        if synthesis_text is None:
            synthesis_text = "Error: Synthesis generation returned None"
        elif not synthesis_text.strip():
            synthesis_text = "Error: Generated synthesis is empty"
        
        # Generate audio for the synthesis
        audio_path = ""
        try:
            if synthesis_text and synthesis_text.strip() and not synthesis_text.startswith("Error:"):
                print(f"Generating audio for synthesis (length: {len(synthesis_text)} characters)")
                print(f"Synthesis preview: {synthesis_text[:200]}...")
                
                # Truncate synthesis for audio if it's too long
                audio_text = synthesis_text
                if len(audio_text) > 3000:
                    # Take the first part and add a note
                    audio_text = synthesis_text[:3000] + "\n\n[Audio truncated due to length]"
                    print(f"Truncated synthesis for audio generation to {len(audio_text)} characters")
                
                audio_path = audio_agent.generate_audio(audio_text)
                print(f"Audio generated successfully: {audio_path}")
                
                # Verify audio file was created
                if audio_path:
                    audio_file_path = os.path.join(data_dir, audio_path.replace("data/", ""))
                    if not os.path.exists(audio_file_path):
                        print(f"Warning: Audio file not found at {audio_file_path}")
                        audio_path = ""
                    else:
                        print(f"Audio file verified at {audio_file_path}")
                else:
                    print("Audio generation returned empty path")
            else:
                print(f"Skipping audio generation for error synthesis: {synthesis_text[:100]}...")
        except Exception as audio_error:
            print(f"Audio generation failed: {audio_error}")
            print(f"Audio error traceback: {traceback.format_exc()}")
            audio_path = ""
        
        return {
            "synthesis": synthesis_result['synthesis'],
            "paper_analyses": synthesis_result['paper_analyses'],
            "common_themes": synthesis_result['common_themes'],
            "conflicting_findings": synthesis_result['conflicting_findings'],
            "synthesis_type": synthesis_result['synthesis_type'],
            "total_papers": synthesis_result['total_papers'],
            "audio": audio_path,
            "generated_at": synthesis_result['generated_at']
        }
    except Exception as e:
        error_msg = f"Error synthesizing papers: {str(e)}"
        print(f"Error: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "error": error_msg,
                "synthesis": "Error occurred while synthesizing papers",
                "paper_analyses": [],
                "common_themes": [],
                "conflicting_findings": [],
                "synthesis_type": synthesis_type,
                "total_papers": 0,
                "audio": "",
                "generated_at": datetime.now().isoformat()
            }
        )

@app.post("/process-doi/")
async def process_doi(doi: str = Form(...), topics: str = Form(...)):
    try:
        # Convert DOI to URL
        doi_url = f"https://doi.org/{doi.strip()}"
        print(f"Processing DOI: {doi} -> URL: {doi_url}")
        
        # Fetch paper from DOI URL
        paper_content = search_agent.fetch_paper(doi_url)
        parsed = parser_agent.extract_text(paper_content)
        classification = classifier_agent.classify(parsed, topics.split(","))
        summary = summarizer_agent.generate_summary(parsed)
        audio_path = audio_agent.generate_audio(summary)
        
        # Extract source information
        source_info = extract_metadata_from_content(paper_content, doi_url)
        source_info['doi'] = doi.strip()
        source_info['access_date'] = datetime.now().strftime("%Y-%m-%d")
        
        # Generate citations
        citations = generate_citation(source_info, "all")
        
        # Verify audio file was created
        audio_file_path = os.path.join(data_dir, audio_path.replace("data/", ""))
        if not os.path.exists(audio_file_path):
            print(f"Warning: Audio file not found at {audio_file_path}")
            audio_path = ""
        
        return {
            "summary": summary,
            "classification": classification,
            "audio": audio_path,
            "source_info": source_info,
            "citations": citations
        }
    except Exception as e:
        error_msg = f"Error processing DOI: {str(e)}"
        print(f"Error: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "error": error_msg,
                "summary": "Error occurred while processing the DOI",
                "classification": "Error",
                "audio": "",
                "source_info": {},
                "citations": {}
            }
        )

@app.post("/upload/")
async def upload_paper(file: UploadFile, topics: str = Form(...)):
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Only PDF files are supported",
                    "summary": "Please upload a valid PDF file",
                    "classification": "Error",
                    "audio": "",
                    "source_info": {},
                    "citations": {}
                }
            )
        
        paper_text = await parser_agent.read_pdf(file)
        
        # Check if PDF parsing was successful
        if paper_text.startswith("Error:") or paper_text.startswith("Unable to extract"):
            return JSONResponse(
                status_code=400,
                content={
                    "error": paper_text,
                    "summary": "PDF processing failed",
                    "classification": "Error",
                    "audio": "",
                    "source_info": {},
                    "citations": {}
                }
            )
        
        classification = classifier_agent.classify(paper_text, topics.split(","))
        summary = summarizer_agent.generate_summary(paper_text)
        print(f"Generated summary: {summary[:100]}...")
        
        audio_path = audio_agent.generate_audio(summary)
        print(f"Audio generation result: {audio_path}")
        
        # Extract metadata from PDF content
        pdf_metadata = parser_agent.extract_pdf_metadata(paper_text)
        
        # Create source information with extracted metadata
        source_info = {
            'filename': file.filename,
            'title': pdf_metadata.get('title', 'Uploaded Document'),
            'authors': pdf_metadata.get('authors', ['Unknown Author']),
            'year': pdf_metadata.get('year', 'Unknown Year'),
            'journal': pdf_metadata.get('journal', 'Uploaded Document'),
            'doi': pdf_metadata.get('doi', ''),
            'access_date': datetime.now().strftime("%Y-%m-%d"),
            'file_size': file.size if hasattr(file, 'size') else 'Unknown'
        }
        
        # Generate citations
        citations = generate_citation(source_info, "all")
        
        # Verify audio file was created
        if audio_path:
            audio_file_path = os.path.join(data_dir, audio_path.replace("data/", ""))
            if not os.path.exists(audio_file_path):
                print(f"Warning: Audio file not found at {audio_file_path}")
                audio_path = ""
            else:
                print(f"Audio file verified at: {audio_file_path}")
        else:
            print("No audio path returned from audio generation")
        
        return {
            "summary": summary,
            "classification": classification,
            "audio": audio_path,
            "source_info": source_info,
            "citations": citations
        }
    except Exception as e:
        error_msg = f"Error processing uploaded file: {str(e)}"
        print(f"Error: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "error": error_msg,
                "summary": "Error occurred while processing the uploaded file",
                "classification": "Error",
                "audio": "",
                "source_info": {},
                "citations": {}
            }
        )
