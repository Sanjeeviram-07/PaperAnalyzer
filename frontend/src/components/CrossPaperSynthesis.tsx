import React, { useState } from 'react';
import axios from 'axios';
import { Search, FileText, Brain, Play, Download, ExternalLink, CheckCircle, Clock } from 'lucide-react';

interface Paper {
  title: string;
  authors: string[];
  summary: string;
  year?: string;
  venue?: string;
  url?: string;
  paper_id?: string;
  source: string;
  arxiv_id?: string;
  pdf_url?: string;
}

interface SynthesisResult {
  synthesis: string;
  paper_analyses: any[];
  common_themes: string[];
  conflicting_findings: string[];
  synthesis_type: string;
  total_papers: number;
  audio: string;
  generated_at: string;
}

interface CrossPaperSynthesisProps {
  setData: (data: any) => void;
  onAnalysisStart?: () => void;
}

export default function CrossPaperSynthesis({ setData, onAnalysisStart }: CrossPaperSynthesisProps) {
  const [query, setQuery] = useState('');
  const [source, setSource] = useState('both');
  const [maxResults, setMaxResults] = useState(10);
  const [papers, setPapers] = useState<Paper[]>([]);
  const [selectedPapers, setSelectedPapers] = useState<string[]>([]);
  const [synthesisType, setSynthesisType] = useState('comprehensive');
  const [loading, setLoading] = useState(false);
  const [searching, setSearching] = useState(false);
  const [synthesisResult, setSynthesisResult] = useState<SynthesisResult | null>(null);
  const [error, setError] = useState('');

  const searchPapers = async () => {
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    setSearching(true);
    setError('');
    setPapers([]);
    setSelectedPapers([]);

    try {
      const form = new FormData();
      form.append('query', query.trim());
      form.append('source', source);
      form.append('max_results', maxResults.toString());

      const response = await axios.post('http://localhost:8000/search-papers/', form);
      setPapers(response.data.papers);
    } catch (err: any) {
      console.error('Error searching papers:', err);
      setError(err.response?.data?.error || err.message || 'Failed to search papers');
    } finally {
      setSearching(false);
    }
  };

  const togglePaperSelection = (paperId: string) => {
    setSelectedPapers(prev => 
      prev.includes(paperId) 
        ? prev.filter(id => id !== paperId)
        : [...prev, paperId]
    );
  };

  const selectAllPapers = () => {
    const allIds = papers.map(paper => paper.paper_id || paper.arxiv_id || paper.title);
    setSelectedPapers(allIds);
  };

  const deselectAllPapers = () => {
    setSelectedPapers([]);
  };

  const generateSynthesis = async () => {
    if (selectedPapers.length < 2) {
      setError('Please select at least 2 papers for synthesis');
      return;
    }

    setLoading(true);
    setError('');
    
    if (onAnalysisStart) {
      onAnalysisStart();
    }

    try {
      const form = new FormData();
      form.append('paper_ids', selectedPapers.join(','));
      form.append('synthesis_type', synthesisType);
      form.append('query', query);

      const response = await axios.post('http://localhost:8000/synthesize-papers/', form);
      setSynthesisResult(response.data);
      
      // Debug response data
      console.log('Synthesis response:', {
        synthesis: response.data.synthesis ? 'Present' : 'Missing',
        synthesisLength: response.data.synthesis ? response.data.synthesis.length : 0,
        audio: response.data.audio ? 'Present' : 'Missing',
        audioPath: response.data.audio,
        paperAnalyses: response.data.paper_analyses ? response.data.paper_analyses.length : 0,
        totalPapers: response.data.total_papers
      });
      
      // Validate response data
      if (!response.data.synthesis) {
        throw new Error('No synthesis content received from server');
      }
      
      // Update the main app data
      setData({
        summary: response.data.synthesis,
        classification: `Cross-paper synthesis (${synthesisType})`,
        audio: response.data.audio || '',
        source_info: {
          title: `Cross-paper Synthesis: ${query}`,
          authors: ['AI Synthesis Engine'],
          year: new Date().getFullYear().toString(),
          journal: 'Research Synthesis',
          synthesis_type: synthesisType,
          total_papers: response.data.total_papers || 0
        },
        citations: {
          papers: response.data.paper_analyses || [],
          common_themes: response.data.common_themes || []
        }
      });
      
      // Debug setData call
      console.log('setData called with audio:', response.data.audio || '');
    } catch (err: any) {
      console.error('Error generating synthesis:', err);
      setError(err.response?.data?.error || err.message || 'Failed to generate synthesis');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="w-20 h-20 bg-gradient-to-br from-teal-400 to-teal-600 rounded-full flex items-center justify-center mx-auto mb-6 animate-pulse shadow-lg">
          <Brain className="w-10 h-10 text-white" />
        </div>
        <h3 className="text-2xl font-bold text-white mb-3">Generating cross-paper synthesis...</h3>
        <p className="text-purple-200 text-lg mb-8">This may take a few moments</p>
        <div className="max-w-md mx-auto bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
          <div className="flex items-center justify-center mb-4">
            <div className="w-6 h-6 border-2 border-teal-400 border-t-transparent rounded-full animate-spin mr-3"></div>
            <span className="text-white font-medium">Analyzing {selectedPapers.length} papers...</span>
          </div>
          <div className="w-full bg-purple-700/50 rounded-full h-2">
            <div className="bg-gradient-to-r from-teal-400 to-teal-600 h-2 rounded-full animate-pulse" style={{width: '60%'}}></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Search Section */}
      <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
        <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
          <Search className="w-6 h-6 mr-3 text-teal-400" />
          Search Research Papers
        </h3>
        
        <div className="grid md:grid-cols-3 gap-6 mb-6">
          <div>
            <label className="block text-white font-semibold mb-3">Search Query</label>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., machine learning, deep learning, neural networks"
              className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white placeholder-purple-300 focus:outline-none focus:border-teal-400 focus:ring-2 focus:ring-teal-400/20 transition-all duration-200"
            />
          </div>
          
          <div>
            <label className="block text-white font-semibold mb-3">Source</label>
            <select
              value={source}
              onChange={(e) => setSource(e.target.value)}
              className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white focus:outline-none focus:border-teal-400 focus:ring-2 focus:ring-teal-400/20 transition-all duration-200 appearance-none cursor-pointer relative z-10"
              style={{
                backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23ffffff' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e")`,
                backgroundPosition: 'right 0.75rem center',
                backgroundRepeat: 'no-repeat',
                backgroundSize: '1.5em 1.5em',
                paddingRight: '2.5rem'
              }}
            >
              <option value="both" className="bg-purple-800 text-white">Both (arXiv + Semantic Scholar)</option>
              <option value="arxiv" className="bg-purple-800 text-white">arXiv</option>
              <option value="semantic_scholar" className="bg-purple-800 text-white">Semantic Scholar</option>
            </select>
          </div>
          
          <div>
            <label className="block text-white font-semibold mb-3">Max Results</label>
            <select
              value={maxResults}
              onChange={(e) => setMaxResults(Number(e.target.value))}
              className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white focus:outline-none focus:border-teal-400 focus:ring-2 focus:ring-teal-400/20 transition-all duration-200 appearance-none cursor-pointer relative z-10"
              style={{
                backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23ffffff' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e")`,
                backgroundPosition: 'right 0.75rem center',
                backgroundRepeat: 'no-repeat',
                backgroundSize: '1.5em 1.5em',
                paddingRight: '2.5rem'
              }}
            >
              <option value={5} className="bg-purple-800 text-white">5 papers</option>
              <option value={10} className="bg-purple-800 text-white">10 papers</option>
              <option value={15} className="bg-purple-800 text-white">15 papers</option>
              <option value={20} className="bg-purple-800 text-white">20 papers</option>
            </select>
          </div>
        </div>
        
        <button
          onClick={searchPapers}
          disabled={!query.trim() || searching}
          className="w-full bg-gradient-to-r from-teal-500 to-teal-600 hover:from-teal-400 hover:to-teal-500 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed text-white py-4 rounded-xl font-bold text-lg transition-all duration-200 flex items-center justify-center space-x-3 shadow-lg hover:shadow-xl transform hover:scale-[1.02] disabled:transform-none"
        >
          <Search className="w-6 h-6" />
          <span>{searching ? 'Searching...' : 'Search Papers'}</span>
        </button>
      </div>

      {/* Papers List */}
      {papers.length > 0 && (
        <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-semibold text-white flex items-center">
              <FileText className="w-5 h-5 mr-2 text-teal-400" />
              Found Papers ({papers.length})
            </h3>
            <div className="flex space-x-2">
              <button
                onClick={selectAllPapers}
                className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-sm transition-all duration-200"
              >
                Select All
              </button>
              <button
                onClick={deselectAllPapers}
                className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-sm transition-all duration-200"
              >
                Deselect All
              </button>
            </div>
          </div>
          
          <div className="space-y-4 max-h-96 overflow-y-auto">
            {papers.map((paper, index) => {
              const paperId = paper.paper_id || paper.arxiv_id || paper.title;
              const isSelected = selectedPapers.includes(paperId);
              
              return (
                <div
                  key={index}
                  className={`p-4 rounded-lg border transition-all duration-200 cursor-pointer ${
                    isSelected
                      ? 'bg-teal-500/20 border-teal-400/50'
                      : 'bg-purple-700/30 border-purple-600/30 hover:border-purple-500/50'
                  }`}
                  onClick={() => togglePaperSelection(paperId)}
                >
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0 mt-1">
                      {isSelected ? (
                        <CheckCircle className="w-5 h-5 text-teal-400" />
                      ) : (
                        <div className="w-5 h-5 border-2 border-purple-400 rounded-full"></div>
                      )}
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <h4 className="text-white font-semibold mb-2 line-clamp-2">
                        {paper.title}
                      </h4>
                      
                      <div className="flex items-center space-x-4 text-sm text-purple-300 mb-2">
                        <span>{paper.authors.slice(0, 3).join(', ')}{paper.authors.length > 3 ? ' et al.' : ''}</span>
                        {paper.year && <span>{paper.year}</span>}
                        {paper.venue && <span>{paper.venue}</span>}
                        <span className="bg-purple-600 px-2 py-1 rounded text-xs">
                          {paper.source}
                        </span>
                      </div>
                      
                      <p className="text-purple-200 text-sm line-clamp-3">
                        {paper.summary}
                      </p>
                      
                      <div className="flex items-center space-x-2 mt-3">
                        {paper.url && (
                          <a
                            href={paper.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-teal-400 hover:text-teal-300 text-sm flex items-center space-x-1"
                            onClick={(e) => e.stopPropagation()}
                          >
                            <ExternalLink className="w-4 h-4" />
                            <span>View Paper</span>
                          </a>
                        )}
                        {paper.pdf_url && (
                          <a
                            href={paper.pdf_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-teal-400 hover:text-teal-300 text-sm flex items-center space-x-1"
                            onClick={(e) => e.stopPropagation()}
                          >
                            <Download className="w-4 h-4" />
                            <span>PDF</span>
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Synthesis Configuration */}
      {selectedPapers.length > 0 && (
        <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
          <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
            <Brain className="w-5 h-5 mr-2 text-teal-400" />
            Synthesis Configuration
          </h3>
          
          <div className="grid md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-white font-semibold mb-3">Synthesis Type</label>
              <select
                value={synthesisType}
                onChange={(e) => setSynthesisType(e.target.value)}
                className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white focus:outline-none focus:border-teal-400 focus:ring-2 focus:ring-teal-400/20 transition-all duration-200 appearance-none cursor-pointer relative z-10"
                style={{
                  backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23ffffff' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e")`,
                  backgroundPosition: 'right 0.75rem center',
                  backgroundRepeat: 'no-repeat',
                  backgroundSize: '1.5em 1.5em',
                  paddingRight: '2.5rem'
                }}
              >
                <option value="comprehensive" className="bg-purple-800 text-white">Comprehensive Analysis</option>
                <option value="comparative" className="bg-purple-800 text-white">Comparative Analysis</option>
                <option value="thematic" className="bg-purple-800 text-white">Thematic Analysis</option>
              </select>
            </div>
            
            <div>
              <label className="block text-white font-semibold mb-3">Selected Papers</label>
              <div className="px-4 py-3 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white">
                {selectedPapers.length} papers selected
              </div>
            </div>
          </div>
          
          <button
            onClick={generateSynthesis}
            className="w-full bg-gradient-to-r from-teal-500 to-teal-600 hover:from-teal-400 hover:to-teal-500 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed text-white py-4 rounded-xl font-bold text-lg transition-all duration-200 flex items-center justify-center space-x-3 shadow-lg hover:shadow-xl transform hover:scale-[1.02] disabled:transform-none"
          >
            <Brain className="w-5 h-5" />
            <span>Generate Cross-Paper Synthesis</span>
          </button>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-4">
          <p className="text-red-300">{error}</p>
        </div>
      )}
    </div>
  );
} 