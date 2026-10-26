"""Curated and verified official knowledge records for Dubai business operations."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class RegulatoryRecord(BaseModel):
    """Authoritative regulatory requirement record with complete citation metadata."""
    record_id: str
    category: str  # "BUSINESS_SETUP", "CHAMBER_MEMBERSHIP", "CORPORATE_TAX", "VAT", "LABOR_MOHRE"
    topic: str
    title: str
    summary: str
    detailed_rules: List[str]
    statutory_law: str
    issuing_authority: str
    source_id: str
    official_source_url: str
    effective_date: str
    tags: List[str]


VERIFIED_REGULATORY_RECORDS: List[RegulatoryRecord] = [
    RegulatoryRecord(
        record_id="REG-DED-LLC-001",
        category="BUSINESS_SETUP",
        topic="Dubai Mainland Limited Liability Company (LLC) Setup",
        title="100% Foreign Ownership Mainland LLC Formation",
        summary="Foreign investors can establish a 100% foreign-owned Mainland LLC in Dubai for over 1,000 commercial and industrial activities without requiring a UAE national shareholder.",
        detailed_rules=[
            "Federal Decree-Law No. (32) of 2021 on Commercial Companies amended the 51% local shareholder requirement.",
            "Initial approval from Dubai DET must be obtained prior to drafting the Memorandum of Association (MOA).",
            "A registered physical or virtual commercial lease (Ejari certificate) is mandatory for standard mainland licenses.",
            "Instant License option waives the lease requirement for the first year for eligible non-regulated activities.",
            "Mandatory automatic membership in Dubai Chamber of Commerce upon issuance of the commercial license."
        ],
        statutory_law="Federal Decree-Law No. (32) of 2021 on Commercial Companies & Dubai Law No. 13 of 2011",
        issuing_authority="Dubai Department of Economy and Tourism (DET)",
        source_id="DUBAI_DET",
        official_source_url="https://www.ded.ae/en/service-details/issue-initial-approval",
        effective_date="2021-06-01",
        tags=["mainland", "llc", "foreign_ownership", "trade_license", "commercial"]
    ),
    RegulatoryRecord(
        record_id="REG-CHAMBER-MEM-002",
        category="CHAMBER_MEMBERSHIP",
        topic="Dubai Chamber of Commerce Mandatory Membership",
        title="Dubai Chamber Registration & Annual Membership Fees",
        summary="All commercial, professional, and industrial entities licensed in Dubai are legally required to maintain active Dubai Chamber membership to conduct business and participate in international trade.",
        detailed_rules=[
            "Chamber membership is linked directly to the commercial license renewal cycle.",
            "Tier A LLCs (capital exceeding AED 500,000) pay AED 2,200 annually.",
            "Tier B LLCs (capital up to AED 500,000) pay AED 1,200 annually.",
            "Branches of foreign corporations pay AED 2,200 annually.",
            "Sole establishments and professional civil entities pay between AED 700 and AED 1,000.",
            "Members obtain Certificates of Origin, commercial dispute mediation, and international market access."
        ],
        statutory_law="Dubai Law No. (1) of 2022 on the Establishment of Dubai Chambers",
        issuing_authority="Dubai Chamber of Commerce",
        source_id="DUBAI_CHAMBER",
        official_source_url="https://www.dubaichamber.com/en/services/membership/",
        effective_date="2022-01-01",
        tags=["dubai_chamber", "membership", "fees", "certificate_of_origin", "export"]
    ),
    RegulatoryRecord(
        record_id="REG-FTA-CT-003",
        category="CORPORATE_TAX",
        topic="UAE Federal Corporate Tax Framework",
        title="Corporate Tax Rates, Brackets, and Small Business Relief",
        summary="UAE Corporate Tax applies to taxable persons at 0% on net profits up to AED 375,000, and 9% on net profits exceeding AED 375,000.",
        detailed_rules=[
            "Statutory rate: 0% up to AED 375,000; 9% on profits above AED 375,000.",
            "Small Business Relief (SBR) under Ministerial Decision No. 73 of 2023 allows resident taxable persons with revenue <= AED 3,000,000 to elect zero tax liability through tax periods ending on or before Dec 31, 2026.",
            "Qualifying Free Zone Persons (QFZPs) benefit from 0% on Qualifying Income provided they maintain adequate substance and derive non-qualifying revenue within the de minimis limit (lower of 5% of turnover or AED 5,000,000).",
            "All entities incorporated in the UAE must register for Corporate Tax with the FTA regardless of profit level."
        ],
        statutory_law="Federal Decree-Law No. 47 of 2022 on Taxation of Corporations and Businesses",
        issuing_authority="UAE Federal Tax Authority (FTA)",
        source_id="UAE_FTA",
        official_source_url="https://tax.gov.ae/en/corporate.tax.aspx",
        effective_date="2023-06-01",
        tags=["corporate_tax", "fta", "small_business_relief", "free_zone", "qfzp", "9%"]
    ),
    RegulatoryRecord(
        record_id="REG-FTA-VAT-004",
        category="VAT",
        topic="UAE Value Added Tax (VAT) Requirements",
        title="VAT Registration Thresholds and Mandatory Compliance",
        summary="Value Added Tax is levied at the standard rate of 5% on taxable supplies. Mandatory registration applies when taxable turnover exceeds AED 375,000 in the prior 12 months.",
        detailed_rules=[
            "Mandatory registration threshold: AED 375,000 turnover over previous 12 months or anticipated within 30 days.",
            "Voluntary registration threshold: AED 187,500 turnover or expenses.",
            "Standard rate: 5% on most commercial goods and consulting/professional services.",
            "Zero-rated supplies (0%): Direct exports of goods and services outside GCC implementing states, international transport, qualifying healthcare and education.",
            "Exempt supplies: Certain financial services and residential property leases.",
            "Tax Invoices must display the 15-digit Tax Registration Number (TRN) of the supplier."
        ],
        statutory_law="Federal Decree-Law No. (8) of 2017 on Value Added Tax",
        issuing_authority="UAE Federal Tax Authority (FTA)",
        source_id="UAE_FTA",
        official_source_url="https://tax.gov.ae/en/taxes/vat.aspx",
        effective_date="2018-01-01",
        tags=["vat", "trn", "tax_invoice", "fta", "5%"]
    ),
    RegulatoryRecord(
        record_id="REG-DED-INSTANT-005",
        category="BUSINESS_SETUP",
        topic="Dubai Instant License Scheme",
        title="Immediate Commercial License Issuance Without Ejari Year 1",
        summary="Eligible businesses can acquire a Dubai commercial license in a single electronic step without needing an office lease (Ejari) for the first year of operation.",
        detailed_rules=[
            "Applicable to selected commercial and professional activities that do not require external government approvals (e.g., General Trading, Management Consulting, IT Services).",
            "Exempts company from submitting an Ejari lease contract and Memorandum of Association during the initial 12-month period.",
            "Partners must possess verified UAE Pass digital identities.",
            "Dubai Municipality 5% tenancy market fee is waived for Year 1.",
            "Upon first-year renewal, an official Ejari registered commercial lease is mandatory."
        ],
        statutory_law="Dubai DET Executive Directive on Digital Commercial Licensing",
        issuing_authority="Dubai Department of Economy and Tourism (DET)",
        source_id="DUBAI_DET",
        official_source_url="https://www.ded.ae/en/instant-license",
        effective_date="2020-01-01",
        tags=["instant_license", "ejari_waiver", "fast_track", "det", "uae_pass"]
    )
]


def search_verified_knowledge(query: str, category: Optional[str] = None, max_results: int = 5) -> List[RegulatoryRecord]:
    """Semantic and keyword search over verified UAE regulatory records."""
    terms = [t.lower().strip() for t in query.split() if len(t.strip()) > 2]
    scored_results = []

    for record in VERIFIED_REGULATORY_RECORDS:
        if category and record.category.lower() != category.lower():
            continue

        score = 0
        searchable_text = f"{record.title} {record.topic} {record.summary} {' '.join(record.detailed_rules)} {' '.join(record.tags)} {record.statutory_law}".lower()

        for term in terms:
            if term in record.topic.lower() or term in record.title.lower():
                score += 5
            elif term in record.tags:
                score += 4
            elif term in searchable_text:
                score += 1

        if score > 0:
            scored_results.append((score, record))

    scored_results.sort(key=lambda x: x[0], reverse=True)
    return [rec for _, rec in scored_results[:max_results]]
