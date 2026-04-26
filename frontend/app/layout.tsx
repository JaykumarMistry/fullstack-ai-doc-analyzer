import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TechTorch AI Agent",
  description: "Agentic RAG application boilerplate",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen flex flex-col">{children}</body>
    </html>
  );
}
