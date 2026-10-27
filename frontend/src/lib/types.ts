export type LanguageCode = "en" | "ar" | "hi" | "ur" | "fil" | "ml";

export interface LanguageMeta {
  code: LanguageCode;
  label: string;
  nativeName: string;
  dir: "ltr" | "rtl";
}

export interface ChatMessage {
  id: string;
  sender: "user" | "agent";
  text: string;
  timestamp: string;
  taskState?: any;
  isCachedZeroInference?: boolean;
}

export interface CalculationStep {
  step_number: number;
  description: string;
  formula: string;
  intermediate_value: string;
  statutory_reference?: string;
}

export interface VATResult {
  base_amount: string;
  vat_rate_percent: string;
  vat_amount: string;
  total_amount: string;
  is_tax_inclusive: boolean;
  vat_category: string;
  apply_reverse_charge: boolean;
  currency: string;
  calculation_steps: CalculationStep[];
}

export interface CorporateTaxResult {
  taxable_net_profit: string;
  annual_revenue?: string;
  small_business_relief_eligible: boolean;
  small_business_relief_applied: boolean;
  tier1_exempt_amount: string;
  tier2_taxable_amount: string;
  effective_tax_rate_percent: string;
  total_tax_payable_aed: string;
  is_qualifying_free_zone_person: boolean;
  calculation_steps: CalculationStep[];
}

export interface DubaiDETFeeResult {
  license_type: string;
  initial_approval_fee_aed: string;
  trade_name_reservation_fee_aed: string;
  base_license_fee_aed: string;
  commercial_register_fee_aed: string;
  market_fee_aed: string;
  knowledge_and_innovation_dirham_aed: string;
  total_det_setup_cost_aed: string;
  calculation_steps: CalculationStep[];
}

export interface DubaiChamberFeeResult {
  legal_form: string;
  share_capital_aed: string;
  base_membership_fee_aed: string;
  certificate_and_verification_fee_aed: string;
  total_chamber_fee_aed: string;
  schedule_tier: string;
  renewal_cycle: string;
  calculation_steps: CalculationStep[];
}

export interface PendingTask {
  task_id: string;
  idempotency_key: string;
  tenant_id: string;
  user_id: string;
  action_name: string;
  risk_level: string;
  status: string;
  input_parameters: Record<string, any>;
  approval_token?: string;
  audit_notes: string[];
  created_at_epoch: number;
}
