import ChatInterface from "@/components/ChatInterface";
import DocumentUpload from "@/components/DocumentUpload";

export default function Home() {
  return (
    <main className="flex-1 flex flex-col md:flex-row h-screen max-w-7xl mx-auto w-full p-4 gap-4">
      {/* Sidebar for Upload */}
      <div className="w-full md:w-1/3 flex flex-col gap-4">
        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700 p-6 flex flex-col">
          <h1 className="text-2xl font-bold mb-2 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">TechTorch AI</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mb-6">
            Upload your PDF or CSV documents to chat with them using Agentic RAG.
          </p>
          <DocumentUpload />
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="w-full md:w-2/3 flex flex-col bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
        <ChatInterface />
      </div>
    </main>
  );
}
