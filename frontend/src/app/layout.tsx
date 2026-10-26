import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Dubai BusinessOne AI — Intelligent Digital Operations Agent",
  description: "Secure, scalable, multilingual, multimodal digital operations agent for the Dubai Chamber Digital AI Agent Competition.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
