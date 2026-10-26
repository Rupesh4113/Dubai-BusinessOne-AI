"use client";

import React, { useState, useEffect } from "react";
import { Navbar } from "../components/Navbar";
import { AgentChat } from "../components/AgentChat";
import { CalculatorsView } from "../components/CalculatorsView";
import { ApprovalCenter } from "../components/ApprovalCenter";
import { AuditExplorer } from "../components/AuditExplorer";
import { DocumentReconciler } from "../components/DocumentReconciler";
import { KnowledgeExplorer } from "../components/KnowledgeExplorer";
import { LanguageCode } from "../lib/types";
import { LANGUAGES } from "../lib/i18n";
import { fetchPendingApprovals } from "../lib/api";

export default function Home() {
  const [currentLang, setCurrentLang] = useState<LanguageCode>("en");
  const [activeTab, setActiveTab] = useState<string>("agent");
  const [pendingCount, setPendingCount] = useState<number>(0);

  const refreshPendingCount = async () => {
    try {
      const data = await fetchPendingApprovals();
      setPendingCount(data.total_pending || 0);
    } catch (e) {
      // Backend not yet running or network delay
    }
  };

  useEffect(() => {
    refreshPendingCount();
    const interval = setInterval(refreshPendingCount, 5000);
    return () => clearInterval(interval);
  }, []);

  const currentDir = LANGUAGES[currentLang]?.dir || "ltr";

  return (
    <div dir={currentDir} className="min-h-screen flex flex-col bg-slate-50 font-sans text-slate-900">
      <Navbar
        currentLang={currentLang}
        onLanguageChange={setCurrentLang}
        activeTab={activeTab}
        onTabChange={setActiveTab}
        pendingCount={pendingCount}
      />

      <main className="flex-1">
        {activeTab === "agent" && (
          <AgentChat currentLang={currentLang} onRefreshPending={refreshPendingCount} />
        )}
        {activeTab === "calculators" && (
          <CalculatorsView currentLang={currentLang} />
        )}
        {activeTab === "approvals" && (
          <ApprovalCenter currentLang={currentLang} onRefreshPending={refreshPendingCount} />
        )}
        {activeTab === "reconciler" && (
          <DocumentReconciler currentLang={currentLang} />
        )}
        {activeTab === "knowledge" && (
          <KnowledgeExplorer currentLang={currentLang} />
        )}
        {activeTab === "audit" && (
          <AuditExplorer currentLang={currentLang} />
        )}
      </main>
    </div>
  );
}
