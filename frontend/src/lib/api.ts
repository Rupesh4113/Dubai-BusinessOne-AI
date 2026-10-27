const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api/v1";

export async function sendAgentChat(prompt: string, language: string = "en", approvalToken?: string) {
  const res = await fetch(`${API_BASE}/agent/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prompt,
      language,
      approval_token: approvalToken || undefined,
    }),
  });
  if (!res.ok) {
    throw new Error(`API Error ${res.status}: ${await res.text()}`);
  }
  return res.json();
}

export async function fetchPendingApprovals() {
  const res = await fetch(`${API_BASE}/approvals/pending`);
  if (!res.ok) throw new Error("Failed to fetch pending approvals");
  return res.json();
}

export async function submitApprovalDecision(taskId: string, approvalToken: string, decision: "APPROVE" | "REJECT", comments?: string) {
  const res = await fetch(`${API_BASE}/approvals/decision`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      task_id: taskId,
      approval_token: approvalToken,
      decision,
      comments,
    }),
  });
  if (!res.ok) throw new Error(`Decision submission failed: ${await res.text()}`);
  return res.json();
}

export async function fetchTelemetry() {
  const res = await fetch(`${API_BASE}/agent/telemetry`);
  if (!res.ok) throw new Error("Failed to fetch telemetry");
  return res.json();
}

export async function fetchTasks(limit: number = 30) {
  const res = await fetch(`${API_BASE}/agent/tasks?limit=${limit}`);
  if (!res.ok) throw new Error("Failed to fetch tasks");
  return res.json();
}

export async function calculateVAT(amount: number, isTaxInclusive: boolean = false, vatCategory: string = "standard") {
  const res = await fetch(`${API_BASE}/calculate/vat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      amount,
      is_tax_inclusive: isTaxInclusive,
      vat_category: vatCategory,
    }),
  });
  return res.json();
}

export async function calculateCorporateTax(taxableNetProfit: number, annualRevenue?: number) {
  const res = await fetch(`${API_BASE}/calculate/corporate-tax`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      taxable_net_profit: taxableNetProfit,
      annual_revenue: annualRevenue || undefined,
    }),
  });
  return res.json();
}

export async function calculateDETSetup(licenseType: string, officeRent: number, isInstant: boolean = false) {
  const res = await fetch(`${API_BASE}/calculate/dubai-det-setup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      license_type: licenseType,
      annual_office_rent_aed: officeRent,
      is_instant_license: isInstant,
    }),
  });
  return res.json();
}

export async function calculateChamberFee(legalForm: string, shareCapital: number) {
  const res = await fetch(`${API_BASE}/calculate/dubai-chamber-fee`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      legal_form: legalForm,
      share_capital: shareCapital,
      is_new_registration: true,
    }),
  });
  return res.json();
}

export async function reconcileInvoiceAPI(invoicePayload: any) {
  const res = await fetch(`${API_BASE}/calculate/reconcile-invoice`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(invoicePayload),
  });
  return res.json();
}

export async function searchKnowledgeAPI(query: string) {
  const res = await fetch(`${API_BASE}/knowledge/search?q=${encodeURIComponent(query)}`);
  return res.json();
}
