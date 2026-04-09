import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OLHO_DE_DEUS | Autonomous Pentest Dashboard",
  description: "Neural Interface for Offensive Security",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="pt-BR"
      className="h-full antialiased"
    >
      <body className="min-h-full flex flex-col bg-black text-emerald-500 font-mono">
        {children}
      </body>
    </html>
  );
}
