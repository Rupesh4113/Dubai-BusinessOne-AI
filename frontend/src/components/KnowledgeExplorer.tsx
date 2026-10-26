"use client";

import React, { useState, useEffect } from "react";
import { TRANSLATIONS } from "../lib/i18n";
import { LanguageCode } from "../lib/types";
import { searchKnowledgeAPI } from "../lib/api";
import { BookOpen, Search, ExternalLink, ShieldCheck } from "lucide-react";

interface KnowledgeExplorerProps {
  currentLang: LanguageCode;
}

export const KnowledgeExplorer: React.FC<KnowledgeExplorerProps> = ({ currentLang }) => {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  const [query, setQuery] = useState("corporate tax small business relief");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (searchTerm?: string) => {
    const q = searchTerm || query;
    if (!q.trim()) return;
    setLoading(true);
    try {
      const data = await searchKnowledgeAPI(q);
      setResults(data || []);
    } catch (e) {
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleSearch("mainland llc corporate tax chamber");
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
        <div className="flex items-center space-x-2 rtl:space-x-reverse text-slate-900 font-bold text-base">
          <BookOpen className="w-5 h-5 text-sky-600" />
          <span>{t.tab_knowledge}</span>
        </div>
        <p className="text-xs text-slate-500">
          Verified regulatory articles from the Dubai Chamber of Commerce, Dubai DET, and UAE Federal Tax Authority.
        </p>

        {/* Search Bar */}
        <div className="flex items-center space-x-2 rtl:space-x-reverse">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            placeholder="Search verified laws (e.g., 100% foreign ownership, instant license, 375,000 threshold)..."
            className="flex-1 border border-slate-300 rounded-xl px-4 py-2.5 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-sky-500"
          />
          <button
            onClick={() => handleSearch()}
            disabled={loading}
            className="bg-sky-600 hover:bg-sky-700 text-white px-4 py-2.5 rounded-xl font-medium text-xs flex items-center space-x-1 rtl:space-x-reverse shadow-sm transition"
          >
            <Search className="w-3.5 h-3.5" />
            <span>Search</span>
          </button>
        </div>

        {/* Results */}
        <div className="space-y-4 pt-2">
          {results.map((rec) => (
            <div
              key={rec.record_id}
              className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2 hover:border-slate-300 transition"
            >
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="font-bold text-slate-900 text-sm">{rec.title}</span>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-100 text-emerald-800 flex items-center space-x-1 rtl:space-x-reverse">
                  <ShieldCheck className="w-3 h-3 text-emerald-600" />
                  <span>Verified Official Source</span>
                </span>
              </div>

              <div className="text-xs text-slate-500 font-medium">
                {rec.issuing_authority} • <span className="italic">{rec.statutory_law}</span>
              </div>

              <p className="text-xs text-slate-700">{rec.summary}</p>

              {rec.detailed_rules && (
                <ul className="list-disc list-inside text-xs text-slate-600 space-y-0.5 pt-1 pl-1">
                  {rec.detailed_rules.map((rule: string, idx: number) => (
                    <li key={idx}>{rule}</li>
                  ))}
                </ul>
              )}

              <div className="pt-2 flex items-center justify-between text-[11px] border-t border-slate-200">
                <div className="flex flex-wrap gap-1">
                  {rec.tags?.map((tg: string) => (
                    <span key={tg} className="px-1.5 py-0.5 bg-slate-200 text-slate-600 rounded text-[10px]">
                      #{tg}
                    </span>
                  ))}
                </div>
                <a
                  href={rec.official_source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-sky-600 hover:text-sky-800 flex items-center space-x-1 rtl:space-x-reverse font-semibold"
                >
                  <span>Official Portal</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
