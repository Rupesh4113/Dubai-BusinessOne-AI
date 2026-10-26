"use client";

import React, { useState, useEffect } from "react";
import { TRANSLATIONS } from "../lib/i18n";
import { LanguageCode, PendingTask } from "../lib/types";
import { fetchPendingApprovals, submitApprovalDecision } from "../lib/api";
import { ShieldAlert, CheckCircle2, XCircle, RefreshCw, KeyRound, Clock } from "lucide-react";

interface ApprovalCenterProps {
  currentLang: LanguageCode;
  onRefreshPending: () => void;
}

export const ApprovalCenter: React.FC<ApprovalCenterProps> = ({ currentLang, onRefreshPending }) => {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  const [pendingTasks, setPendingTasks] = useState<PendingTask[]>([]);
  const [loading, setLoading] = useState(false);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  const loadApprovals = async () => {
    setLoading(true);
    try {
      const data = await fetchPendingApprovals();
      setPendingTasks(data.pending_tasks || []);
    } catch (e) {
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadApprovals();
  }, []);

  const handleDecision = async (task: PendingTask, decision: "APPROVE" | "REJECT") => {
    if (!task.approval_token) return;
    try {
      const res = await submitApprovalDecision(task.task_id, task.approval_token, decision);
      setActionMessage(`Task ${task.task_id} successfully ${decision === "APPROVE" ? "Authorized & Executed" : "Rejected"}.`);
      loadApprovals();
      onRefreshPending();
    } catch (err: any) {
      setActionMessage(`Decision error: ${err.message}`);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center space-x-2 rtl:space-x-reverse">
            <ShieldAlert className="w-6 h-6 text-amber-500" />
            <span>{t.tab_approvals}</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Supervisory Gate for high-impact commercial transactions, legal filings, and official reservations.
          </p>
        </div>
        <button
          onClick={loadApprovals}
          className="flex items-center space-x-1.5 rtl:space-x-reverse text-xs bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 px-3 py-1.5 rounded-lg shadow-sm"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
          <span>Refresh Queue</span>
        </button>
      </div>

      {actionMessage && (
        <div className="p-3 bg-sky-50 border border-sky-200 rounded-xl text-xs text-sky-800 flex items-center justify-between">
          <span>{actionMessage}</span>
          <button onClick={() => setActionMessage(null)} className="text-sky-600 font-bold ml-2">×</button>
        </div>
      )}

      {/* Pending Tasks Queue */}
      {pendingTasks.length === 0 ? (
        <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center shadow-sm">
          <div className="w-12 h-12 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto mb-3">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <h3 className="text-sm font-semibold text-slate-800">{t.no_pending_tasks}</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
            High-risk operations (such as official trade name reservation) will trigger a cryptographic token holding state here for authorized sign-off.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {pendingTasks.map((task) => (
            <div
              key={task.task_id}
              className="bg-white border border-amber-200 rounded-2xl p-5 shadow-sm space-y-4"
            >
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
                <div className="flex items-center space-x-2 rtl:space-x-reverse">
                  <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800">
                    {t.risk_high}
                  </span>
                  <span className="font-mono text-xs font-bold text-slate-800">{task.task_id}</span>
                </div>
                <div className="flex items-center space-x-1.5 rtl:space-x-reverse text-xs text-slate-400">
                  <Clock className="w-3.5 h-3.5" />
                  <span>{new Date(task.created_at_epoch * 1000).toLocaleTimeString()}</span>
                </div>
              </div>

              {/* Action and details */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div>
                  <span className="text-slate-500 block mb-0.5">Requested Action:</span>
                  <span className="font-semibold text-slate-800 text-sm">{task.action_name}</span>
                  <div className="mt-2 text-slate-600 space-y-0.5">
                    {task.input_parameters?.prompt && (
                      <p className="italic bg-slate-50 p-2 rounded-lg border border-slate-200">
                        "{task.input_parameters.prompt}"
                      </p>
                    )}
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="p-3 bg-amber-50/70 border border-amber-200 rounded-xl space-y-1">
                    <div className="flex items-center space-x-1 rtl:space-x-reverse text-amber-900 font-semibold text-[11px]">
                      <KeyRound className="w-3.5 h-3.5 text-amber-600" />
                      <span>One-Time Approval Token:</span>
                    </div>
                    <code className="block font-mono font-bold text-xs text-amber-950 bg-amber-100/80 px-2 py-1 rounded">
                      {task.approval_token}
                    </code>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center justify-end space-x-2 rtl:space-x-reverse pt-2 border-t border-slate-100">
                <button
                  onClick={() => handleDecision(task, "REJECT")}
                  className="px-4 py-2 border border-slate-300 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-semibold flex items-center space-x-1 rtl:space-x-reverse transition"
                >
                  <XCircle className="w-3.5 h-3.5 text-slate-500" />
                  <span>{t.reject_button}</span>
                </button>
                <button
                  onClick={() => handleDecision(task, "APPROVE")}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-semibold flex items-center space-x-1 rtl:space-x-reverse shadow-sm transition"
                >
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>{t.approve_button}</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
