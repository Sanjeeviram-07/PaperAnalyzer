# Research Summary & Cross-Paper Synthesis System

A comprehensive research paper analysis and synthesis platform that combines multiple specialized agents to process, analyze, and generate insights from research papers with audio narration capabilities, using free APIs and pattern-based analysis.

[![🎬 Watch Demo Video](https://img.shields.io/badge/Watch%20Demo-Video-blue?logo=youtube)](https://www.linkedin.com/posts/sanjeevi-ram-274947298_research-ai-machinelearning-activity-7356616003222429697-zMPA?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEgK4LgBRFNRl7hTlEYfgJZUXGGuEqrFfTs)


---

## Screenshots

| Upload | Cross-Paper Synthesis |
|------------------|------------------------|
| ![Pdf Upload](PaperAnalyzer\Pdf.png) | ![Crosspaper Analysis](PaperAnalyzer\Cross_paper_analysis.png) |

| Audio Narration & Summary | Citation |
|------------------|------------------|
| ![Summary](PaperAnalyzer\Summary.png) | ![Cictation](PaperAnalyzer\Citation.png) |

## Features

- **Multi-Agent Paper Processing**: Specialized agents for parsing, classification, summarization, and synthesis
- **Cross-Paper Synthesis**: Advanced analysis across multiple research papers
- **Audio Generation**: Natural-sounding AI narration of research summaries
- **Multiple Input Sources**: PDF upload, URL analysis, DOI processing
- **Free API Integration**: arXiv and Semantic Scholar for paper discovery
- **Citation Management**: Automatic citation generation in multiple formats
- **Modern UI**: Responsive React frontend with Tailwind CSS
- **Real-time Processing**: Live analysis with progress indicators

## Architecture

### High-Level Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI Agents     │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Python)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    ┌─────────┐            ┌─────────┐            ┌─────────┐
    │ Tailwind│            │  Audio  │            │ Free    │
    │   CSS   │            │  Files  │            │ APIs    │
    └─────────┘            └─────────┘            └─────────┘
```

### Component Architecture

#### Frontend (React + TypeScript)
- **App.tsx**: Main application orchestrator
- **Components**: Modular UI components for each feature
- **State Management**: React hooks for local state
- **API Integration**: Axios for backend communication

#### Backend (FastAPI + Python)
- **Main API**: RESTful endpoints for paper processing
- **Agent Coordination**: Multi-agent system orchestration
- **File Management**: PDF processing and audio file handling
- **Error Handling**: Comprehensive error management

#### Specialized Agents (Python)
- **Parser Agent**: PDF text extraction and metadata parsing
- **Classifier Agent**: Topic classification and categorization
- **Summarizer Agent**: Pattern-based summary generation
- **Synthesizer Agent**: Cross-paper analysis using free APIs and pattern matching
- **Audio Agent**: Text-to-speech generation
- **Search Agent**: Paper discovery via arXiv and Semantic Scholar APIs

## Multi-Agent Design & Coordination

### Agent Architecture

The system employs a sophisticated multi-agent architecture where each agent specializes in specific tasks and coordinates through a centralized orchestrator, using free APIs and pattern-based analysis instead of expensive AI services.

#### Agent Responsibilities

| Agent | Primary Function | Input | Output |
|-------|-----------------|-------|--------|
| **Parser Agent** | Text extraction & metadata parsing | PDF files, URLs | Structured text, metadata |
| **Classifier Agent** | Topic classification | Text content | Categories, topics |
| **Summarizer Agent** | Summary generation | Text content | Pattern-based summaries |
| **Synthesizer Agent** | Cross-paper analysis | Multiple papers | Synthesis reports |
| **Audio Agent** | Text-to-speech | Summary text | Audio files (MP3) |
| **Search Agent** | Paper discovery | Search queries | Paper metadata |

#### Coordination Flow

```
1. Input Reception
   ↓
2. Parser Agent (Text Extraction)
   ↓
3. Classifier Agent (Topic Analysis)
   ↓
4. Summarizer Agent (Summary Generation)
   ↓
5. Audio Agent (Narration)
   ↓
6. Response Assembly
   ↓
7. Frontend Display
```

### Agent Communication

```python
# Example agent coordination
def process_paper(file: UploadFile, topics: str):
    # 1. Parser Agent
    paper_text = parser_agent.read_pdf(file)
    
    # 2. Classifier Agent
    classification = classifier_agent.classify(paper_text, topics)
    
    # 3. Summarizer Agent
    summary = summarizer_agent.generate_summary(paper_text)
    
    # 4. Audio Agent
    audio_path = audio_agent.generate_audio(summary)
    
    return {
        "summary": summary,
        "classification": classification,
        "audio": audio_path
    }
```

## 📄 Paper Processing Methodology

### Processing Pipeline

#### 1. Input Handling
- **PDF Upload**: Direct file upload with metadata extraction
- **URL Processing**: Web scraping for paper content
- **DOI Resolution**: Automatic DOI to URL conversion

#### 2. Text Extraction
```python
def extract_text(content: str) -> str:
    # Remove HTML tags
    # Extract main content
    # Clean formatting
    # Preserve structure
    return cleaned_text
```

#### 3. Metadata Parsing
- **Title Extraction**: Pattern matching and AI assistance
- **Author Identification**: Multiple pattern recognition
- **Year Detection**: Regex and context analysis
- **Journal/Conference**: Source identification

#### 4. Content Analysis
- **Topic Classification**: Multi-label classification
- **Key Insights Extraction**: Pattern-based analysis using regex
- **Citation Detection**: Reference identification
- **Free API Integration**: arXiv and Semantic Scholar for paper discovery

### Free API Integration

The system uses free APIs for paper discovery and analysis:

#### arXiv API
- **Endpoint**: `http://export.arxiv.org/api/query`
- **Features**: Free access to preprints and published papers
- **Rate Limits**: Generous limits for normal usage
- **Data**: Title, authors, abstract, PDF links, categories

#### Semantic Scholar API
- **Endpoint**: `https://api.semanticscholar.org/graph/v1/paper/search`
- **Features**: Academic paper database with citations
- **Rate Limits**: Free tier with generous limits
- **Data**: Title, authors, abstract, year, venue, citations

### Cross-Paper Synthesis

#### Synthesis Types

1. **Comprehensive Analysis**
   - Full cross-paper comparison
   - Common themes identification
   - Research gaps analysis

2. **Comparative Analysis**
   - Side-by-side methodology comparison
   - Performance metrics analysis
   - Strengths and weaknesses evaluation

3. **Thematic Analysis**
   - Theme-based paper grouping
   - Topic evolution tracking
   - Emerging trends identification

#### Synthesis Process

The synthesizer agent uses pattern-based analysis and free APIs:

```python
def synthesize_papers(papers: List[Dict], synthesis_type: str):
    # 1. Extract key insights using regex patterns
    insights = [extract_key_insights(paper) for paper in papers]
    
    # 2. Identify common themes using keyword analysis
    themes = identify_common_themes(papers)
    
    # 3. Generate synthesis using template-based approach
    if synthesis_type == "comprehensive":
        return generate_comprehensive_synthesis(papers, themes)
    elif synthesis_type == "comparative":
        return generate_comparative_synthesis(papers)
    else:
        return generate_thematic_synthesis(papers, themes)

def extract_key_insights(text: str) -> List[str]:
    """Extract insights using regex patterns"""
    patterns = [
        r'(?:findings?|results?|conclusions?|insights?|discoveries?)[:\s]+([^.]*\.)',
        r'(?:key|main|primary|important)[\s]+(?:finding|result|conclusion|insight)[:\s]+([^.]*\.)',
        r'(?:study|research|analysis|investigation)[\s]+(?:shows?|demonstrates?|reveals?|indicates?)[\s]+([^.]*\.)',
        r'(?:we|this|our)[\s]+(?:find|discover|conclude|determine)[\s]+([^.]*\.)'
    ]
    # Extract matches and return top insights
```

##  Audio Generation Implementation

### Text-to-Speech Pipeline

#### 1. Text Preprocessing
```python
def preprocess_text_for_audio(text: str) -> str:
    # Remove markdown formatting
    # Clean special characters
    # Optimize for speech
    # Add pauses for readability
    return processed_text
```

#### 2. Audio Generation
```python
def generate_audio(text: str) -> str:
    try:
        from gtts import gTTS
        
        # Create unique filename
        audio_filename = f"audio_{uuid.uuid4().hex}.mp3"
        
        # Generate audio using Google TTS
        tts = gTTS(text=text, lang='en')
        tts.save(audio_path)
        
        return audio_path
    except Exception as e:
        return ""  # Graceful fallback
```

#### 3. Audio Management
- **File Storage**: Organized in `data/` directory
- **Static Serving**: FastAPI static file serving
- **Cleanup**: Automatic old file cleanup
- **Error Handling**: Graceful fallbacks

### Audio Features

- **Natural Speech**: High-quality TTS with proper intonation
- **Multiple Formats**: MP3 output for broad compatibility
- **Download Support**: Direct audio file downloads
- **Progress Tracking**: Real-time generation status

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Internet connection (for free APIs)

### Backend Setup

1. **Clone and Navigate**
   ```bash
   cd backend
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # No API keys required - uses free APIs
   # System is ready to use immediately
   ```

5. **Start Backend Server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to Frontend**
   ```bash
   cd frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start Development Server**
   ```bash
   npm start
   ```

4. **Access Application**
   ```
   Frontend: http://localhost:3000
   Backend:  http://localhost:8000
   ```

### API Documentation

Once the backend is running, access the interactive API documentation:
```
http://localhost:8000/docs
```

##  Project Structure

```
Research/
├── backend/
│   ├── agents/
│   │   ├── audio_agent.py          # Text-to-speech generation
│   │   ├── classifier_agent.py     # Topic classification
│   │   ├── parser_agent.py         # PDF/text parsing
│   │   ├── search_agent.py         # Paper discovery
│   │   ├── summarizer_agent.py     # Summary generation
│   │   └── synthesizer_agent.py    # Cross-paper synthesis
│   ├── data/                       # Generated files storage
│   ├── main.py                     # FastAPI application
│   ├── config.py                   # Configuration settings
│   ├── utils.py                    # Utility functions
│   └── requirements.txt            # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── App.tsx             # Main application
│   │   │   ├── NavBar.tsx          # Navigation component
│   │   │   ├── UploadForm.tsx      # File upload interface
│   │   │   ├── SearchBar.tsx       # URL search interface
│   │   │   ├── DoiBar.tsx          # DOI search interface
│   │   │   ├── CrossPaperSynthesis.tsx # Synthesis interface
│   │   │   ├── SummaryViewer.tsx   # Results display
│   │   │   ├── CitationViewer.tsx  # Citation management
│   │   │   └── GenerationHistory.tsx # History management
│   │   ├── index.css               # Tailwind CSS + custom utilities
│   │   └── index.tsx               # React entry point
│   ├── package.json                # Node.js dependencies
│   └── tailwind.config.js          # Tailwind configuration
└── README.md                       # This file
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload/` | POST | Upload PDF for analysis |
| `/process-url/` | POST | Analyze paper from URL |
| `/process-doi/` | POST | Analyze paper from DOI |
| `/search-papers/` | POST | Search papers using APIs |
| `/synthesize-papers/` | POST | Generate cross-paper synthesis |
| `/health` | GET | Health check endpoint |

## Limitations

### Current Limitations

1. **File Size**: Maximum 10MB PDF files
2. **Processing Time**: Large papers may take 30-60 seconds
3. **Audio Quality**: Dependent on Google TTS service
4. **API Rate Limits**: Subject to arXiv and Semantic Scholar API limits
5. **Browser Support**: Requires modern browsers for full functionality
6. **Language Support**: Primarily English language support

### Technical Constraints

1. **Memory Usage**: Large papers require significant memory
2. **Concurrent Users**: Limited by server resources
3. **File Storage**: Local storage only (no cloud backup)
4. **Audio Storage**: Temporary storage, files may be cleaned up

## Future Improvements

### Planned Enhancements

#### 1. Performance Optimizations
- **Caching**: Redis-based caching for processed papers
- **Async Processing**: Background job queues for large files
- **CDN Integration**: Cloud storage for audio files
- **Database**: PostgreSQL for persistent storage

#### 2. Feature Enhancements
- **Multi-language Support**: Additional language processing
- **Advanced Synthesis**: More sophisticated cross-paper analysis
- **Citation Networks**: Visual citation relationship mapping
- **Collaborative Features**: User accounts and sharing

#### 3. Analysis Improvements
- **Enhanced Pattern Matching**: More sophisticated text analysis patterns
- **Better Classification**: More accurate topic classification
- **Enhanced Summaries**: More detailed and structured summaries
- **Audio Customization**: Voice selection and speed control

#### 4. User Experience
- **Real-time Collaboration**: Live editing and sharing
- **Advanced Search**: Semantic search capabilities
- **Export Options**: Multiple format exports (PDF, Word, etc.)
- **Mobile App**: Native mobile applications

#### 5. Infrastructure
- **Microservices**: Service-oriented architecture
- **Containerization**: Docker deployment
- **Cloud Deployment**: AWS/Azure/GCP integration
- **Monitoring**: Comprehensive logging and monitoring

### Research Directions

1. **Advanced Pattern Analysis**: Better understanding of research context
2. **Knowledge Graphs**: Building research knowledge networks
3. **Automated Review**: Pattern-based paper review generation
4. **Trend Analysis**: Research trend prediction and analysis

## Contributing

### Development Setup

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes**: Follow coding standards and add tests
4. **Test thoroughly**: Ensure all functionality works
5. **Submit pull request**: Detailed description of changes

### Code Standards

- **Python**: PEP 8 style guide
- **TypeScript**: ESLint configuration
- **React**: Functional components with hooks
- **Documentation**: Comprehensive docstrings and comments

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Google TTS**: For text-to-speech capabilities
- **arXiv API**: For free paper discovery and access
- **Semantic Scholar**: For free academic paper data
- **FastAPI**: For high-performance API framework
- **React**: For frontend framework
- **Tailwind CSS**: For utility-first CSS framework

## Support

For questions, issues, or contributions:

1. **Issues**: Create GitHub issues for bugs or feature requests
2. **Discussions**: Use GitHub Discussions for questions
3. **Email**: Contact maintainers for urgent issues

---

**Built for the research community** 
