import React from 'react';
import { FileText } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-purple-900/80 backdrop-blur-xl border-t border-white/10">
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="text-center">
          {/* Logo & Mission */}
          <div className="flex items-center justify-center space-x-3 mb-8">
            <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-green-600 rounded-xl flex items-center justify-center shadow-lg">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <span className="text-3xl font-bold text-white tracking-wide">PaperAnalyzer</span>
          </div>
          <p className="text-purple-200 text-xl leading-relaxed mb-6 max-w-2xl mx-auto">
            Making research accessible and efficient through AI-powered analysis.
          </p>
          <p className="text-purple-300 text-lg mb-8">
            Built for researchers, by researchers. Transform how you consume and understand academic papers.
          </p>
          
          {/* Copyright */}
          <div className="pt-8 border-t border-white/10">
            <p className="text-purple-300 text-sm">
              © 2025 PaperAnalyzer. Built for researchers, by researchers.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
} 