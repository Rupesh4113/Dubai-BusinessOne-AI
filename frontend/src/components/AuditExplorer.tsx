"use client";

import React, { useState, useEffect } from "react";
import { TRANSLATIONS } from "../lib/i18n";
import { LanguageCode } from "../lib/types";
import { fetchTasks, fetchTelemetry } from "../lib/api";
import { History, Zap, ShieldCheck, Database, RefreshCw } from "lucide-react";

interface AuditExplorerProps {
  currentLang: LanguageCode;
}

export const AuditExplorer: React.FC<AuditExplorerProps> = ({ currentLang }) => {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  const [tasks, setTasks] = useState<any[]>([]);
  const [telemetry, setTelemetry] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [tasksRes, teleRes] = await Promise.all([fetchTasks(25), fetchTelemetry()]);
      setTasks(tasksRes.tasks || []);
      setTelemetry(teleRes);
    } catch (e) {
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      {/* Telemetry Header Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex items-center space-x-3 rtl:space-x-reverse">
          <div className="p-3 bg-emerald-50 rounded-xl text-emerald-600">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[11px] text-slate-500 font-medium">{t.tokens_saved}</span>
            <div className="text-xl font-bold text-slate-900 font-mono">
              {telemetry?.layer1_cache_stats?.estimated_zero_inference_tokens_saved ?? 0}
            </div>
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex items-center space-x-3 rtl:space-x-reverse">
          <div className="p-3 bg-sky-50 rounded-xl text-sky-600">
            <Database className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[11px] text-slate-500 font-medium">{t.cache_hit_ratio}</span>
            <div className="text-xl font-bold text-slate-900 font-mono">
              {telemetry?.layer1_cache_stats?.hit_ratio_percent ?? 0}%
            </div>
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex items-center space-x-3 rtl:space-x-reverse">
          <div className="p-3 bg-purple-50 rounded-xl text-purple-600">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[11px] text-slate-500 font-medium">Pending Human Gates</span>
            <div className="text-xl font-bold text-slate-900 font-mono">
              {telemetry?.layer4_pending_approvals_count ?? 0}
            </div>
          </div>
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 rtl:space-x-reverse text-slate-900 font-bold text-base">
            <History className="w-5 h-5 text-sky-600" />
            <span>{t.tab_audit}</span>
          </div>
          <button
            onClick={loadData}
            className="flex items-center space-x-1.5 rtl:space-x-reverse text-xs bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-300 px-3 py-1.5 rounded-lg shadow-sm"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
            <span>Refresh Logs</span>
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full text-xs text-left rtl:text-right text-slate-600">
            <thead className="bg-slate-50 text-slate-800 uppercase tracking-wider text-[10px] font-semibold">
              <tr>
                <th className="py-2.5 px-3">Task ID</th>
                <th className="py-2.5 px-3">Action</th>
                <th className="py-2.5 px-3">Risk Tier</th>
                <th className="py-2.5 px-3">Status</th>
                <th className="py-2.5 px-3">Idempotency Key</th>
                <th className="py-2.5 px-3">Audit Trail Excerpt</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono">
              {tasks.map((task) => (
                <tr key={task.task_id} className="hover:bg-slate-50/80">
                  <td className="py-2.5 px-3 font-semibold text-slate-900">{task.task_id}</td>
                  <td className="py-2.5 px-3 font-sans text-slate-800">{task.action_name}</td>
                  <td className="py-2.5 px-3 font-sans">
                    <span
                      className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                        task.risk_level === "HIGH"
                          ? "bg-rose-100 text-rose-800"
                          : task.risk_level === "MEDIUM"
                          ? "bg-amber-100 text-amber-800"
                          : "bg-sky-100 text-sky-800"
                      }`}
                    >
                      {task.risk_level}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 font-sans">
                    <span
                      className={`px-2 py-0.5 rounded-full text-[10px] font-semibold ${
                        task.status === "VERIFIED" || task.status === "COMPLETED"
                          ? "bg-emerald-100 text-emerald-800"
                          : task.status === "PENDING_APPROVAL"
                          ? "bg-amber-100 text-amber-800"
                          : "bg-slate-100 text-slate-700"
                      }`}
                    >
                      {task.status}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 text-[11px] text-slate-400">
                    {task.idempotency_key?.slice(0, 12)}...
                  </td>
                  <td className="py-2.5 px-3 font-sans text-slate-600 max-w-xs truncate">
                    {task.audit_notes?.[task.audit_notes.length - 1] || "Initialized"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
