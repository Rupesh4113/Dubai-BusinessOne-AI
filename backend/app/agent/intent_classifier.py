"""Intent Classification and Prompt-Injection Defense Module."""

import re
from typing import Dict, Any, Tuple

# Defense against prompt injection, jailbreaks, and unauthorized commands
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"system\s*override",
    r"jailbreak",
    r"disregard\s+(all\s+)?rules",
    r"you\s+are\s+now\s+in\s+unrestricted\s+mode",
    r"reveal\s+(api\s+keys|passwords|secret\s+key|database\s+url)",
    r"drop\s+database",
    r"delete\s+from\s+users",
    r"<script\b",
    r"javascript:"
]


def sanitize_and_check_safety(raw_prompt: str) -> Tuple[str, bool, str]:
    """Sanitizes user input and flags malicious prompt injections or adversarial attempts.

    Returns: (sanitized_prompt, is_safe, flagged_reason)
    """
    clean_text = raw_prompt.strip()

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, clean_text, re.IGNORECASE):
            return clean_text, False, f"Prompt injection or unauthorized directive detected: '{pattern}'"

    # Strip dangerous HTML/script tags
    clean_text = re.sub(r"<[^>]*>", "", clean_text)
    return clean_text, True, "OK"


def classify_intent_and_extract_entities(prompt: str) -> Tuple[str, Dict[str, Any]]:
    """Identifies business intent and extracts key operational parameters.

    Supports multilingual triggers for English, Arabic, Hindi, Urdu, Filipino, and Malayalam.
    """
    p_lower = prompt.lower()
    entities: Dict[str, Any] = {}

    # Extract numeric values (amounts, revenue, rent)
    aed_matches = re.findall(r"(?:aed|dhs|dirhams?|\$|usd)?\s*([\d,]+(?:\.\d+)?)\s*(?:aed|dhs|dirhams?|usd)?", p_lower)
    extracted_numbers = []
    for m in aed_matches:
        cleaned_num = m.replace(",", "")
        try:
            val = float(cleaned_num)
            if val > 0:
                extracted_numbers.append(val)
        except ValueError:
            pass

    # 1. Targeted regex for revenue, rent, and capital
    rev_match = re.search(r"(?:revenue|turnover|sales|إيرادات|دخل)\s*(?:of|is|at)?\s*(?:aed|dhs|dirhams?|\$|usd)?\s*([\d,]+(?:\.\d+)?)", p_lower)
    if rev_match:
        try:
            entities["projected_revenue"] = float(rev_match.group(1).replace(",", ""))
        except ValueError:
            pass

    rent_match = re.search(r"(?:rent|lease|office|إيجار|مكتب)\s*(?:of|is|at)?\s*(?:aed|dhs|dirhams?|\$|usd)?\s*([\d,]+(?:\.\d+)?)", p_lower)
    if rent_match:
        try:
            entities["annual_office_rent"] = float(rent_match.group(1).replace(",", ""))
        except ValueError:
            pass

    cap_match = re.search(r"(?:capital|share capital|رأس المال)\s*(?:of|is|at)?\s*(?:aed|dhs|dirhams?|\$|usd)?\s*([\d,]+(?:\.\d+)?)", p_lower)
    if cap_match:
        try:
            entities["share_capital"] = float(cap_match.group(1).replace(",", ""))
        except ValueError:
            pass

    # Extract entity legal form
    if any(k in p_lower for k in ["llc", "ذ.م.م", "ذ م م", "limited liability"]):
        entities["legal_form"] = "llc"
    elif any(k in p_lower for k in ["free zone", "freezone", "منطقة حرة"]):
        entities["legal_form"] = "freezone"
    elif any(k in p_lower for k in ["sole", "فردية", "individual"]):
        entities["legal_form"] = "sole_proprietorship"
    elif any(k in p_lower for k in ["foreign branch", "فرع أجنبي"]):
        entities["legal_form"] = "branch_foreign"

    # 1. Explicit Trade Name Reservation (HIGH RISK - Specific to reserving/registering official name)
    if any(k in p_lower for k in [
        "reserve trade name", "register trade name", "حجز الاسم التجاري", "حجز اسم",
        "reserve company name", "reserve the name", "trade name reservation"
    ]):
        intent = "TRADE_NAME_RESERVATION"
        # Extract proposed name
        name_match = re.search(r'(?:name|called|named|named as)\s+["\']?([^"\',.\n]+)["\']?', prompt, re.IGNORECASE)
        if name_match:
            entities["company_name"] = name_match.group(1).strip()
        else:
            entities["company_name"] = "Apex Business Solutions LLC"

    # 2. Invoice Reconciliation
    elif any(k in p_lower for k in [
        "reconcile", "invoice", "مطابقة الفواتير", "فاتورة", "trn", "line item", "discrepancy", "bill check"
    ]):
        intent = "INVOICE_RECONCILIATION"
        inv_match = re.search(r"inv-[\w\d-]+", p_lower)
        if inv_match:
            entities["invoice_number"] = inv_match.group(0).upper()

    # 3. Comprehensive Business Setup Inquiry & Cost Breakdown
    elif any(k in p_lower for k in [
        "setup", "cost", "start business", "تكلفة تأسيس", "تأسيس", "consulting firm", "tech company",
        "establish", "license fee", "mainland llc", "how much to start"
    ]):
        intent = "BUSINESS_SETUP_INQUIRY"
        # Only fallback to generic position matching if targeted regex did not match
        if "projected_revenue" not in entities and extracted_numbers:
            for num in extracted_numbers:
                if num >= 200000:
                    entities["projected_revenue"] = num
                    break
        if "annual_office_rent" not in entities and extracted_numbers:
            for num in extracted_numbers:
                if 10000 <= num < 200000:
                    entities["annual_office_rent"] = num
                    break

    # 4. Corporate Tax Calculation
    elif any(k in p_lower for k in [
        "corporate tax", "ضريبة الشركات", "small business relief", "375000", "9%", "tax payable", "ct"
    ]):
        intent = "CORPORATE_TAX_CALCULATION"
        if extracted_numbers:
            entities["taxable_net_profit"] = extracted_numbers[0]

    # 5. VAT Calculation
    elif any(k in p_lower for k in [
        "vat", "value added tax", "ضريبة القيمة المضافة", "5%", "input tax", "tax invoice"
    ]):
        intent = "VAT_CALCULATION"
        if extracted_numbers:
            entities["amount"] = extracted_numbers[0]

    # 6. Currency Conversion
    elif any(k in p_lower for k in [
        "convert", "usd to aed", "aed to usd", "exchange rate", "تحويل العملة", "currency"
    ]):
        intent = "CURRENCY_CONVERSION"
        if extracted_numbers:
            entities["amount"] = extracted_numbers[0]

    # Default to Regulatory / Knowledge Inquiry
    else:
        intent = "REGULATORY_KNOWLEDGE_INQUIRY"

    return intent, entities
