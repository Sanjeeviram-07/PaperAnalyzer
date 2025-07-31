import React, { useState } from 'react';
import axios from 'axios';
import { Link, FileText } from 'lucide-react';

interface SearchBarProps {
  setData: (data: any, source: string) => void;
  onAnalysisStart?: () => void;
}

export default function SearchBar({ setData, onAnalysisStart }: SearchBarProps) {
  const [url, setUrl] = useState("");
  const [topics, setTopics] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetch = async () => {
    if (!url.trim()) {
      setError("Please enter a URL");
      return;
    }

    setLoading(true);
    setError("");
    
    // Call onAnalysisStart if provided
    if (onAnalysisStart) {
      onAnalysisStart();
    }

    try {
      const form = new FormData();
      form.append("topics", topics);
      const res = await axios.post(`http://localhost:8000/process-url/?url=${url}`, form);
      setData(res.data, url);
    } catch (err: any) {
      console.error("Error:", err);
      setError(err.response?.data?.error || err.message || "Failed to process URL");
      setData({
        summary: "Error occurred while processing the paper",
        classification: "Error",
        audio: ""
      }, url);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="w-20 h-20 bg-gradient-to-br from-teal-400 to-teal-600 rounded-full flex items-center justify-center mx-auto mb-6 animate-pulse shadow-lg">
          <Link className="w-10 h-10 text-white" />
        </div>
        <h3 className="text-2xl font-bold text-white mb-3">Fetching and analyzing paper...</h3>
        <p className="text-purple-200 text-lg mb-8">This may take a few moments</p>
        <div className="max-w-md mx-auto bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
          <div className="flex items-center justify-between mb-4">
            <span className="text-white font-medium">Processing: {url}</span>
            <div className="w-6 h-6 border-2 border-teal-400 border-t-transparent rounded-full animate-spin"></div>
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
      {/* URL Input */}
      <div>
        <label className="block text-white font-bold text-lg mb-4">Paper URL</label>
        <div className="relative">
          <div className="absolute left-4 top-1/2 transform -translate-y-1/2 w-6 h-6 bg-gradient-to-br from-purple-400 to-purple-600 rounded-lg flex items-center justify-center">
            <Link className="w-4 h-4 text-white" />
          </div>
          <input
            type="url"
            placeholder="https://arxiv.org/abs/..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full pl-16 pr-6 py-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white placeholder-purple-300 focus:outline-none focus:border-teal-400 focus:ring-2 focus:ring-teal-400/20 transition-all duration-200 text-lg"
          />
        </div>
        <p className="text-purple-300 text-sm mt-3 flex items-center">
          <span className="w-2 h-2 bg-teal-400 rounded-full mr-2"></span>
          Supports arXiv, PubMed, and other academic sources
        </p>
      </div>

      {/* Topics Input */}
      <div>
        <label className="block text-white font-bold text-lg mb-4">Research Topics (Optional)</label>
        <input
          type="text"
          placeholder="e.g., Quantum Computing, Physics, Algorithms"
          value={topics}
          onChange={(e) => setTopics(e.target.value)}
          className="w-full px-6 py-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white placeholder-purple-300 focus:outline-none focus:border-teal-400 focus:ring-2 focus:ring-teal-400/20 transition-all duration-200 text-lg"
        />
        <p className="text-purple-300 text-sm mt-3 flex items-center">
          <span className="w-2 h-2 bg-teal-400 rounded-full mr-2"></span>
          Help us focus the analysis on specific areas
        </p>
      </div>

      {/* Process Button */}
      <button
        onClick={fetch}
        disabled={!url.trim() || loading}
        className="w-full bg-gradient-to-r from-teal-500 to-teal-600 hover:from-teal-400 hover:to-teal-500 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed text-white py-4 rounded-xl font-bold text-lg transition-all duration-200 flex items-center justify-center space-x-3 shadow-lg hover:shadow-xl transform hover:scale-[1.02] disabled:transform-none"
      >
        <FileText className="w-6 h-6" />
        <span>Analyze Paper</span>
      </button>

      {error && (
        <div className="p-6 bg-red-500/20 backdrop-blur-sm border border-red-400/30 rounded-xl">
          <p className="text-red-300 font-medium">{error}</p>
        </div>
      )}
    </div>
  );
}
  