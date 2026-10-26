"use client";

import React from "react";
import { LANGUAGES, TRANSLATIONS } from "../lib/i18n";
import { LanguageCode } from "../lib/types";
import { Globe, ShieldCheck, Cpu, CheckCircle } from "lucide-react";

interface NavbarProps {
  currentLang: LanguageCode;
  onLanguageChange: (lang: LanguageCode) => void;
  activeTab: string;
  onTabChange: (tab: string) => void;
  pendingCount: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentLang,
  onLanguageChange,
  activeTab,
  onTabChange,
  pendingCount,
}) => {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  const tabs = [
    { id: "agent", label: t.tab_agent },
    { id: "calculators", label: t.tab_calculators },
    { id: "approvals", label: `${t.tab_approvals} ${pendingCount > 0 ? `(${pendingCount})` : ""}` },
    { id: "reconciler", label: t.tab_reconciler },
    { id: "knowledge", label: t.tab_knowledge },
    { id: "audit", label: t.tab_audit },
  ];

  return (
    <header className="bg-slate-900 border-b border-slate-800 text-white sticky top-0 z-50 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Title */}
          <div className="flex items-center space-x-3 rtl:space-x-reverse cursor-pointer" onClick={() => onTabChange("agent")}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 via-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20">
              <Cpu className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2 rtl:space-x-reverse">
                <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-amber-200 bg-clip-text text-transparent">
                  {t.app_title}
                </span>
                <span className="px-2 py-0.5 text-[10px] font-semibold bg-sky-500/20 text-sky-400 border border-sky-500/30 rounded-full">
                  Competition Edition
                </span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">
                {t.app_subtitle}
              </p>
            </div>
          </div>

          {/* Right controls: Language & Status */}
          <div className="flex items-center space-x-4 rtl:space-x-reverse">
            {/* Live Operational Badge */}
            <div className="hidden md:flex items-center space-x-1.5 rtl:space-x-reverse px-2.5 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-xs text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>Online • Zero-Inference L1 Ready</span>
            </div>

            {/* Language Dropdown */}
            <div className="flex items-center space-x-1.5 rtl:space-x-reverse bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200">
              <Globe className="w-3.5 h-3.5 text-slate-400" />
              <select
                value={currentLang}
                onChange={(e) => onLanguageChange(e.target.value as LanguageCode)}
                className="bg-transparent text-white focus:outline-none cursor-pointer"
              >
                {Object.values(LANGUAGES).map((lang) => (
                  <option key={lang.code} value={lang.code} className="bg-slate-900 text-white">
                    {lang.nativeName} ({lang.code.toUpperCase()})
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex overflow-x-auto space-x-1 rtl:space-x-reverse border-t border-slate-800/80 py-2 scrollbar-none">
          {tabs.map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all ${
                  isActive
                    ? "bg-sky-600 text-white shadow-sm shadow-sky-600/30"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                }`}
              >
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
};
