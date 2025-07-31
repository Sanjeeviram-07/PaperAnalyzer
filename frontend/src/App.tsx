import React, { useState } from 'react';
import { FileText, Upload, Link, Hash, Brain, Headphones, Search, BookOpen, Zap, ArrowRight, CheckCircle, Play, Download, Share2, ExternalLink } from 'lucide-react';
import UploadForm from './components/UploadForm';
import SearchBar from './components/SearchBar';
import DoiBar from './components/DoiBar';
import CrossPaperSynthesis from './components/CrossPaperSynthesis';
import SummaryViewer from './components/SummaryViewer';
import NavBar from './components/NavBar';
import Footer from './components/Footer';
import GenerationHistory from './components/GenerationHistory';

interface DataType {
  summary: string;
  classification: string;
  audio: string;
  source_info?: any;
  citations?: any;
}

interface HistoryItem {
  id: string;
  type: 'upload' | 'url' | 'doi' | 'synthesis';
  title: string;
  source: string;
  timestamp: string;
  summary: string;
  classification: string;
  audio?: string;
  source_info?: any;
  citations?: any;
}

export default function App() {
  const [data, setData] = React.useState<DataType | null>(null);
  const [activeTab, setActiveTab] = useState<'upload' | 'url' | 'doi' | 'synthesis'>('upload');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showHistory, setShowHistory] = useState(false);

  const saveToHistory = (type: 'upload' | 'url' | 'doi' | 'synthesis', source: string, result: DataType) => {
    try {
      const historyItem: HistoryItem = {
        id: Date.now().toString(),
        type,
        title: result.source_info?.title || 'Research Paper',
        source,
        timestamp: new Date().toISOString(),
        summary: result.summary,
        classification: result.classification,
        audio: result.audio,
        source_info: result.source_info,
        citations: result.citations
      };

      const existingHistory = localStorage.getItem('paperAnalyzerHistory');
      const history = existingHistory ? JSON.parse(existingHistory) : [];
      
      // Add new item to the beginning
      history.unshift(historyItem);
      
      // Keep only the last 50 items
      const limitedHistory = history.slice(0, 50);
      
      localStorage.setItem('paperAnalyzerHistory', JSON.stringify(limitedHistory));
    } catch (error) {
      console.error('Error saving to history:', error);
    }
  };

  const handleDataUpdate = (newData: DataType, type: 'upload' | 'url' | 'doi' | 'synthesis', source: string) => {
    setData(newData);
    setIsAnalyzing(false);
    saveToHistory(type, source, newData);
  };

  const handleAnalysisStart = () => {
    setIsAnalyzing(true);
  };

  const resetToLanding = () => {
    setData(null);
    setIsAnalyzing(false);
  };

  const handleLoadHistoryItem = (item: HistoryItem) => {
    setData({
      summary: item.summary,
      classification: item.classification,
      audio: item.audio || '',
      source_info: item.source_info,
      citations: item.citations
    });
  };



  // If we have results, show the result page
  if (data) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900">
        <NavBar onReset={resetToLanding} showReset={true} onHistoryClick={() => setShowHistory(true)} />
        
        {/* Results Section */}
        <div className="max-w-7xl mx-auto px-6 py-8">
          <SummaryViewer data={data} />
        </div>
        
        <Footer />
        
        {/* Generation History Modal */}
        {showHistory && (
          <GenerationHistory
            onClose={() => setShowHistory(false)}
            onLoadItem={handleLoadHistoryItem}
          />
        )}
      </div>
    );
  }

  // Landing page
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900">
      <NavBar onReset={resetToLanding} showReset={false} onHistoryClick={() => setShowHistory(true)} />
      
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-6 py-20">
          <div className="text-center mb-16">
            <h1 className="text-6xl font-bold text-white mb-8 leading-tight">
              Summarize and Understand Research—<span className="text-teal-400">Instantly.</span>
            </h1>
            <p className="text-xl text-purple-200 max-w-3xl mx-auto mb-12 leading-relaxed">
              Upload papers or input links to generate summaries, trace citations, and listen to audio explanations.
            </p>
            
            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-16">
              <button
                onClick={() => document.getElementById('start-analysis')?.scrollIntoView({ behavior: 'smooth' })}
                className="bg-teal-500 hover:bg-teal-600 text-white px-8 py-4 rounded-full font-semibold text-lg transition-all duration-200 flex items-center space-x-2 shadow-lg hover:shadow-xl transform hover:scale-105"
              >
                <span>Get Started</span>
                <ArrowRight className="w-5 h-5" />
              </button>
              <button
                onClick={() => document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth' })}
                className="bg-white/10 backdrop-blur-md border border-white/20 text-white px-8 py-4 rounded-full font-semibold text-lg transition-all duration-200 flex items-center space-x-2 shadow-lg hover:shadow-xl transform hover:scale-105 hover:bg-white/20"
              >
                <span>Learn More</span>
                <ArrowRight className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 bg-purple-800/20">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-4xl font-bold text-white text-center mb-16">How PaperAnalyzer Works</h2>
          
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <Upload className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Upload or Paste</h3>
              <p className="text-purple-200">Choose PDF, URL, or DOI to get started with your research analysis.</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">AI Agents Analyze</h3>
              <p className="text-purple-200">Our multi-agent system extracts data and classifies topics intelligently.</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <BookOpen className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Get Smart Summaries</h3>
              <p className="text-purple-200">Read fast, listen to key insights, or explore synthesis across multiple papers.</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <CheckCircle className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Verify & Cite</h3>
              <p className="text-purple-200">Trace every claim back to its source with clean citations and references.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Highlights Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-4xl font-bold text-white text-center mb-16">What You Can Do With PaperAnalyzer</h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-purple-800/30 backdrop-blur-sm rounded-2xl p-8 border border-purple-600/30 hover:border-teal-400/50 transition-all duration-300">
              <div className="w-12 h-12 bg-teal-500 rounded-xl flex items-center justify-center mb-6">
                <Search className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Topic-based Research Search</h3>
              <p className="text-purple-200">Find and analyze papers by specific research topics and keywords.</p>
            </div>
            
            <div className="bg-purple-800/30 backdrop-blur-sm rounded-2xl p-8 border border-purple-600/30 hover:border-teal-400/50 transition-all duration-300">
              <div className="w-12 h-12 bg-teal-500 rounded-xl flex items-center justify-center mb-6">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Cross-paper Synthesis</h3>
              <p className="text-purple-200">Connect insights across multiple papers for comprehensive understanding.</p>
            </div>
            
            <div className="bg-purple-800/30 backdrop-blur-sm rounded-2xl p-8 border border-purple-600/30 hover:border-teal-400/50 transition-all duration-300">
              <div className="w-12 h-12 bg-teal-500 rounded-xl flex items-center justify-center mb-6">
                <Headphones className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Audio Summary Generator</h3>
              <p className="text-purple-200">Listen to research summaries with natural-sounding AI narration.</p>
            </div>
            
            <div className="bg-purple-800/30 backdrop-blur-sm rounded-2xl p-8 border border-purple-600/30 hover:border-teal-400/50 transition-all duration-300">
              <div className="w-12 h-12 bg-teal-500 rounded-xl flex items-center justify-center mb-6">
                <BookOpen className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Citation & Source Tracing</h3>
              <p className="text-purple-200">Track every claim back to its original source with proper citations.</p>
            </div>
            
            <div className="bg-purple-800/30 backdrop-blur-sm rounded-2xl p-8 border border-purple-600/30 hover:border-teal-400/50 transition-all duration-300">
              <div className="w-12 h-12 bg-teal-500 rounded-xl flex items-center justify-center mb-6">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Multi-Agent Paper Intelligence</h3>
              <p className="text-purple-200">Advanced AI agents work together to extract and analyze research content.</p>
            </div>
            
            <div className="bg-purple-800/30 backdrop-blur-sm rounded-2xl p-8 border border-purple-600/30 hover:border-teal-400/50 transition-all duration-300">
              <div className="w-12 h-12 bg-teal-500 rounded-xl flex items-center justify-center mb-6">
                <Download className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Export & Share</h3>
              <p className="text-purple-200">Download summaries, audio files, and citations in multiple formats.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Upload & Input Interface */}
      <section id="start-analysis" className="py-20 bg-purple-800/20">
        <div className="max-w-4xl mx-auto px-6">
          <h2 className="text-4xl font-bold text-white text-center mb-16">Start Your Analysis</h2>
          
          {/* Tab Navigation */}
          <div className="flex justify-center mb-8">
            <div className="bg-purple-800/30 backdrop-blur-sm rounded-xl p-2 border border-purple-600/30">
              <div className="flex space-x-2">
                <button
                  onClick={() => setActiveTab('upload')}
                  className={`px-6 py-3 rounded-lg font-semibold transition-all duration-200 ${
                    activeTab === 'upload'
                      ? 'bg-teal-500 text-white shadow-lg'
                      : 'text-purple-200 hover:text-white hover:bg-purple-700/50'
                  }`}
                >
                  Upload Paper
                </button>
                <button
                  onClick={() => setActiveTab('url')}
                  className={`px-6 py-3 rounded-lg font-semibold transition-all duration-200 ${
                    activeTab === 'url'
                      ? 'bg-teal-500 text-white shadow-lg'
                      : 'text-purple-200 hover:text-white hover:bg-purple-700/50'
                  }`}
                >
                  Analyze from URL
                </button>
                <button
                  onClick={() => setActiveTab('doi')}
                  className={`px-6 py-3 rounded-lg font-semibold transition-all duration-200 ${
                    activeTab === 'doi'
                      ? 'bg-teal-500 text-white shadow-lg'
                      : 'text-purple-200 hover:text-white hover:bg-purple-700/50'
                  }`}
                >
                  Analyze from DOI
                </button>
                <button
                  onClick={() => setActiveTab('synthesis')}
                  className={`px-6 py-3 rounded-lg font-semibold transition-all duration-200 ${
                    activeTab === 'synthesis'
                      ? 'bg-teal-500 text-white shadow-lg'
                      : 'text-purple-200 hover:text-white hover:bg-purple-700/50'
                  }`}
                >
                  Cross-Paper Synthesis
                </button>
              </div>
            </div>
          </div>

          {/* Active Panel */}
          <div className="bg-purple-800/30 backdrop-blur-sm rounded-2xl p-8 border border-purple-600/30">
            {activeTab === 'upload' && (
              <div id="upload-section">
                <h3 className="text-2xl font-semibold text-white mb-6 flex items-center">
                  <Upload className="w-6 h-6 mr-2 text-teal-400" />
                  Upload Research Paper
                </h3>
                <UploadForm 
                  setData={(data) => handleDataUpdate(data, 'upload', 'Uploaded File')} 
                  onAnalysisStart={handleAnalysisStart} 
                />
              </div>
            )}
            
            {activeTab === 'url' && (
              <div id="url-section">
                <h3 className="text-2xl font-semibold text-white mb-6 flex items-center">
                  <Link className="w-6 h-6 mr-2 text-teal-400" />
                  Analyze from URL
                </h3>
                <SearchBar 
                  setData={(data) => handleDataUpdate(data, 'url', 'URL Analysis')} 
                  onAnalysisStart={handleAnalysisStart} 
                />
              </div>
            )}
            
            {activeTab === 'doi' && (
              <div id="doi-section">
                <h3 className="text-2xl font-semibold text-white mb-6 flex items-center">
                  <Hash className="w-6 h-6 mr-2 text-teal-400" />
                  Analyze from DOI
                </h3>
                <DoiBar 
                  setData={(data) => handleDataUpdate(data, 'doi', 'DOI Analysis')} 
                  onAnalysisStart={handleAnalysisStart} 
                />
              </div>
            )}
            
            {activeTab === 'synthesis' && (
              <div id="synthesis-section">
                <h3 className="text-2xl font-semibold text-white mb-6 flex items-center">
                  <Brain className="w-6 h-6 mr-2 text-teal-400" />
                  Cross-Paper Synthesis
                </h3>
                <CrossPaperSynthesis 
                  setData={(data) => handleDataUpdate(data, 'synthesis', 'Cross-Paper Synthesis')} 
                  onAnalysisStart={handleAnalysisStart} 
                />
              </div>
            )}
          </div>

          {/* Processing State */}
          {isAnalyzing && (
            <div className="mt-8 bg-purple-800/30 backdrop-blur-sm rounded-2xl p-8 border border-purple-600/30">
              <div className="text-center">
                <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
                  <Brain className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">AI analyzing your research paper...</h3>
                <p className="text-purple-200">This may take a few moments</p>
                <div className="mt-6 bg-purple-700 rounded-lg p-4">
                  <div className="flex items-center justify-center">
                    <div className="w-6 h-6 border-2 border-teal-400 border-t-transparent rounded-full animate-spin mr-3"></div>
                    <span className="text-white text-sm">Processing and generating summary...</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </section>

      <Footer />
      
      {/* Generation History Modal */}
      {showHistory && (
        <GenerationHistory
          onClose={() => setShowHistory(false)}
          onLoadItem={handleLoadHistoryItem}
        />
      )}
    </div>
  );
}
