"""Direct Deterministic Calculator API Router."""

from fastapi import APIRouter
from ..calculator import (
    calculate_uae_vat,
    calculate_uae_corporate_tax,
    calculate_dubai_chamber_fee,
    calculate_dubai_det_fees,
    convert_currency,
    reconcile_invoice,
    VATCalculationRequest,
    VATCalculationResult,
    CorporateTaxRequest,
    CorporateTaxResult,
    DubaiChamberFeeRequest,
    DubaiChamberFeeResult,
    DubaiDETFeeRequest,
    DubaiDETFeeResult,
    CurrencyConversionRequest,
    CurrencyConversionResult,
    InvoiceReconciliationRequest,
    InvoiceReconciliationResult
)

router = APIRouter(prefix="/calculate", tags=["Deterministic Financial & Regulatory Engines"])


@router.post("/vat", response_model=VATCalculationResult)
def calculate_vat_endpoint(req: VATCalculationRequest):
    """Calculates UAE VAT (5%, Zero-Rated, Exempt) with statutory article citations."""
    return calculate_uae_vat(req)


@router.post("/corporate-tax", response_model=CorporateTaxResult)
def calculate_corporate_tax_endpoint(req: CorporateTaxRequest):
    """Calculates UAE Corporate Tax (0% up to AED 375k, 9% above, SBR, and Free Zone QFZP)."""
    return calculate_uae_corporate_tax(req)


@router.post("/dubai-chamber-fee", response_model=DubaiChamberFeeResult)
def calculate_chamber_fee_endpoint(req: DubaiChamberFeeRequest):
    """Calculates official Dubai Chamber of Commerce membership tariff."""
    return calculate_dubai_chamber_fee(req)


@router.post("/dubai-det-setup", response_model=DubaiDETFeeResult)
def calculate_det_fee_endpoint(req: DubaiDETFeeRequest):
    """Calculates Dubai Department of Economy and Tourism startup and license fees."""
    return calculate_dubai_det_fees(req)


@router.post("/currency", response_model=CurrencyConversionResult)
def convert_currency_endpoint(req: CurrencyConversionRequest):
    """Converts currencies using Central Bank of UAE fixed peg (USD/AED=3.6725) and daily rates."""
    return convert_currency(req)


@router.post("/reconcile-invoice", response_model=InvoiceReconciliationResult)
def reconcile_invoice_endpoint(req: InvoiceReconciliationRequest):
    """Performs line-item reconciliation, VAT checks, and TRN validation on commercial invoices."""
    return reconcile_invoice(req)
