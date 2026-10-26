"use client";

import React, { useState } from "react";
import { TRANSLATIONS } from "../lib/i18n";
import { LanguageCode } from "../lib/types";
import {
  calculateVAT,
  calculateCorporateTax,
  calculateDETSetup,
  calculateChamberFee,
} from "../lib/api";
import { Calculator, Check, ArrowRight, ShieldCheck, Scale, Coins } from "lucide-react";

interface CalculatorsViewProps {
  currentLang: LanguageCode;
}

export const CalculatorsView: React.FC<CalculatorsViewProps> = ({ currentLang }) => {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  // VAT state
  const [vatAmount, setVatAmount] = useState<number>(1000);
  const [isVatInclusive, setIsVatInclusive] = useState(false);
  const [vatResult, setVatResult] = useState<any>(null);

  // Corporate Tax state
  const [taxProfit, setTaxProfit] = useState<number>(1000000);
  const [taxRevenue, setTaxRevenue] = useState<number>(2500000);
  const [taxResult, setTaxResult] = useState<any>(null);

  // DET state
  const [detLicenseType, setDetLicenseType] = useState("commercial");
  const [detRent, setDetRent] = useState<number>(60000);
  const [detInstant, setDetInstant] = useState(false);
  const [detResult, setDetResult] = useState<any>(null);

  // Chamber state
  const [chamberLegalForm, setChamberLegalForm] = useState("llc");
  const [chamberCapital, setChamberCapital] = useState<number>(300000);
  const [chamberResult, setChamberResult] = useState<any>(null);

  const handleCalcVAT = async () => {
    try {
      const res = await calculateVAT(vatAmount, isVatInclusive);
      setVatResult(res);
    } catch (e) {}
  };

  const handleCalcCT = async () => {
    try {
      const res = await calculateCorporateTax(taxProfit, taxRevenue);
      setTaxResult(res);
    } catch (e) {}
  };

  const handleCalcDET = async () => {
    try {
      const res = await calculateDETSetup(detLicenseType, detRent, detInstant);
      setDetResult(res);
    } catch (e) {}
  };

  const handleCalcChamber = async () => {
    try {
      const res = await calculateChamberFee(chamberLegalForm, chamberCapital);
      setChamberResult(res);
    } catch (e) {}
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* 1. VAT Calculator */}
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
          <div className="flex items-center space-x-2 rtl:space-x-reverse text-slate-900 font-bold text-base">
            <Calculator className="w-5 h-5 text-sky-600" />
            <span>{t.calc_vat_title}</span>
          </div>
          <div className="space-y-3 text-xs">
            <div>
              <label className="block text-slate-600 mb-1">{t.amount}</label>
              <input
                type="number"
                value={vatAmount}
                onChange={(e) => setVatAmount(Number(e.target.value))}
                className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 font-semibold"
              />
            </div>
            <label className="flex items-center space-x-2 rtl:space-x-reverse cursor-pointer">
              <input
                type="checkbox"
                checked={isVatInclusive}
                onChange={(e) => setIsVatInclusive(e.target.checked)}
                className="rounded border-slate-300 text-sky-600"
              />
              <span className="text-slate-700">Tax-Inclusive Gross Base</span>
            </label>
            <button
              onClick={handleCalcVAT}
              className="w-full bg-sky-600 hover:bg-sky-700 text-white font-medium py-2 rounded-lg transition"
            >
              {t.calculate_now}
            </button>

            {vatResult && (
              <div className="mt-3 p-3 bg-sky-50/60 rounded-xl border border-sky-200 space-y-1 font-mono text-xs">
                <div className="flex justify-between">
                  <span>Net Base:</span>
                  <span className="font-bold">AED {vatResult.base_amount}</span>
                </div>
                <div className="flex justify-between text-sky-800">
                  <span>VAT (5%):</span>
                  <span className="font-bold">AED {vatResult.vat_amount}</span>
                </div>
                <div className="flex justify-between border-t border-sky-200 pt-1 text-slate-900 font-bold">
                  <span>Total Amount:</span>
                  <span>AED {vatResult.total_amount}</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* 2. Corporate Tax Calculator */}
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
          <div className="flex items-center space-x-2 rtl:space-x-reverse text-slate-900 font-bold text-base">
            <Scale className="w-5 h-5 text-indigo-600" />
            <span>{t.calc_tax_title}</span>
          </div>
          <div className="space-y-3 text-xs">
            <div>
              <label className="block text-slate-600 mb-1">{t.taxable_profit}</label>
              <input
                type="number"
                value={taxProfit}
                onChange={(e) => setTaxProfit(Number(e.target.value))}
                className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 font-semibold"
              />
            </div>
            <div>
              <label className="block text-slate-600 mb-1">{t.annual_revenue}</label>
              <input
                type="number"
                value={taxRevenue}
                onChange={(e) => setTaxRevenue(Number(e.target.value))}
                className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 font-semibold"
              />
            </div>
            <button
              onClick={handleCalcCT}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 rounded-lg transition"
            >
              {t.calculate_now}
            </button>

            {taxResult && (
              <div className="mt-3 p-3 bg-indigo-50/60 rounded-xl border border-indigo-200 space-y-1 font-mono text-xs">
                <div className="flex justify-between">
                  <span>Tier 1 Exempt (0% up to 375k):</span>
                  <span className="font-bold">AED {taxResult.tier1_exempt_amount}</span>
                </div>
                <div className="flex justify-between">
                  <span>Tier 2 Taxable (9%):</span>
                  <span className="font-bold">AED {taxResult.tier2_taxable_amount}</span>
                </div>
                <div className="flex justify-between border-t border-indigo-200 pt-1 text-slate-900 font-bold">
                  <span>Total Tax Payable:</span>
                  <span className="text-indigo-800">AED {taxResult.total_tax_payable_aed}</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* 3. DET Setup Fees */}
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
          <div className="flex items-center space-x-2 rtl:space-x-reverse text-slate-900 font-bold text-base">
            <Coins className="w-5 h-5 text-amber-600" />
            <span>{t.calc_det_title}</span>
          </div>
          <div className="space-y-3 text-xs">
            <div>
              <label className="block text-slate-600 mb-1">{t.license_type}</label>
              <select
                value={detLicenseType}
                onChange={(e) => setDetLicenseType(e.target.value)}
                className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 font-semibold"
              >
                <option value="commercial">Commercial License (Trading/General)</option>
                <option value="professional">Professional License (Consulting/Services)</option>
                <option value="industrial">Industrial License (Manufacturing)</option>
              </select>
            </div>
            <div>
              <label className="block text-slate-600 mb-1">{t.office_rent}</label>
              <input
                type="number"
                value={detRent}
                onChange={(e) => setDetRent(Number(e.target.value))}
                className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 font-semibold"
              />
            </div>
            <button
              onClick={handleCalcDET}
              className="w-full bg-amber-600 hover:bg-amber-700 text-white font-medium py-2 rounded-lg transition"
            >
              {t.calculate_now}
            </button>

            {detResult && (
              <div className="mt-3 p-3 bg-amber-50/60 rounded-xl border border-amber-200 space-y-1 font-mono text-xs">
                <div className="flex justify-between">
                  <span>Base License + Approvals:</span>
                  <span className="font-bold">AED {Number(detResult.base_license_fee_aed) + Number(detResult.initial_approval_fee_aed) + Number(detResult.trade_name_reservation_fee_aed)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Market Fee (5% Lease):</span>
                  <span className="font-bold">AED {detResult.market_fee_aed}</span>
                </div>
                <div className="flex justify-between border-t border-amber-200 pt-1 text-slate-900 font-bold">
                  <span>Total DET Startup Cost:</span>
                  <span className="text-amber-800">AED {detResult.total_det_setup_cost_aed}</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* 4. Chamber Membership Tariff */}
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
          <div className="flex items-center space-x-2 rtl:space-x-reverse text-slate-900 font-bold text-base">
            <ShieldCheck className="w-5 h-5 text-emerald-600" />
            <span>{t.calc_chamber_title}</span>
          </div>
          <div className="space-y-3 text-xs">
            <div>
              <label className="block text-slate-600 mb-1">{t.legal_form}</label>
              <select
                value={chamberLegalForm}
                onChange={(e) => setChamberLegalForm(e.target.value)}
                className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 font-semibold"
              >
                <option value="llc">Limited Liability Company (LLC)</option>
                <option value="branch_foreign">Branch of Foreign Corporation</option>
                <option value="branch_local">Branch of UAE Local Mainland Entity</option>
                <option value="sole_proprietorship">Sole Establishment / Professional</option>
              </select>
            </div>
            <div>
              <label className="block text-slate-600 mb-1">Declared Capital (AED)</label>
              <input
                type="number"
                value={chamberCapital}
                onChange={(e) => setChamberCapital(Number(e.target.value))}
                className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 font-semibold"
              />
            </div>
            <button
              onClick={handleCalcChamber}
              className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 rounded-lg transition"
            >
              {t.calculate_now}
            </button>

            {chamberResult && (
              <div className="mt-3 p-3 bg-emerald-50/60 rounded-xl border border-emerald-200 space-y-1 font-mono text-xs">
                <div className="flex justify-between">
                  <span>Schedule Tier:</span>
                  <span className="font-bold font-sans">{chamberResult.schedule_tier}</span>
                </div>
                <div className="flex justify-between">
                  <span>Base Membership:</span>
                  <span className="font-bold">AED {chamberResult.base_membership_fee_aed}</span>
                </div>
                <div className="flex justify-between border-t border-emerald-200 pt-1 text-slate-900 font-bold">
                  <span>Total Chamber Annual Fee:</span>
                  <span className="text-emerald-800">AED {chamberResult.total_chamber_fee_aed}</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
