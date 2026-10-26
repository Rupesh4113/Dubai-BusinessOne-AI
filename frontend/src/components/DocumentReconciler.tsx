"use client";

import React, { useState } from "react";
import { TRANSLATIONS } from "../lib/i18n";
import { LanguageCode } from "../lib/types";
import { reconcileInvoiceAPI } from "../lib/api";
import { Receipt, CheckCircle, AlertOctagon, Plus, Trash2 } from "lucide-react";

interface DocumentReconcilerProps {
  currentLang: LanguageCode;
}

export const DocumentReconciler: React.FC<DocumentReconcilerProps> = ({ currentLang }) => {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  const [invoiceNumber, setInvoiceNumber] = useState("INV-2026-901");
  const [vendorTRN, setVendorTRN] = useState("100234567890003");
  const [lineItems, setLineItems] = useState([
    { line_number: 1, description: "Consulting Services", quantity: 10, unit_price: 500, discount_amount: 0, vat_rate: 0.05, reported_line_total: 5000 },
    { line_number: 2, description: "Software Subscription", quantity: 2, unit_price: 1000, discount_amount: 0, vat_rate: 0.05, reported_line_total: 2000 },
  ]);
  const [reportedSubtotal, setReportedSubtotal] = useState(7000);
  const [reportedVAT, setReportedVAT] = useState(350);
  const [reportedGrandTotal, setReportedGrandTotal] = useState(7350);

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleReconcile = async () => {
    setLoading(true);
    try {
      const payload = {
        invoice_number: invoiceNumber,
        vendor_trn: vendorTRN,
        invoice_date: "2026-03-01",
        line_items: lineItems,
        reported_subtotal: reportedSubtotal,
        reported_vat_total: reportedVAT,
        reported_grand_total: reportedGrandTotal,
      };
      const res = await reconcileInvoiceAPI(payload);
      setResult(res);
    } catch (e: any) {
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
        <div className="flex items-center space-x-2 rtl:space-x-reverse text-slate-900 font-bold text-base">
          <Receipt className="w-5 h-5 text-sky-600" />
          <span>{t.tab_reconciler}</span>
        </div>
        <p className="text-xs text-slate-500">
          Independent line-item arithmetic verifier and UAE FTA 15-digit TRN compliance checker.
        </p>

        {/* Invoice Metadata */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div>
            <label className="block text-slate-600 mb-1">{t.invoice_number}</label>
            <input
              type="text"
              value={invoiceNumber}
              onChange={(e) => setInvoiceNumber(e.target.value)}
              className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 font-mono font-semibold"
            />
          </div>
          <div>
            <label className="block text-slate-600 mb-1">{t.vendor_trn}</label>
            <input
              type="text"
              value={vendorTRN}
              onChange={(e) => setVendorTRN(e.target.value)}
              className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 font-mono font-semibold"
            />
          </div>
        </div>

        {/* Line Items Table */}
        <div className="border border-slate-200 rounded-xl overflow-hidden">
          <table className="min-w-full text-xs text-left rtl:text-right">
            <thead className="bg-slate-50 text-slate-700 font-semibold text-[11px]">
              <tr>
                <th className="py-2 px-3">#</th>
                <th className="py-2 px-3">Description</th>
                <th className="py-2 px-3">Qty</th>
                <th className="py-2 px-3">Unit Price (AED)</th>
                <th className="py-2 px-3">Reported Line Total (AED)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {lineItems.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-50">
                  <td className="py-2 px-3 font-mono">{item.line_number}</td>
                  <td className="py-2 px-3">{item.description}</td>
                  <td className="py-2 px-3 font-mono">{item.quantity}</td>
                  <td className="py-2 px-3 font-mono">AED {item.unit_price}</td>
                  <td className="py-2 px-3 font-mono font-semibold">AED {item.reported_line_total}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Totals Section */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs bg-slate-50 p-3 rounded-xl border border-slate-200">
          <div>
            <span className="text-slate-500 block">Reported Subtotal:</span>
            <span className="font-bold text-slate-800 font-mono">AED {reportedSubtotal}</span>
          </div>
          <div>
            <span className="text-slate-500 block">Reported VAT (5%):</span>
            <span className="font-bold text-sky-700 font-mono">AED {reportedVAT}</span>
          </div>
          <div>
            <span className="text-slate-500 block">Reported Grand Total:</span>
            <span className="font-bold text-slate-900 font-mono">AED {reportedGrandTotal}</span>
          </div>
        </div>

        <button
          onClick={handleReconcile}
          disabled={loading}
          className="w-full bg-sky-600 hover:bg-sky-700 text-white font-medium py-2.5 rounded-xl transition text-xs shadow-sm"
        >
          {loading ? "Auditing Line Items..." : t.reconcile_action}
        </button>

        {/* Reconciliation Outcome */}
        {result && (
          <div
            className={`p-4 rounded-xl border ${
              result.is_valid && result.compliance_passed
                ? "bg-emerald-50/70 border-emerald-200"
                : "bg-rose-50/70 border-rose-200"
            } space-y-3`}
          >
            <div className="flex items-center space-x-2 rtl:space-x-reverse font-bold text-sm">
              {result.is_valid && result.compliance_passed ? (
                <>
                  <CheckCircle className="w-5 h-5 text-emerald-600" />
                  <span className="text-emerald-900">Reconciliation Succeeded — 100% Mathematical Match</span>
                </>
              ) : (
                <>
                  <AlertOctagon className="w-5 h-5 text-rose-600" />
                  <span className="text-rose-900">Discrepancy Detected — Compliance Variance</span>
                </>
              )}
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs font-mono">
              <div>Calculated Subtotal: <span className="font-bold">AED {result.calculated_subtotal}</span></div>
              <div>Calculated VAT: <span className="font-bold">AED {result.calculated_vat_total}</span></div>
              <div>Calculated Grand Total: <span className="font-bold">AED {result.calculated_grand_total}</span></div>
              <div>TRN Validation: <span className="font-bold">{result.trn_validation_status}</span></div>
            </div>

            {result.variances && result.variances.length > 0 && (
              <div className="space-y-1.5 text-xs text-rose-800 border-t border-rose-200 pt-2 font-sans">
                <span className="font-semibold block">Identified Discrepancies:</span>
                {result.variances.map((v: any, idx: number) => (
                  <div key={idx} className="bg-white/80 p-2 rounded border border-rose-200">
                    <span className="font-bold">[{v.severity}] {v.field_name}:</span> {v.explanation}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
