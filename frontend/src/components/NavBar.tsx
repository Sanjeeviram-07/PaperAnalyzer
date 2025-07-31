import React from 'react';
import { Home, History } from 'lucide-react';
import PaperAnalyzerLogo from './PaperAnalyzerLogo';

interface NavBarProps {
  onReset: () => void;
  showReset: boolean;
  onHistoryClick?: () => void;
}

export default function NavBar({ onReset, showReset, onHistoryClick }: NavBarProps) {
  return (
    <header className="sticky top-0 z-50 bg-purple-900/90 backdrop-blur-xl border-b border-white/10 shadow-lg">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          {/* Logo/Brand */}
          <PaperAnalyzerLogo />

          {/* Navigation */}
          <div className="flex items-center space-x-4">
            {showReset ? (
              <>
                <button
                  onClick={onHistoryClick}
                  className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm hover:bg-white/20 border border-white/20 text-white px-6 py-3 rounded-full transition-all duration-200 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
                >
                  <History className="w-4 h-4" />
                  <span>Generation History</span>
                </button>
                <button
                  onClick={onReset}
                  className="flex items-center space-x-2 bg-gradient-to-r from-teal-500 to-teal-600 hover:from-teal-400 hover:to-teal-500 text-white px-6 py-3 rounded-full transition-all duration-200 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
                >
                  <Home className="w-4 h-4" />
                  <span>New Analysis</span>
                </button>
              </>
            ) : (
              <button
                onClick={onHistoryClick}
                className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm hover:bg-white/20 border border-white/20 text-white px-6 py-3 rounded-full transition-all duration-200 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
              >
                <History className="w-4 h-4" />
                <span>Generation History</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
} 