"use client";

import React, { useState } from "react";
import { TRANSLATIONS } from "../lib/i18n";
import { LanguageCode, ChatMessage } from "../lib/types";
import { sendAgentChat } from "../lib/api";
import {
  Send,
  Sparkles,
  ShieldAlert,
  ShieldCheck,
  Zap,
  RotateCcw,
  ExternalLink,
  ChevronDown,
  ChevronUp,
  FileCheck2,
  AlertTriangle
} from "lucide-react";

interface AgentChatProps {
  currentLang: LanguageCode;
  onRefreshPending: () => void;
}

export const AgentChat: React.FC<AgentChatProps> = ({ currentLang, onRefreshPending }) => {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "initial-1",
      sender: "agent",
      text: t.chat_placeholder,
      timestamp: "Just now",
    },
  ]);
  const [inputPrompt, setInputPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [expandedCalcs, setExpandedCalcs] = useState<Record<string, boolean>>({});

  const handleSend = async (textToSend?: string, approvalToken?: string) => {
    const query = textToSend || inputPrompt;
    if (!query.trim()) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: "user",
      text: query,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInputPrompt("");
    setLoading(true);

    try {
      const responseState = await sendAgentChat(query, currentLang, approvalToken);
      const isL1 = responseState.is_cached_zero_inference;

      const agentMsg: ChatMessage = {
        id: `agent-${Date.now()}`,
        sender: "agent",
        text: responseState.final_response_text || "Task processed.",
        timestamp: new Date().toLocaleTimeString(),
        taskState: responseState,
        isCachedZeroInference: isL1,
      };

      setMessages((prev) => [...prev, agentMsg]);
      onRefreshPending();
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: `err-${Date.now()}`,
          sender: "agent",
          text: `⚠️ Execution notice: ${err.message || "Unable to complete request"}`,
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const toggleCalcDetails = (msgId: string) => {
    setExpandedCalcs((prev) => ({ ...prev, [msgId]: !prev[msgId] }));
  };

  const handleQuickPrompt = (scenarioKey: string) => {
    let p = "";
    if (scenarioKey === "s1") {
      p = "I want to establish a technology consulting firm as a Mainland LLC in Dubai with expected year 1 revenue of 1,200,000 AED and 60,000 AED office rent.";
    } else if (scenarioKey === "s2") {
      p = "Please reserve trade name 'Falcon Tech Solutions LLC' in Dubai DET";
    } else if (scenarioKey === "s3") {
      p = "Calculate UAE Corporate Tax on annual taxable net profit of 1,000,000 AED";
    } else if (scenarioKey === "s4") {
      p = "Reconcile commercial invoice INV-2026-001 for UAE VAT compliance and verify TRN 100998877665544";
    }
    handleSend(p);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8.5rem)] max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      {/* Quick Prompts Carousel / Buttons */}
      <div className="mb-3">
        <div className="flex items-center space-x-2 rtl:space-x-reverse mb-1.5 text-xs font-semibold text-slate-500 uppercase tracking-wider">
          <Sparkles className="w-3.5 h-3.5 text-amber-500" />
          <span>{t.quick_prompts_title}</span>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => handleQuickPrompt("s1")}
            className="text-xs bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 px-3 py-1.5 rounded-lg shadow-sm transition"
          >
            📋 {t.scenario_1}
          </button>
          <button
            onClick={() => handleQuickPrompt("s2")}
            className="text-xs bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 px-3 py-1.5 rounded-lg shadow-sm transition"
          >
            🛡️ {t.scenario_2}
          </button>
          <button
            onClick={() => handleQuickPrompt("s3")}
            className="text-xs bg-sky-50 hover:bg-sky-100 text-sky-900 border border-sky-200 px-3 py-1.5 rounded-lg shadow-sm transition"
          >
            ⚖️ {t.scenario_3}
          </button>
          <button
            onClick={() => handleQuickPrompt("s4")}
            className="text-xs bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border border-emerald-200 px-3 py-1.5 rounded-lg shadow-sm transition"
          >
            🧾 {t.scenario_4}
          </button>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 bg-white border border-slate-200 rounded-2xl p-4 sm:p-6 overflow-y-auto space-y-4 shadow-sm">
        {messages.map((msg) => {
          const isAgent = msg.sender === "agent";
          const state = msg.taskState;

          return (
            <div
              key={msg.id}
              className={`flex flex-col ${isAgent ? "items-start" : "items-end"} max-w-4xl ${
                !isAgent && "ml-auto rtl:mr-auto rtl:ml-0"
              }`}
            >
              <div
                className={`rounded-2xl px-5 py-4 ${
                  isAgent
                    ? "bg-slate-50 text-slate-800 border border-slate-200 shadow-sm w-full"
                    : "bg-sky-600 text-white shadow-md max-w-2xl"
                }`}
              >
                {/* Badges Bar for Agent Messages */}
                {isAgent && state && (
                  <div className="flex flex-wrap items-center gap-2 mb-3 pb-2.5 border-b border-slate-200 text-xs">
                    {msg.isCachedZeroInference ? (
                      <span className="flex items-center space-x-1 rtl:space-x-reverse px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-semibold border border-emerald-200">
                        <Zap className="w-3 h-3 text-emerald-600" />
                        <span>{t.cache_hit_badge}</span>
                      </span>
                    ) : (
                      <span className="flex items-center space-x-1 rtl:space-x-reverse px-2.5 py-0.5 rounded-full bg-slate-200 text-slate-700 font-medium">
                        <span>Task ID: {state.task_id}</span>
                      </span>
                    )}

                    {state.risk_level === "HIGH" ? (
                      <span className="flex items-center space-x-1 rtl:space-x-reverse px-2.5 py-0.5 rounded-full bg-rose-100 text-rose-800 font-semibold border border-rose-200">
                        <AlertTriangle className="w-3 h-3 text-rose-600" />
                        <span>{t.risk_high}</span>
                      </span>
                    ) : state.risk_level === "MEDIUM" ? (
                      <span className="flex items-center space-x-1 rtl:space-x-reverse px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 font-medium border border-amber-200">
                        <span>{t.risk_medium}</span>
                      </span>
                    ) : (
                      <span className="flex items-center space-x-1 rtl:space-x-reverse px-2.5 py-0.5 rounded-full bg-sky-100 text-sky-800 font-medium border border-sky-200">
                        <ShieldCheck className="w-3 h-3 text-sky-600" />
                        <span>{t.risk_low}</span>
                      </span>
                    )}
                  </div>
                )}

                {/* Text Content */}
                <div className="prose prose-sm max-w-none whitespace-pre-line text-slate-800">
                  {msg.text}
                </div>

                {/* High Risk Approval Gate Prompt */}
                {isAgent && state && state.requires_human_approval && !state.is_approved_by_human && (
                  <div className="mt-4 p-4 rounded-xl bg-amber-50 border border-amber-300">
                    <div className="flex items-center space-x-2 rtl:space-x-reverse text-amber-900 font-semibold text-sm mb-1">
                      <ShieldAlert className="w-4 h-4 text-amber-600" />
                      <span>{t.pending_approval_notice}</span>
                    </div>
                    <p className="text-xs text-amber-800 mb-3">
                      Token: <code className="bg-amber-100 px-2 py-0.5 rounded font-mono font-bold text-amber-950">{state.approval_token}</code>
                    </p>
                    <button
                      onClick={() => handleSend(msg.text, state.approval_token)}
                      className="px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-xs font-semibold shadow-sm transition"
                    >
                      🛡️ {t.approve_button}
                    </button>
                  </div>
                )}

                {/* Deterministic Calculations Provenance Drawer */}
                {isAgent && state && state.intermediate_calculations && Object.keys(state.intermediate_calculations).length > 0 && (
                  <div className="mt-4 border-t border-slate-200 pt-3">
                    <button
                      onClick={() => toggleCalcDetails(msg.id)}
                      className="flex items-center space-x-1 rtl:space-x-reverse text-xs font-medium text-sky-700 hover:text-sky-900"
                    >
                      <FileCheck2 className="w-3.5 h-3.5" />
                      <span>{t.statutory_steps_title}</span>
                      {expandedCalcs[msg.id] ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                    </button>

                    {expandedCalcs[msg.id] && (
                      <div className="mt-2.5 space-y-2 bg-slate-100/70 p-3 rounded-xl text-xs">
                        {Object.entries(state.intermediate_calculations).map(([calcKey, calcData]: [string, any]) => (
                          <div key={calcKey} className="p-2 bg-white rounded-lg border border-slate-200">
                            <span className="font-semibold text-slate-900 uppercase tracking-wide text-[11px]">
                              {calcKey.replace("_", " ")}
                            </span>
                            {calcData.calculation_steps && (
                              <div className="mt-1.5 space-y-1">
                                {calcData.calculation_steps.map((st: any) => (
                                  <div key={st.step_number} className="text-slate-600 text-[11px] font-mono">
                                    Step {st.step_number}: {st.description} → <span className="font-bold text-slate-800">{st.intermediate_value}</span>
                                    {st.statutory_reference && (
                                      <div className="text-[10px] text-slate-400 font-sans italic">{st.statutory_reference}</div>
                                    )}
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* Citations Footer */}
                {isAgent && state && state.citations && state.citations.length > 0 && (
                  <div className="mt-3 pt-2.5 border-t border-slate-200 flex flex-wrap gap-2 text-[11px] text-slate-500">
                    <span className="font-medium text-slate-700">{t.citations_title}:</span>
                    {state.citations.map((c: any, idx: number) => (
                      <a
                        key={idx}
                        href={c.official_source_url}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center space-x-1 rtl:space-x-reverse text-sky-600 hover:text-sky-800 underline decoration-sky-300"
                      >
                        <span>{c.authority_name}</span>
                        <ExternalLink className="w-2.5 h-2.5" />
                      </a>
                    ))}
                  </div>
                )}
              </div>
              <span className="text-[10px] text-slate-400 mt-1 px-2">{msg.timestamp}</span>
            </div>
          );
        })}

        {loading && (
          <div className="flex items-center space-x-2 rtl:space-x-reverse text-slate-500 text-xs py-2 px-3 bg-slate-50 border border-slate-200 rounded-xl w-fit animate-pulse">
            <Zap className="w-4 h-4 text-amber-500" />
            <span>{t.processing}</span>
          </div>
        )}
      </div>

      {/* Input Form */}
      <div className="mt-3 flex items-center space-x-2 rtl:space-x-reverse">
        <input
          type="text"
          value={inputPrompt}
          onChange={(e) => setInputPrompt(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !loading && handleSend()}
          placeholder={t.chat_placeholder}
          disabled={loading}
          className="flex-1 bg-white border border-slate-300 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500 text-slate-900 shadow-sm"
        />
        <button
          onClick={() => handleSend()}
          disabled={loading || !inputPrompt.trim()}
          className="bg-sky-600 hover:bg-sky-700 disabled:bg-slate-300 text-white px-5 py-3 rounded-xl font-medium text-sm flex items-center space-x-1.5 rtl:space-x-reverse shadow-md transition"
        >
          <Send className="w-4 h-4" />
          <span className="hidden sm:inline">{t.send_button}</span>
        </button>
      </div>
    </div>
  );
};
