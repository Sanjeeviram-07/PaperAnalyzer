import React from 'react';
import { FileText } from 'lucide-react';

interface PaperAnalyzerLogoProps {
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

export default function PaperAnalyzerLogo({ className = '', size = 'md' }: PaperAnalyzerLogoProps) {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12'
  };

  const iconSizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6'
  };

  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      <div className={`${sizeClasses[size]} bg-gradient-to-br from-green-400 to-green-600 rounded-xl flex items-center justify-center shadow-lg`}>
        <FileText className={`${iconSizeClasses[size]} text-white`} />
      </div>
      <span className="text-xl font-bold text-white tracking-wide">PaperAnalyzer</span>
    </div>
  );
} 