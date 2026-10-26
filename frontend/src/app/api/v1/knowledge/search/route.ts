import { NextResponse } from "next/server";

const VERIFIED_RECORDS = [
  {
    record_id: "REG-DED-LLC-001",
    category: "BUSINESS_SETUP",
    topic: "Dubai Mainland Limited Liability Company (LLC) Setup",
    title: "100% Foreign Ownership Mainland LLC Formation",
    summary: "Foreign investors can establish a 100% foreign-owned Mainland LLC in Dubai for over 1,000 commercial and industrial activities without requiring a UAE national shareholder.",
    detailed_rules: [
      "Federal Decree-Law No. (32) of 2021 on Commercial Companies amended the 51% local shareholder requirement.",
      "Initial approval from Dubai DET must be obtained prior to drafting the Memorandum of Association (MOA).",
      "A registered physical or virtual commercial lease (Ejari certificate) is mandatory for standard mainland licenses.",
      "Instant License option waives the lease requirement for the first year for eligible non-regulated activities.",
      "Mandatory automatic membership in Dubai Chamber of Commerce upon issuance of the commercial license.",
    ],
    statutory_law: "Federal Decree-Law No. (32) of 2021 on Commercial Companies & Dubai Law No. 13 of 2011",
    issuing_authority: "Dubai Department of Economy and Tourism (DET)",
    source_id: "DUBAI_DET",
    official_source_url: "https://www.ded.ae/en/service-details/issue-initial-approval",
    tags: ["mainland", "llc", "foreign_ownership", "trade_license", "commercial"],
  },
  {
    record_id: "REG-CHAMBER-MEM-002",
    category: "CHAMBER_MEMBERSHIP",
    topic: "Dubai Chamber of Commerce Mandatory Membership",
    title: "Dubai Chamber Registration & Annual Membership Fees",
    summary: "All commercial, professional, and industrial entities licensed in Dubai are legally required to maintain active Dubai Chamber membership to conduct business and participate in international trade.",
    detailed_rules: [
      "Chamber membership is linked directly to the commercial license renewal cycle.",
      "Tier A LLCs (capital exceeding AED 500,000) pay AED 2,200 annually.",
      "Tier B LLCs (capital up to AED 500,000) pay AED 1,200 annually.",
      "Branches of foreign corporations pay AED 2,200 annually.",
      "Sole establishments and professional civil entities pay between AED 700 and AED 1,000.",
    ],
    statutory_law: "Dubai Law No. (1) of 2022 on the Establishment of Dubai Chambers",
    issuing_authority: "Dubai Chamber of Commerce",
    source_id: "DUBAI_CHAMBER",
    official_source_url: "https://www.dubaichamber.com/en/services/membership/",
    tags: ["dubai_chamber", "membership", "fees", "certificate_of_origin"],
  },
  {
    record_id: "REG-FTA-CT-003",
    category: "CORPORATE_TAX",
    topic: "UAE Federal Corporate Tax Framework",
    title: "Corporate Tax Rates, Brackets, and Small Business Relief",
    summary: "UAE Corporate Tax applies to taxable persons at 0% on net profits up to AED 375,000, and 9% on net profits exceeding AED 375,000.",
    detailed_rules: [
      "Statutory rate: 0% up to AED 375,000; 9% on profits above AED 375,000.",
      "Small Business Relief (SBR) under Ministerial Decision No. 73 of 2023 allows resident taxable persons with revenue <= AED 3,000,000 to elect zero tax liability.",
      "Qualifying Free Zone Persons (QFZPs) benefit from 0% on Qualifying Income with de minimis compliance.",
    ],
    statutory_law: "Federal Decree-Law No. 47 of 2022 on Taxation of Corporations and Businesses",
    issuing_authority: "UAE Federal Tax Authority (FTA)",
    source_id: "UAE_FTA",
    official_source_url: "https://tax.gov.ae/en/corporate.tax.aspx",
    tags: ["corporate_tax", "fta", "small_business_relief", "free_zone"],
  },
];

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const q = (searchParams.get("q") || "").toLowerCase();

  if (!q) return NextResponse.json(VERIFIED_RECORDS);

  const filtered = VERIFIED_RECORDS.filter(
    (r) =>
      r.title.toLowerCase().includes(q) ||
      r.summary.toLowerCase().includes(q) ||
      r.tags.some((tg) => tg.includes(q))
  );

  return NextResponse.json(filtered.length > 0 ? filtered : VERIFIED_RECORDS);
}
