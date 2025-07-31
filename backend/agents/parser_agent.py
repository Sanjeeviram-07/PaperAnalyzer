import io
import re
import os
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter

async def read_pdf(file):
    """Read PDF file with improved error handling and fallback methods"""
    try:
        contents = await file.read()
        
        # Save file to disk
        file_path = f"data/{file.filename}"
        os.makedirs("data", exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        # Try primary method: pdfminer high-level extraction
        try:
            text = extract_text(io.BytesIO(contents))
            if is_valid_text(text):
                print(f"Successfully extracted text using pdfminer high-level: {len(text)} characters")
                return text
        except Exception as e:
            print(f"Primary PDF extraction failed: {e}")
        
        # Fallback method: manual extraction with better error handling
        try:
            text = extract_text_manual(io.BytesIO(contents))
            if is_valid_text(text):
                print(f"Successfully extracted text using manual method: {len(text)} characters")
                return text
        except Exception as e:
            print(f"Manual PDF extraction failed: {e}")
        
        # Final fallback: return error message
        error_msg = "Unable to extract text from PDF. The file may be corrupted, password-protected, or contain only images."
        print(error_msg)
        return error_msg
        
    except Exception as e:
        error_msg = f"Error reading PDF file: {str(e)}"
        print(error_msg)
        return error_msg

def extract_text_manual(pdf_file):
    """Manual PDF text extraction with better error handling"""
    try:
        # Create resource manager
        rsrcmgr = PDFResourceManager()
        
        # Create string buffer for output
        retstr = io.StringIO()
        
        # Create text converter
        device = TextConverter(rsrcmgr, retstr, laparams=LAParams())
        
        # Create PDF parser and document
        parser = PDFParser(pdf_file)
        doc = PDFDocument(parser)
        
        # Process each page
        for page in PDFPage.create_pages(doc):
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            interpreter.process_page(page)
        
        # Get text and clean up
        text = retstr.getvalue()
        device.close()
        retstr.close()
        
        return text
        
    except Exception as e:
        print(f"Manual extraction error: {e}")
        return ""

def is_valid_text(text: str) -> bool:
    """Check if extracted text is valid and not garbled"""
    if not text or not isinstance(text, str):
        return False
    
    # Check for binary/garbled content
    if text.startswith('%PDF-1.') or text.startswith('%PDF-2.'):
        return False
    
    # Check for excessive binary characters
    binary_chars = sum(1 for c in text if ord(c) < 32 and c not in '\n\r\t')
    if binary_chars > len(text) * 0.1:  # More than 10% binary chars
        return False
    
    # Check for reasonable text length
    if len(text.strip()) < 50:
        return False
    
    # Check for printable character ratio
    printable_chars = sum(1 for c in text if c.isprintable() or c.isspace())
    if len(text) > 0 and printable_chars / len(text) < 0.8:
        return False
    
    return True

def extract_text(html_content: str) -> str:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

def extract_pdf_metadata(pdf_text: str) -> dict:
    """Extract metadata from PDF text content"""
    metadata = {
        'title': 'Unknown Title',
        'authors': ['Unknown Author'],
        'year': 'Unknown Year',
        'journal': 'Unknown Journal',
        'doi': '',
        'abstract': ''
    }
    
    try:
        # Split text into lines for easier processing
        lines = pdf_text.split('\n')
        
        # Look for title (usually in first few lines, often in caps or bold)
        for i, line in enumerate(lines[:20]):  # Check first 20 lines
            line = line.strip()
            if len(line) > 10 and len(line) < 200:
                # Check if line looks like a title (no numbers, reasonable length)
                if not re.search(r'^\d+\.', line) and not re.search(r'^[A-Z\s]+$', line):
                    # Avoid common non-title patterns
                    if not any(skip in line.lower() for skip in ['abstract', 'introduction', 'references', 'table', 'figure']):
                        metadata['title'] = line
                        break
        
        # Look for authors (common patterns)
        author_patterns = [
            r'by\s+([^,\n]+(?:,\s*[^,\n]+)*)',
            r'authors?:\s*([^,\n]+(?:,\s*[^,\n]+)*)',
            r'written by\s+([^,\n]+(?:,\s*[^,\n]+)*)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s*,\s*[A-Z][a-z]+\s+[A-Z][a-z]+)*)',
            r'([A-Z][a-z]+,\s*[A-Z]\.(?:\s*,\s*[A-Z][a-z]+,\s*[A-Z]\.)*)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+\s+and\s+[A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s*,\s*[A-Z][a-z]+\s+[A-Z][a-z]+)*\s+et al\.)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s*,\s*[A-Z][a-z]+\s+[A-Z][a-z]+)*\s+and\s+[A-Z][a-z]+\s+[A-Z][a-z]+)'
        ]
        
        for pattern in author_patterns:
            for line in lines[:50]:  # Check first 50 lines
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    authors_str = match.group(1).strip()
                    # Clean up authors
                    authors = []
                    for author in re.split(r',\s*|\sand\s+', authors_str):
                        author = author.strip()
                        # Remove common suffixes and prefixes
                        author = re.sub(r'\s+et al\.?$', '', author, flags=re.IGNORECASE)
                        author = re.sub(r'^\s*and\s+', '', author, flags=re.IGNORECASE)
                        
                        if (len(author) > 3 and 
                            not any(skip in author.lower() for skip in [
                                'university', 'department', 'institute', 'email', 'http', 'www',
                                'abstract', 'introduction', 'references', 'table', 'figure',
                                'unknown', 'anonymous', 'et al', 'and others', 'corresponding'
                            ]) and
                            not re.match(r'^\d+$', author) and  # Not just numbers
                            not re.match(r'^[A-Z\s]+$', author) and  # Not all caps
                            not re.match(r'^[a-z\s]+$', author)):  # Not all lowercase
                            authors.append(author)
                    
                    if authors:
                        metadata['authors'] = authors[:5]  # Limit to first 5 authors
                        break
            if metadata['authors'] != ['Unknown Author']:
                break
        
        # Look for year
        year_pattern = r'\b(19|20)\d{2}\b'
        for line in lines[:100]:  # Check first 100 lines
            year_match = re.search(year_pattern, line)
            if year_match:
                metadata['year'] = year_match.group()
                break
        
        # Look for journal name
        journal_patterns = [
            r'published in\s+([^,\n]+)',
            r'journal:\s*([^,\n]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Journal|Review|Letters|Proceedings))',
            r'([A-Z]+(?:\s+[A-Z]+)*\s+(?:Journal|Review|Letters|Proceedings))'
        ]
        
        for pattern in journal_patterns:
            for line in lines[:100]:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    journal = match.group(1).strip()
                    if len(journal) > 3 and len(journal) < 100:
                        metadata['journal'] = journal
                        break
            if metadata['journal'] != 'Unknown Journal':
                break
        
        # Look for DOI
        doi_pattern = r'10\.\d{4,}/[-._;()/:\w]+'
        doi_match = re.search(doi_pattern, pdf_text)
        if doi_match:
            metadata['doi'] = doi_match.group()
        
        # Look for abstract
        abstract_patterns = [
            r'abstract[:\s]*([^]*?)(?=\n\n|\n[A-Z]|introduction|keywords)',
            r'summary[:\s]*([^]*?)(?=\n\n|\n[A-Z])'
        ]
        
        for pattern in abstract_patterns:
            match = re.search(pattern, pdf_text, re.IGNORECASE | re.DOTALL)
            if match:
                abstract = match.group(1).strip()
                if len(abstract) > 50 and len(abstract) < 1000:
                    metadata['abstract'] = abstract
                    break
                    
    except Exception as e:
        print(f"Error extracting PDF metadata: {e}")
    
    return metadata
