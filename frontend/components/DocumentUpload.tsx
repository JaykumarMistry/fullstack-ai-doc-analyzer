"use client";

import { useState } from "react";
import { UploadCloud, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";

export default function DocumentUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setStatus("idle");
      setMessage("");
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setStatus("uploading");
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setStatus("success");
        setMessage(`Indexed ${data.num_chunks} chunks.`);
      } else {
        setStatus("error");
        setMessage(data.detail || "Upload failed");
      }
    } catch (error) {
      setStatus("error");
      setMessage("Connection error. Is backend running?");
    }
  };

  return (
    <div className="flex flex-col gap-4 mt-auto">
      <div className="relative border-2 border-dashed border-slate-300 dark:border-slate-600 rounded-xl p-6 flex flex-col items-center justify-center text-center hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors">
        <UploadCloud className="w-8 h-8 text-slate-400 mb-2" />
        <p className="text-sm font-medium text-slate-700 dark:text-slate-200">
          {file ? file.name : "Select a PDF or CSV"}
        </p>
        <p className="text-xs text-slate-500 mt-1">Up to 10MB</p>
        <input
          type="file"
          accept=".pdf,.csv"
          onChange={handleFileChange}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
      </div>

      <button
        onClick={handleUpload}
        disabled={!file || status === "uploading"}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        {status === "uploading" && <Loader2 className="w-4 h-4 animate-spin" />}
        {status === "uploading" ? "Uploading..." : (file ? "Submit Document" : "Select Document")}
      </button>

      {status === "success" && (
        <div className="flex items-center gap-2 text-sm text-green-600 bg-green-50 p-3 rounded-lg">
          <CheckCircle2 className="w-4 h-4" />
          <span>{message}</span>
        </div>
      )}

      {status === "error" && (
        <div className="flex items-center gap-2 text-sm text-red-600 bg-red-50 p-3 rounded-lg">
          <AlertCircle className="w-4 h-4" />
          <span>{message}</span>
        </div>
      )}
    </div>
  );
}
