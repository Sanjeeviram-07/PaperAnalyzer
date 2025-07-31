import React, { useState, useEffect } from 'react';
import { FileText, Link, Hash, Clock, ExternalLink, Play, Download, X } from 'lucide-react';

interface HistoryItem {
  id: string;
  type: 'upload' | 'url' | 'doi';
  title: string;
  source: string;
  timestamp: string;
  summary: string;
  classification: string;
  audio?: string;
  source_info?: any;
  citations?: any;
}

interface GenerationHistoryProps {
  onClose: () => void;
  onLoadItem: (item: HistoryItem) => void;
}

export default function GenerationHistory({ onClose, onLoadItem }: GenerationHistoryProps) {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load history from localStorage
    const loadHistory = () => {
      try {
        const savedHistory = localStorage.getItem('paperAnalyzerHistory');
        if (savedHistory) {
          setHistory(JSON.parse(savedHistory));
        }
      } catch (error) {
        console.error('Error loading history:', error);
      } finally {
        setLoading(false);
      }
    };

    loadHistory();
  }, []);

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'upload':
        return <FileText className="w-4 h-4" />;
      case 'url':
        return <Link className="w-4 h-4" />;
      case 'doi':
        return <Hash className="w-4 h-4" />;
      default:
        return <FileText className="w-4 h-4" />;
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'upload':
        return 'Uploaded Paper';
      case 'url':
        return 'URL Analysis';
      case 'doi':
        return 'DOI Analysis';
      default:
        return 'Paper';
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) {
      return 'Just now';
    } else if (diffInHours < 24) {
      return `${diffInHours} hour${diffInHours > 1 ? 's' : ''} ago`;
    } else {
      const diffInDays = Math.floor(diffInHours / 24);
      return `${diffInDays} day${diffInDays > 1 ? 's' : ''} ago`;
    }
  };

  const handleLoadItem = (item: HistoryItem) => {
    onLoadItem(item);
    onClose();
  };

  const clearHistory = () => {
    if (window.confirm('Are you sure you want to clear all history?')) {
      localStorage.removeItem('paperAnalyzerHistory');
      setHistory([]);
    }
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
        <div className="bg-purple-800/90 backdrop-blur-sm rounded-2xl p-8 border border-purple-600/30 max-w-4xl w-full mx-4 max-h-[80vh] overflow-hidden">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-white">Generation History</h2>
            <button
              onClick={onClose}
              className="text-purple-300 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
          <div className="flex items-center justify-center py-12">
            <div className="w-8 h-8 border-2 border-teal-400 border-t-transparent rounded-full animate-spin"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="bg-purple-800/90 backdrop-blur-sm rounded-2xl p-8 border border-purple-600/30 max-w-4xl w-full mx-4 max-h-[80vh] overflow-hidden">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Generation History</h2>
          <div className="flex items-center space-x-3">
            {history.length > 0 && (
              <button
                onClick={clearHistory}
                className="text-purple-300 hover:text-red-400 transition-colors text-sm"
              >
                Clear History
              </button>
            )}
            <button
              onClick={onClose}
              className="text-purple-300 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        <div className="overflow-y-auto max-h-[calc(80vh-120px)]">
          {history.length === 0 ? (
            <div className="text-center py-12">
              <FileText className="w-16 h-16 text-purple-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">No History Yet</h3>
              <p className="text-purple-300">
                Your analyzed papers will appear here for easy access.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {history.map((item) => (
                <div
                  key={item.id}
                  className="bg-purple-700/50 rounded-xl p-6 border border-purple-600/30 hover:border-teal-400/50 transition-all duration-200 cursor-pointer"
                  onClick={() => handleLoadItem(item)}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-teal-500 rounded-lg flex items-center justify-center">
                        {getTypeIcon(item.type)}
                      </div>
                      <div>
                        <h3 className="text-white font-semibold text-lg">
                          {item.title}
                        </h3>
                        <p className="text-purple-300 text-sm">
                          {getTypeLabel(item.type)}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2 text-purple-300 text-sm">
                      <Clock className="w-4 h-4" />
                      <span>{formatTimestamp(item.timestamp)}</span>
                    </div>
                  </div>

                  <div className="mb-4">
                    <p className="text-purple-200 text-sm mb-2">
                      <span className="font-semibold">Source:</span> {item.source}
                    </p>
                    <p className="text-purple-200 text-sm">
                      <span className="font-semibold">Classification:</span> {item.classification}
                    </p>
                  </div>

                  <div className="flex items-center justify-between">
                    <p className="text-purple-300 text-sm line-clamp-2">
                      {item.summary.substring(0, 150)}...
                    </p>
                    <div className="flex items-center space-x-2">
                      {item.audio && (
                        <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
                          <Play className="w-4 h-4 text-white" />
                        </div>
                      )}
                      <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
                        <Download className="w-4 h-4 text-white" />
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 