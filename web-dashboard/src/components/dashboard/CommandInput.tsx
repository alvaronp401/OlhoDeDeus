'use client';

import { useState, useRef } from 'react';
import { Send, Camera, X } from 'lucide-react';

interface CommandInputProps {
  onExecute: (command: string) => void;
  onSendImage?: (file: File, prompt: string) => void;
  isProcessing: boolean;
}

export const CommandInput = ({ onExecute, onSendImage, isProcessing }: CommandInputProps) => {
  const [input, setInput] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isProcessing) return;

    if (selectedFile && onSendImage) {
      onSendImage(selectedFile, input || "Analise esta evidência.");
      setSelectedFile(null);
      setPreviewUrl(null);
    } else if (input.trim()) {
      onExecute(input);
    }
    
    setInput('');
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
  };

  return (
    <div className="border border-emerald-900/30 bg-black/40 p-4 backdrop-blur-sm relative transition-all focus-within:border-emerald-500/50">
      
      {/* File Preview */}
      {previewUrl && (
        <div className="absolute -top-32 left-4 p-2 bg-black border border-emerald-500/50 animate-in slide-in-from-bottom-2 duration-200">
          <div className="relative group">
            <img src={previewUrl} alt="Preview" className="h-24 object-contain brightness-75 group-hover:brightness-100 transition-all" />
            <button 
              onClick={clearFile}
              className="absolute -top-2 -right-2 bg-rose-500 text-white p-1 rounded-full hover:bg-rose-600 transition-colors shadow-lg"
            >
              <X size={12} />
            </button>
          </div>
          <p className="text-[8px] mt-1 text-emerald-500 uppercase font-mono tracking-widest truncate max-w-[100px]">
            {selectedFile?.name}
          </p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex gap-4">
        <input 
          type="file" 
          ref={fileInputRef}
          onChange={handleFileChange}
          accept="image/*"
          className="hidden"
        />
        
        <button 
          type="button"
          onClick={() => fileInputRef.current?.click()}
          className={`flex items-center justify-center w-10 transition-colors ${selectedFile ? 'text-emerald-400 bg-emerald-500/10 border border-emerald-500/30' : 'text-emerald-900 hover:text-emerald-500'}`}
          title="Anexar evidência visual (Burp, Terminal, etc)"
        >
          <Camera size={18} />
        </button>

        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={selectedFile ? "Descreva o que analisar na imagem..." : "ESTABELECER_OBJETIVO_DE_INTRUSAO ..."}
          className="flex-1 bg-transparent border-none outline-none text-xs text-emerald-200 placeholder:text-emerald-900/50 font-mono"
          disabled={isProcessing}
        />
        <button 
          type="submit"
          className={`px-6 py-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-500 text-[10px] font-black uppercase tracking-[0.2em] transition-all
            ${isProcessing ? 'opacity-50 cursor-not-allowed' : 'hover:bg-emerald-500 hover:text-black hover:shadow-[0_0_20px_rgba(16,185,129,0.3)]'}
          `}
          disabled={isProcessing}
        >
          {isProcessing ? 'Calculando ...' : selectedFile ? 'Analisar' : 'Executar'}
        </button>
      </form>
    </div>
  );
};
