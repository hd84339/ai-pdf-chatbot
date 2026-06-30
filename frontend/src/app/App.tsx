import React, { useState, useRef } from 'react';

export function App() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const [isUploading, setIsUploading] = useState(false);
  const [isIndexed, setIsIndexed] = useState(false);

  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState<{ role: 'user' | 'bot'; text: string }[]>([]);
  const [isAsking, setIsAsking] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus('Please select a PDF file first.');
      return;
    }

    setIsUploading(true);
    setUploadStatus('Uploading and indexing PDF... This may take a moment.');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/upload-pdf', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setUploadStatus(`Success! Indexed ${data.num_chunks} chunks.`);
        setIsIndexed(true);
      } else {
        const errorData = await response.json();
        setUploadStatus(`Error: ${errorData.detail || 'Failed to upload'}`);
      }
    } catch (error: any) {
      setUploadStatus(`Connection error: Make sure the backend is running.`);
    } finally {
      setIsUploading(false);
    }
  };

  const handleAskQuestion = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    const userQuestion = question;
    setQuestion('');
    setChatHistory((prev) => [...prev, { role: 'user', text: userQuestion }]);
    setIsAsking(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: userQuestion }),
      });

      if (response.ok) {
        const data = await response.json();
        setChatHistory((prev) => [...prev, { role: 'bot', text: data.answer }]);
      } else {
        setChatHistory((prev) => [
          ...prev,
          { role: 'bot', text: 'Sorry, I encountered an error answering your question.' },
        ]);
      }
    } catch (error) {
      setChatHistory((prev) => [
        ...prev,
        { role: 'bot', text: 'Error: Cannot reach the backend server.' },
      ]);
    } finally {
      setIsAsking(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8 font-sans text-slate-800">
      <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Sidebar: Upload Section */}
        <div className="md:col-span-1 bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col">
          <h2 className="text-xl font-bold mb-4">1. Document Setup</h2>
          <p className="text-sm text-slate-500 mb-6">
            Upload your PDF. The backend will extract text, chunk it, and generate embeddings.
          </p>

          <input
            type="file"
            accept=".pdf"
            className="hidden"
            ref={fileInputRef}
            onChange={handleFileChange}
          />

          <button
            onClick={() => fileInputRef.current?.click()}
            className="w-full border-2 border-dashed border-slate-300 hover:border-blue-500 hover:bg-blue-50 text-slate-600 rounded-lg py-8 px-4 mb-4 transition-colors"
          >
            {file ? (
              <span className="font-medium text-blue-600">{file.name}</span>
            ) : (
              <span>Click to select a PDF</span>
            )}
          </button>

          <button
            onClick={handleUpload}
            disabled={!file || isUploading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            {isUploading ? 'Indexing...' : 'Upload & Index PDF'}
          </button>

          {uploadStatus && (
            <div className={`mt-4 p-3 rounded text-sm ${isIndexed ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-blue-50 text-blue-700 border border-blue-200'}`}>
              {uploadStatus}
            </div>
          )}
        </div>

        {/* Main Area: Chat Section */}
        <div className="md:col-span-2 bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col h-[600px]">
          <h2 className="text-xl font-bold mb-4">2. Chat with your PDF</h2>
          
          <div className="flex-1 overflow-y-auto mb-4 bg-slate-50 rounded-lg border border-slate-100 p-4 space-y-4">
            {!isIndexed && chatHistory.length === 0 ? (
              <div className="text-center text-slate-400 mt-20">
                Please upload and index a PDF first to start asking questions.
              </div>
            ) : null}

            {chatHistory.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white rounded-tr-none'
                      : 'bg-white border border-slate-200 text-slate-700 rounded-tl-none shadow-sm'
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
            {isAsking && (
              <div className="flex justify-start">
                <div className="bg-white border border-slate-200 text-slate-500 rounded-2xl rounded-tl-none px-4 py-3 shadow-sm animate-pulse">
                  Thinking...
                </div>
              </div>
            )}
          </div>

          <form onSubmit={handleAskQuestion} className="relative">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              disabled={!isIndexed || isAsking}
              placeholder={isIndexed ? "Ask a question about the document..." : "Index a PDF first..."}
              className="w-full bg-slate-50 border border-slate-200 rounded-full py-3 pl-4 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={!question.trim() || !isIndexed || isAsking}
              className="absolute right-2 top-2 bottom-2 bg-blue-600 text-white rounded-full p-2 hover:bg-blue-700 disabled:opacity-50 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
              </svg>
            </button>
          </form>

        </div>
      </div>
    </div>
  );
}
