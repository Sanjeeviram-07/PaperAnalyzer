import React, { useState } from 'react';
import axios from 'axios';
import { Upload, FileText } from 'lucide-react';

interface UploadFormProps {
  setData: (data: any, source: string) => void;
  onAnalysisStart?: () => void;
}

export default function UploadForm({ setData, onAnalysisStart }: UploadFormProps) {
  const [file, setFile] = useState<File | null>(null);
  const [topics, setTopics] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const upload = async () => {
    if (!file) {
      setError("Please select a file");
      return;
    }

    setLoading(true);
    setError("");
    
    // Call onAnalysisStart if provided
    if (onAnalysisStart) {
      onAnalysisStart();
    }

    try {
      const formData = new FormData();
      formData.append("file", file!);
      formData.append("topics", topics);
      const res = await axios.post("http://localhost:8000/upload/", formData);
      setData(res.data, file.name);
    } catch (err: any) {
      console.error("Error:", err);
      setError(err.response?.data?.error || err.message || "Failed to upload file");
      setData({
        summary: "Error occurred while processing the uploaded file",
        classification: "Error",
        audio: ""
      }, file.name);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="w-20 h-20 bg-gradient-to-br from-teal-400 to-teal-600 rounded-full flex items-center justify-center mx-auto mb-6 animate-pulse shadow-lg">
          <FileText className="w-10 h-10 text-white" />
        </div>
        <h3 className="text-2xl font-bold text-white mb-3">AI analyzing your paper...</h3>
        <p className="text-purple-200 text-lg mb-8">This may take a few moments</p>
        <div className="max-w-md mx-auto bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
          <div className="flex items-center justify-between mb-4">
            <span className="text-white font-medium">Processing: {file?.name}</span>
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
      {/* File Upload */}
      <div>
        <label className="block text-white font-bold text-lg mb-4">Select Research Paper</label>
        <div className="border-2 border-dashed border-purple-400/50 rounded-2xl p-12 text-center hover:border-purple-300 transition-all duration-300 bg-white/5 backdrop-blur-sm hover:bg-white/10">
          <div className="w-20 h-20 bg-gradient-to-br from-purple-400 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg">
            <Upload className="w-10 h-10 text-white" />
          </div>
          <h3 className="text-xl font-semibold text-white mb-3">Upload Research Paper</h3>
          <p className="text-purple-200 mb-6 text-lg">Drag and drop your file here, or click to browse</p>
          <input
            type="file"
            onChange={e => setFile(e.target.files?.[0] || null)}
            className="hidden"
            id="file-upload"
            accept=".pdf,.doc,.docx,.txt"
          />
          <label
            htmlFor="file-upload"
            className="bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 text-white px-8 py-3 rounded-full cursor-pointer transition-all duration-200 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            Choose File
          </label>
          {file && (
            <div className="mt-6 p-4 bg-teal-500/20 border border-teal-400/30 rounded-xl">
              <p className="text-teal-300 font-medium flex items-center justify-center">
                <FileText className="w-4 h-4 mr-2" />
                {file.name}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Topics Input */}
      <div>
        <label className="block text-white font-bold text-lg mb-4">Research Topics (Optional)</label>
        <input
          type="text"
          placeholder="e.g., AI, Machine Learning, Medical Diagnosis"
          value={topics}
          onChange={e => setTopics(e.target.value)}
          className="w-full px-6 py-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white placeholder-purple-300 focus:outline-none focus:border-teal-400 focus:ring-2 focus:ring-teal-400/20 transition-all duration-200 text-lg"
        />
        <p className="text-purple-300 text-sm mt-3 flex items-center">
          <span className="w-2 h-2 bg-teal-400 rounded-full mr-2"></span>
          Help us focus the analysis on specific areas
        </p>
      </div>

      {/* Upload Button */}
      <button
        onClick={upload}
        disabled={!file || loading}
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
