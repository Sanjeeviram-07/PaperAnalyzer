import React, { useState } from 'react';
import { FileText, Copy, Check, ExternalLink, Download } from 'lucide-react';

interface SourceInfo {
  title: string;
  authors: string[];
  year: string;
  journal: string;
  doi?: string;
  url?: string;
  filename?: string;
  access_date: string;
  file_size?: string;
}

interface Citations {
  apa?: string;
  mla?: string;
  chicago?: string;
  bibtex?: string;
}

interface CitationViewerProps {
  sourceInfo: SourceInfo;
  citations: Citations;
}

export default function CitationViewer({ sourceInfo, citations }: CitationViewerProps) {
  const [selectedFormat, setSelectedFormat] = useState<'apa' | 'mla' | 'chicago' | 'bibtex'>('apa');
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const downloadBibTeX = () => {
    if (citations.bibtex) {
      const blob = new Blob([citations.bibtex], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'citation.bib';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  const openSource = () => {
    if (sourceInfo.url) {
      window.open(sourceInfo.url, '_blank');
    } else if (sourceInfo.doi) {
      window.open(`https://doi.org/${sourceInfo.doi}`, '_blank');
    }
  };

  return (
    <div className="space-y-6">
      {/* Source Information */}
      <div className="bg-purple-700/50 rounded-xl p-6">
        <h2 className="text-2xl font-semibold text-white mb-6 flex items-center">
          <FileText className="w-6 h-6 mr-2 text-teal-400" />
          Source Information
        </h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Title</h3>
              <p className="text-purple-200">{sourceInfo.title}</p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Authors</h3>
              <p className="text-purple-200">{sourceInfo.authors.join(', ')}</p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Journal</h3>
              <p className="text-purple-200">{sourceInfo.journal}</p>
            </div>
          </div>
          
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Year</h3>
              <p className="text-purple-200">{sourceInfo.year}</p>
            </div>
            
            {sourceInfo.doi && (
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">DOI</h3>
                <p className="text-teal-400 font-mono text-sm">{sourceInfo.doi}</p>
              </div>
            )}
            
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Accessed</h3>
              <p className="text-purple-200">{sourceInfo.access_date}</p>
            </div>
          </div>
        </div>
        
        {/* Action Buttons */}
        <div className="flex flex-wrap gap-3 mt-6">
          {(sourceInfo.url || sourceInfo.doi) && (
            <button
              onClick={openSource}
              className="flex items-center space-x-2 bg-teal-500 hover:bg-teal-600 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <ExternalLink className="w-4 h-4" />
              <span>View Source</span>
            </button>
          )}
          
          {sourceInfo.filename && (
            <div className="flex items-center space-x-2 bg-purple-600 text-white px-4 py-2 rounded-lg">
              <FileText className="w-4 h-4" />
              <span>{sourceInfo.filename}</span>
            </div>
          )}
        </div>
      </div>

      {/* Citations */}
      <div className="bg-purple-700/50 rounded-xl p-6">
        <h2 className="text-2xl font-semibold text-white mb-6 flex items-center">
          <FileText className="w-6 h-6 mr-2 text-teal-400" />
          Citations
        </h2>
        
        {/* Citation Format Selector */}
        <div className="flex flex-wrap gap-2 mb-6">
          {Object.keys(citations).map((format) => (
            <button
              key={format}
              onClick={() => setSelectedFormat(format as any)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedFormat === format
                  ? 'bg-teal-500 text-white'
                  : 'bg-purple-600 text-purple-200 hover:bg-purple-500'
              }`}
            >
              {format.toUpperCase()}
            </button>
          ))}
        </div>
        
        {/* Citation Display */}
        {citations[selectedFormat] && (
          <div className="bg-purple-800/50 rounded-xl p-6">
            <div className="flex items-start justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">{selectedFormat.toUpperCase()} Citation</h3>
              <div className="flex space-x-2">
                <button
                  onClick={() => copyToClipboard(citations[selectedFormat]!)}
                  className="flex items-center space-x-2 bg-purple-600 hover:bg-purple-500 text-white px-3 py-1 rounded-lg transition-colors"
                >
                  {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                  <span className="text-sm">{copied ? 'Copied!' : 'Copy'}</span>
                </button>
                
                {selectedFormat === 'bibtex' && (
                  <button
                    onClick={downloadBibTeX}
                    className="flex items-center space-x-2 bg-teal-500 hover:bg-teal-600 text-white px-3 py-1 rounded-lg transition-colors"
                  >
                    <Download className="w-4 h-4" />
                    <span className="text-sm">Download</span>
                  </button>
                )}
              </div>
            </div>
            
            <div className="bg-purple-900/50 rounded-lg p-4">
              <pre className="text-purple-100 text-sm whitespace-pre-wrap font-mono">
                {citations[selectedFormat]}
              </pre>
            </div>
          </div>
        )}
        
        {/* Citation Guidelines */}
        <div className="mt-6 bg-purple-800/30 rounded-lg p-4">
          <h4 className="text-white font-semibold mb-2">Citation Guidelines</h4>
          <ul className="text-purple-200 text-sm space-y-1">
            <li>• <strong>APA:</strong> American Psychological Association - commonly used in social sciences</li>
            <li>• <strong>MLA:</strong> Modern Language Association - commonly used in humanities</li>
            <li>• <strong>Chicago:</strong> Chicago Manual of Style - commonly used in history and some sciences</li>
            <li>• <strong>BibTeX:</strong> Reference management format for LaTeX documents</li>
          </ul>
        </div>
      </div>
    </div>
  );
} 