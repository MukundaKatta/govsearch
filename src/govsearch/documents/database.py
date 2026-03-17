"""Document database with 50+ sample government documents."""

from __future__ import annotations

from datetime import date

from govsearch.documents.types import (
    DocumentStatus,
    DocumentType,
    Jurisdiction,
)
from govsearch.models import Citation, GovernmentDocument


class DocumentDatabase:
    """In-memory store for government documents with sample data."""

    def __init__(self, load_samples: bool = True) -> None:
        self._documents: dict[str, GovernmentDocument] = {}
        if load_samples:
            self._load_sample_documents()

    # ---- public API ----

    def add(self, doc: GovernmentDocument) -> None:
        self._documents[doc.doc_id] = doc

    def get(self, doc_id: str) -> GovernmentDocument | None:
        return self._documents.get(doc_id)

    def all_documents(self) -> list[GovernmentDocument]:
        return list(self._documents.values())

    def count(self) -> int:
        return len(self._documents)

    def remove(self, doc_id: str) -> bool:
        return self._documents.pop(doc_id, None) is not None

    def get_by_type(self, doc_type: DocumentType) -> list[GovernmentDocument]:
        return [d for d in self._documents.values() if d.doc_type == doc_type]

    def get_by_agency(self, agency: str) -> list[GovernmentDocument]:
        agency_lower = agency.lower()
        return [
            d for d in self._documents.values()
            if agency_lower in d.agency.lower()
        ]

    def search_title(self, query: str) -> list[GovernmentDocument]:
        q = query.lower()
        return [d for d in self._documents.values() if q in d.title.lower()]

    # ---- sample data ----

    def _load_sample_documents(self) -> None:
        samples = _build_sample_documents()
        for doc in samples:
            self._documents[doc.doc_id] = doc


def _build_sample_documents() -> list[GovernmentDocument]:
    """Build 50+ realistic sample government documents."""
    docs: list[GovernmentDocument] = []

    # --- LEGISLATION (10) ---
    docs.append(GovernmentDocument(
        doc_id="LEG-001", title="Clean Air Act Amendments of 2024",
        doc_type=DocumentType.LEGISLATION, agency="U.S. Congress",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 3, 15), date_effective=date(2024, 7, 1),
        summary="Comprehensive amendments strengthening air quality standards and expanding EPA enforcement authority under 42 U.S.C. 7401.",
        full_text="SECTION 1. Short Title. This Act may be cited as the 'Clean Air Act Amendments of 2024'. SECTION 2. Findings. The Congress finds that air pollution continues to pose significant risks to public health, as documented in EPA Report RPT-003. SECTION 3. Enhanced Standards. The Administrator shall revise National Ambient Air Quality Standards within 18 months. Particulate matter (PM2.5) limits reduced to 9 micrograms per cubic meter. SECTION 4. Enforcement. Civil penalties increased to $150,000 per day per violation. Reference: 42 U.S.C. 7413. SECTION 5. State Implementation Plans. Each state shall submit revised SIPs within 24 months of promulgation of revised standards. See also Executive Order 14057.",
        tags=["environment", "air quality", "EPA", "pollution", "public health"],
        citations=[Citation(source_doc_id="LEG-001", target_doc_id="RPT-003", target_title="EPA Air Quality Assessment Report")],
        related_docs=["REG-001", "EO-001", "RPT-003"],
    ))

    docs.append(GovernmentDocument(
        doc_id="LEG-002", title="Digital Privacy Protection Act",
        doc_type=DocumentType.LEGISLATION, agency="U.S. Congress",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 6, 1), date_effective=date(2025, 1, 1),
        summary="Establishes comprehensive federal data privacy framework for consumer protection in the digital economy.",
        full_text="SECTION 1. Short Title. This Act may be cited as the 'Digital Privacy Protection Act'. SECTION 2. Definitions. 'Covered entity' means any organization processing personal data of more than 50,000 individuals. 'Sensitive data' includes biometric, health, financial, and geolocation data. SECTION 3. Consumer Rights. Consumers have the right to access, correct, delete, and port their personal data. SECTION 4. Data Minimization. Covered entities shall collect only data reasonably necessary for the stated purpose. SECTION 5. Enforcement. The FTC shall enforce this Act. State attorneys general may bring civil actions. Penalties up to $50,000 per violation. See H.R. 4021 for related amendments.",
        tags=["privacy", "data protection", "technology", "FTC", "consumer rights"],
        related_docs=["REG-003", "CR-004"],
    ))

    docs.append(GovernmentDocument(
        doc_id="LEG-003", title="Infrastructure Investment and Modernization Act",
        doc_type=DocumentType.LEGISLATION, agency="U.S. Congress",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2023, 11, 20), date_effective=date(2024, 1, 1),
        summary="Authorizes $500 billion in federal spending for roads, bridges, broadband, and water systems over five years.",
        full_text="SECTION 1. Short Title. Infrastructure Investment and Modernization Act. SECTION 2. Authorization of Appropriations. There is authorized $500 billion over fiscal years 2024-2028, allocated: $200B surface transportation, $100B water infrastructure, $80B broadband expansion, $65B energy grid, $55B public transit. SECTION 3. Highway Trust Fund. The Highway Trust Fund under 23 U.S.C. 9503 is reauthorized through FY2028. SECTION 4. Broadband Equity. The NTIA shall administer grants ensuring broadband access in underserved areas. Reference: Pub. L. 117-58 for prior infrastructure investments. SECTION 5. Buy America Requirements. All iron, steel, and manufactured products used in projects shall be produced domestically per 41 U.S.C. 8301.",
        tags=["infrastructure", "transportation", "broadband", "water", "spending"],
        related_docs=["BUD-001", "RPT-005"],
    ))

    docs.append(GovernmentDocument(
        doc_id="LEG-004", title="Renewable Energy Transition Act",
        doc_type=DocumentType.LEGISLATION, agency="U.S. Congress",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 2, 10),
        summary="Sets binding targets for renewable energy adoption and provides tax incentives for clean energy development.",
        full_text="SECTION 1. Short Title. Renewable Energy Transition Act. SECTION 2. National Targets. 50 percent of electricity from renewable sources by 2030; 80 percent by 2040. SECTION 3. Tax Credits. Investment tax credit of 30 percent for solar, wind, and geothermal installations extended through 2035. Production tax credit of $26/MWh for qualifying facilities. SECTION 4. Grid Modernization. DOE shall establish grant programs for grid storage and smart grid technology. SECTION 5. Workforce Development. $5 billion authorized for clean energy workforce training programs. Reference: 26 U.S.C. 48 for existing energy tax credits.",
        tags=["energy", "renewable", "climate", "tax credits", "DOE"],
        related_docs=["REG-002", "EO-001", "BUD-002"],
    ))

    docs.append(GovernmentDocument(
        doc_id="LEG-005", title="Cybersecurity Enhancement Act of 2024",
        doc_type=DocumentType.LEGISLATION, agency="U.S. Congress",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 4, 22),
        summary="Strengthens federal cybersecurity requirements and establishes incident reporting mandates for critical infrastructure.",
        full_text="SECTION 1. Short Title. Cybersecurity Enhancement Act of 2024. SECTION 2. Critical Infrastructure Protection. Owners and operators of critical infrastructure shall implement baseline cybersecurity standards per NIST framework. SECTION 3. Incident Reporting. Covered entities must report significant cyber incidents to CISA within 72 hours. Ransomware payments reported within 24 hours. SECTION 4. Federal Systems. Each agency shall implement zero-trust architecture by FY2027. SECTION 5. Appropriations. $3.5 billion authorized for CISA operations and state/local cybersecurity grants. See Executive Order 14028 on improving federal cybersecurity.",
        tags=["cybersecurity", "CISA", "critical infrastructure", "federal IT"],
        related_docs=["EO-003", "REG-005"],
    ))

    docs.append(GovernmentDocument(
        doc_id="LEG-006", title="California Consumer Data Protection Act",
        doc_type=DocumentType.LEGISLATION, agency="California State Legislature",
        jurisdiction=Jurisdiction.STATE, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 9, 15), date_effective=date(2025, 7, 1),
        summary="Expands California consumer privacy protections with AI transparency and data broker registration requirements.",
        full_text="SECTION 1. Title. California Consumer Data Protection Act. SECTION 2. AI Transparency. Businesses deploying automated decision-making shall provide consumers with meaningful information about the logic involved. SECTION 3. Data Brokers. Data brokers must register with the California Privacy Protection Agency and allow consumer opt-out. SECTION 4. Children's Data. Enhanced protections for data of individuals under 18. SECTION 5. Penalties. Violations subject to fines of $7,500 per intentional violation. California Attorney General and CPPA share enforcement authority.",
        tags=["privacy", "AI", "California", "data brokers", "consumer protection"],
        related_docs=["LEG-002"],
    ))

    docs.append(GovernmentDocument(
        doc_id="LEG-007", title="National AI Research and Innovation Act",
        doc_type=DocumentType.LEGISLATION, agency="U.S. Congress",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 7, 30),
        summary="Establishes National AI Research Resource and invests in responsible AI development and workforce training.",
        full_text="SECTION 1. Short Title. National AI Research and Innovation Act. SECTION 2. National AI Research Resource. NSF shall establish a shared computing infrastructure for AI research accessible to academia and nonprofits. SECTION 3. AI Safety Institute. NIST AI Safety Institute authorized with $500M over 5 years for AI evaluation and standards. SECTION 4. Workforce. $2B for AI and STEM education programs. SECTION 5. International Cooperation. State Department shall coordinate AI governance frameworks with allied nations. Reference: Executive Order 14110 on Safe AI.",
        tags=["AI", "research", "NIST", "NSF", "workforce", "technology"],
        related_docs=["EO-005", "RPT-008"],
    ))

    docs.append(GovernmentDocument(
        doc_id="LEG-008", title="Federal Water Quality Improvement Act",
        doc_type=DocumentType.LEGISLATION, agency="U.S. Congress",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2023, 8, 5),
        summary="Updates Clean Water Act standards for PFAS contamination and lead pipe replacement funding.",
        full_text="SECTION 1. Short Title. Federal Water Quality Improvement Act. SECTION 2. PFAS Standards. EPA shall establish maximum contaminant levels for PFAS compounds within 2 years. Limit: 4 parts per trillion for PFOA and PFOS. SECTION 3. Lead Pipe Replacement. $15 billion for nationwide lead service line replacement. Priority given to disadvantaged communities. SECTION 4. Agricultural Runoff. Strengthened nutrient management requirements for concentrated animal feeding operations. Reference: 33 U.S.C. 1251 (Clean Water Act). SECTION 5. Funding. EPA Clean Water State Revolving Fund increased by $5 billion annually.",
        tags=["water quality", "PFAS", "lead pipes", "EPA", "environment"],
        related_docs=["REG-004", "RPT-006"],
    ))

    docs.append(GovernmentDocument(
        doc_id="LEG-009", title="Veterans Healthcare Modernization Act",
        doc_type=DocumentType.LEGISLATION, agency="U.S. Congress",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 5, 28),
        summary="Expands VA healthcare services including mental health, telehealth, and community care access.",
        full_text="SECTION 1. Short Title. Veterans Healthcare Modernization Act. SECTION 2. Mental Health Services. VA shall expand mental health staffing by 5,000 providers. Suicide prevention programs receive $1.5B. SECTION 3. Telehealth Expansion. Telehealth services available to all enrolled veterans regardless of location. SECTION 4. Community Care. Veterans may access community providers when VA wait times exceed 20 days or travel exceeds 30 minutes. SECTION 5. Electronic Health Records. $3B for completion of VA EHR modernization. Reference: 38 U.S.C. 1710 for VA healthcare eligibility.",
        tags=["veterans", "healthcare", "VA", "mental health", "telehealth"],
        related_docs=["BUD-003", "RPT-007"],
    ))

    docs.append(GovernmentDocument(
        doc_id="LEG-010", title="Small Business Innovation Incentive Act",
        doc_type=DocumentType.LEGISLATION, agency="U.S. Congress",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 1, 18),
        summary="Expands SBIR/STTR programs and provides tax incentives for small business R&D investment.",
        full_text="SECTION 1. Short Title. Small Business Innovation Incentive Act. SECTION 2. SBIR Expansion. SBIR allocation increased from 3.2% to 4.0% of extramural R&D budgets. SECTION 3. Tax Credits. R&D tax credit for small businesses (under 500 employees) doubled to 20% of qualified expenses. SECTION 4. Venture Capital. SBA authorized to guarantee up to $2B in venture loans for technology startups. SECTION 5. Regulatory Relief. One-year compliance grace period for small businesses subject to new federal regulations. Reference: 15 U.S.C. 638 (SBIR authorization).",
        tags=["small business", "innovation", "SBIR", "tax credits", "SBA"],
        related_docs=["BUD-004"],
    ))

    # --- REGULATIONS (8) ---
    docs.append(GovernmentDocument(
        doc_id="REG-001", title="National Ambient Air Quality Standards: PM2.5 Update",
        doc_type=DocumentType.REGULATION, agency="Environmental Protection Agency",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 5, 1), date_effective=date(2024, 8, 1),
        summary="Final rule lowering the annual PM2.5 standard from 12 to 9 micrograms per cubic meter.",
        full_text="ENVIRONMENTAL PROTECTION AGENCY. 40 CFR Parts 50 and 58. National Ambient Air Quality Standards for Particulate Matter. SECTION 1. Background. Pursuant to Clean Air Act Section 109, 42 U.S.C. 7409, EPA is revising NAAQS for PM2.5. SECTION 2. Revised Standards. The primary annual PM2.5 standard is revised to 9.0 ug/m3. The 24-hour standard remains at 35 ug/m3. SECTION 3. Implementation Timeline. States shall submit revised SIPs within 24 months. Attainment deadline: 2032 for Moderate areas, 2037 for Serious areas. SECTION 4. Monitoring. Enhanced monitoring required in environmental justice communities per Executive Order 14057.",
        tags=["air quality", "PM2.5", "EPA", "NAAQS", "environment"],
        related_docs=["LEG-001", "EO-001"],
    ))

    docs.append(GovernmentDocument(
        doc_id="REG-002", title="Renewable Fuel Standard: 2025 Volume Requirements",
        doc_type=DocumentType.REGULATION, agency="Environmental Protection Agency",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 6, 15),
        summary="Establishes 2025 renewable fuel volume obligations under the Clean Air Act.",
        full_text="ENVIRONMENTAL PROTECTION AGENCY. 40 CFR Part 80. Renewable Fuel Standard Program. SECTION 1. Volume Requirements. Total renewable fuel: 22.33 billion gallons. Advanced biofuel: 7.43 billion gallons. Cellulosic biofuel: 1.75 billion gallons. Biomass-based diesel: 3.35 billion gallons. SECTION 2. Compliance. Obligated parties shall demonstrate compliance through Renewable Identification Numbers (RINs). SECTION 3. Small Refinery Exemptions. Exemptions available upon demonstration of disproportionate economic hardship. Reference: 42 U.S.C. 7545(o).",
        tags=["renewable fuel", "biofuel", "EPA", "RFS", "energy"],
        related_docs=["LEG-004"],
    ))

    docs.append(GovernmentDocument(
        doc_id="REG-003", title="FTC Data Privacy Rule: Consumer Data Rights",
        doc_type=DocumentType.REGULATION, agency="Federal Trade Commission",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.PROPOSED,
        date_published=date(2024, 8, 20),
        summary="Proposed rule implementing consumer data rights under the Digital Privacy Protection Act.",
        full_text="FEDERAL TRADE COMMISSION. 16 CFR Part 314. Trade Regulation Rule on Consumer Data Rights. SECTION 1. Scope. Applies to covered entities as defined in the Digital Privacy Protection Act (LEG-002). SECTION 2. Access Requests. Covered entities must respond to consumer access requests within 30 days. SECTION 3. Deletion. Data deletion must be completed within 45 days and confirmed in writing. SECTION 4. Data Portability. Data provided in machine-readable, interoperable format. SECTION 5. Record Keeping. Entities shall maintain records of all data rights requests for 3 years.",
        tags=["privacy", "FTC", "consumer data", "data rights", "regulation"],
        related_docs=["LEG-002"],
    ))

    docs.append(GovernmentDocument(
        doc_id="REG-004", title="PFAS National Primary Drinking Water Regulation",
        doc_type=DocumentType.REGULATION, agency="Environmental Protection Agency",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 4, 10), date_effective=date(2024, 6, 10),
        summary="First-ever national drinking water standard for six PFAS compounds.",
        full_text="ENVIRONMENTAL PROTECTION AGENCY. 40 CFR Part 141. National Primary Drinking Water Regulations for PFAS. SECTION 1. Maximum Contaminant Levels. PFOA: 4 ppt. PFOS: 4 ppt. PFHxS: 10 ppt. PFNA: 10 ppt. GenX: 10 ppt. Mixture of PFAS: Hazard Index of 1. SECTION 2. Monitoring. Public water systems shall begin monitoring within 3 years. SECTION 3. Compliance. Systems exceeding MCLs must install treatment within 5 years. SECTION 4. Funding. $9 billion available through Drinking Water SRF for PFAS treatment. Reference: Safe Drinking Water Act, 42 U.S.C. 300f.",
        tags=["PFAS", "drinking water", "EPA", "contaminants", "public health"],
        related_docs=["LEG-008", "RPT-006"],
    ))

    docs.append(GovernmentDocument(
        doc_id="REG-005", title="CISA Cybersecurity Incident Reporting Rule",
        doc_type=DocumentType.REGULATION, agency="Cybersecurity and Infrastructure Security Agency",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 9, 5),
        summary="Implements mandatory cyber incident reporting for critical infrastructure entities.",
        full_text="DEPARTMENT OF HOMELAND SECURITY. 6 CFR Part 826. Cyber Incident Reporting for Critical Infrastructure Act Implementation. SECTION 1. Covered Entities. Critical infrastructure sectors as defined in Presidential Policy Directive 21. SECTION 2. Reporting Requirements. Substantial cyber incidents reported to CISA within 72 hours. Ransomware payments within 24 hours. SECTION 3. Report Contents. Incident description, affected systems, indicators of compromise, response actions taken. SECTION 4. Protections. Reports are exempt from FOIA and cannot be used in regulatory enforcement against the reporting entity.",
        tags=["cybersecurity", "CISA", "incident reporting", "critical infrastructure"],
        related_docs=["LEG-005", "EO-003"],
    ))

    docs.append(GovernmentDocument(
        doc_id="REG-006", title="SEC Climate Risk Disclosure Rule",
        doc_type=DocumentType.REGULATION, agency="Securities and Exchange Commission",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 3, 6),
        summary="Requires public companies to disclose climate-related risks and greenhouse gas emissions.",
        full_text="SECURITIES AND EXCHANGE COMMISSION. 17 CFR Parts 210, 229, 230, 232, 239, 249. Enhancement and Standardization of Climate-Related Disclosures. SECTION 1. Climate Risk Disclosure. Registrants must disclose material climate risks in annual reports. SECTION 2. GHG Emissions. Large accelerated filers: Scope 1 and 2 emissions, with assurance. Accelerated filers: Scope 1 and 2 without assurance initially. SECTION 3. Financial Impact. Quantify climate-related impacts exceeding 1% of relevant financial statement line items. SECTION 4. Transition Plans. Disclose any climate transition plans, targets, and goals.",
        tags=["climate disclosure", "SEC", "emissions", "ESG", "financial regulation"],
        related_docs=["EO-004"],
    ))

    docs.append(GovernmentDocument(
        doc_id="REG-007", title="FDA Artificial Intelligence in Medical Devices",
        doc_type=DocumentType.REGULATION, agency="Food and Drug Administration",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.PROPOSED,
        date_published=date(2024, 7, 12),
        summary="Proposed framework for regulation of AI/ML-enabled medical devices including continuous learning systems.",
        full_text="DEPARTMENT OF HEALTH AND HUMAN SERVICES. 21 CFR Part 820. AI/ML-Enabled Medical Devices. SECTION 1. Scope. Applies to devices using artificial intelligence or machine learning for diagnosis, treatment recommendations, or clinical decision support. SECTION 2. Pre-market Review. Predetermined change control plans required for adaptive AI algorithms. SECTION 3. Transparency. Labeling shall include description of AI training data, performance metrics, and known limitations. SECTION 4. Post-market Surveillance. Manufacturers shall monitor real-world performance and report algorithmic drift. SECTION 5. Cybersecurity. AI medical devices must meet cybersecurity requirements per 21 CFR 860.",
        tags=["AI", "medical devices", "FDA", "machine learning", "healthcare"],
        related_docs=["LEG-007", "EO-005"],
    ))

    docs.append(GovernmentDocument(
        doc_id="REG-008", title="DOL Overtime Protection Rule Update",
        doc_type=DocumentType.REGULATION, agency="Department of Labor",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 4, 23), date_effective=date(2024, 7, 1),
        summary="Raises salary threshold for overtime exemption under the Fair Labor Standards Act.",
        full_text="DEPARTMENT OF LABOR. 29 CFR Part 541. Defining and Delimiting the Exemptions for Executive, Administrative, Professional, and Outside Sales Employees. SECTION 1. Salary Level. Minimum salary for exemption raised to $58,656 annually ($1,128/week). SECTION 2. Highly Compensated Employees. HCE threshold raised to $151,164 annually. SECTION 3. Automatic Updates. Salary thresholds updated every 3 years based on wage data. SECTION 4. Duties Test. No changes to existing duties tests for white-collar exemptions. Reference: 29 U.S.C. 213(a)(1).",
        tags=["overtime", "labor", "FLSA", "wages", "employment"],
    ))

    # --- COURT RULINGS (6) ---
    docs.append(GovernmentDocument(
        doc_id="CR-001", title="United States v. TechCorp Inc. - Data Monopoly Case",
        doc_type=DocumentType.COURT_RULING, agency="U.S. District Court, D.C.",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 8, 15),
        summary="Landmark antitrust ruling finding major technology company maintained illegal monopoly in digital advertising.",
        full_text="UNITED STATES DISTRICT COURT FOR THE DISTRICT OF COLUMBIA. Case No. 1:23-cv-01234. OPINION AND ORDER. Judge Richardson presiding. I. BACKGROUND. The United States alleges that TechCorp maintained monopoly power in digital advertising through exclusionary contracts and acquisitions. II. FINDINGS OF FACT. TechCorp controls 74% of the ad-tech stack market. Exclusive default agreements with device manufacturers foreclosed competition. III. CONCLUSIONS OF LAW. Under Section 2 of the Sherman Act, 15 U.S.C. 2, TechCorp's conduct constitutes unlawful monopolization. IV. REMEDY. Structural remedies to be determined. Parties shall submit proposed remedy frameworks within 90 days. Reference: 370 F. Supp. 3d 1121.",
        tags=["antitrust", "technology", "monopoly", "advertising", "Sherman Act"],
        related_docs=["CR-005"],
    ))

    docs.append(GovernmentDocument(
        doc_id="CR-002", title="EPA v. Industrial Solvents LLC - Clean Water Enforcement",
        doc_type=DocumentType.COURT_RULING, agency="U.S. Court of Appeals, 4th Circuit",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 3, 22),
        summary="Upheld EPA enforcement action and $45 million penalty for PFAS contamination of waterways.",
        full_text="UNITED STATES COURT OF APPEALS FOR THE FOURTH CIRCUIT. No. 23-1847. EPA v. Industrial Solvents LLC. I. PROCEDURAL HISTORY. EPA brought enforcement action under CWA Section 311, 33 U.S.C. 1321, for discharge of PFAS into the Cape Fear River. District court found liability and assessed $45M penalty. II. ANALYSIS. Defendant argues PFAS were not 'hazardous substances' at time of discharge. We disagree. EPA's designation of PFAS as hazardous under CERCLA applies retroactively. III. CONCLUSION. District court judgment AFFIRMED. Penalty of $45,000,000 upheld as proportionate given scope of contamination affecting 300,000 residents.",
        tags=["PFAS", "Clean Water Act", "EPA", "enforcement", "contamination"],
        related_docs=["REG-004", "LEG-008"],
    ))

    docs.append(GovernmentDocument(
        doc_id="CR-003", title="State of Texas v. Federal Energy Regulatory Commission",
        doc_type=DocumentType.COURT_RULING, agency="U.S. Court of Appeals, 5th Circuit",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 6, 10),
        summary="Vacated FERC rule on regional transmission planning, finding exceeded statutory authority.",
        full_text="UNITED STATES COURT OF APPEALS FOR THE FIFTH CIRCUIT. No. 23-60471. State of Texas et al. v. FERC. I. BACKGROUND. FERC Order No. 2023 required regional transmission organizations to conduct long-range planning for renewable energy integration. Texas and several states challenge as exceeding FERC jurisdiction. II. ANALYSIS. Under the Federal Power Act, 16 U.S.C. 824, FERC's authority over transmission planning does not extend to mandating specific generation resource assumptions. III. HOLDING. FERC Order No. 2023 VACATED AND REMANDED. FERC may establish planning processes but may not predetermine generation outcomes.",
        tags=["energy", "FERC", "transmission", "federalism", "regulatory authority"],
        related_docs=["LEG-004", "REG-002"],
    ))

    docs.append(GovernmentDocument(
        doc_id="CR-004", title="Citizens for Digital Rights v. DataBroker Inc.",
        doc_type=DocumentType.COURT_RULING, agency="U.S. District Court, N.D. California",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 10, 5),
        summary="Class action settlement establishing precedent for consumer data deletion rights and broker accountability.",
        full_text="UNITED STATES DISTRICT COURT, NORTHERN DISTRICT OF CALIFORNIA. Case No. 3:23-cv-05678. CLASS ACTION SETTLEMENT APPROVAL. I. OVERVIEW. Plaintiff class of 2.3 million consumers whose location data was sold without consent. II. SETTLEMENT TERMS. DataBroker to pay $125M to class members. Delete all non-consensual data within 90 days. Implement opt-in consent framework. Submit to 5-year compliance monitoring. III. COURT ANALYSIS. Settlement is fair, reasonable, and adequate under Fed. R. Civ. P. 23(e). Injunctive relief addresses systemic privacy harms beyond monetary compensation. APPROVED.",
        tags=["privacy", "data broker", "class action", "consumer rights", "data deletion"],
        related_docs=["LEG-002", "LEG-006"],
    ))

    docs.append(GovernmentDocument(
        doc_id="CR-005", title="FTC v. MegaMerge Corp - Merger Challenge",
        doc_type=DocumentType.COURT_RULING, agency="U.S. District Court, S.D. New York",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 5, 18),
        summary="Granted FTC preliminary injunction blocking $28 billion technology acquisition on antitrust grounds.",
        full_text="UNITED STATES DISTRICT COURT, SOUTHERN DISTRICT OF NEW YORK. Case No. 1:24-cv-00891. FTC v. MegaMerge Corp. PRELIMINARY INJUNCTION. I. STANDARD. Under Section 13(b) of the FTC Act, 15 U.S.C. 53(b). II. LIKELIHOOD OF SUCCESS. FTC demonstrates the proposed acquisition would substantially lessen competition in the cloud computing market. Combined entity would control 62% market share. III. BALANCE OF EQUITIES. Public interest in competitive markets outweighs private interest in completing transaction. IV. ORDER. Proposed acquisition ENJOINED pending full administrative proceedings. Reference: Clayton Act Section 7, 15 U.S.C. 18.",
        tags=["antitrust", "merger", "FTC", "technology", "cloud computing"],
        related_docs=["CR-001"],
    ))

    docs.append(GovernmentDocument(
        doc_id="CR-006", title="National Labor Relations Board v. GigWork Platform",
        doc_type=DocumentType.COURT_RULING, agency="U.S. Court of Appeals, 9th Circuit",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 11, 2),
        summary="Affirmed NLRB finding that gig platform workers are employees entitled to collective bargaining rights.",
        full_text="UNITED STATES COURT OF APPEALS FOR THE NINTH CIRCUIT. No. 23-55912. NLRB v. GigWork Platform Inc. I. QUESTION PRESENTED. Whether app-based workers are 'employees' under Section 2(3) of the National Labor Relations Act, 29 U.S.C. 152(3). II. ANALYSIS. Applying the common-law agency test, the platform exercises sufficient control over workers through algorithmic management, fare setting, and deactivation authority. III. HOLDING. Workers are employees under the NLRA. NLRB order requiring good-faith bargaining ENFORCED. IV. CONCURRENCE. Judge Lee concurs, noting Congress should provide clearer statutory guidance for the platform economy.",
        tags=["labor", "gig economy", "NLRB", "employment", "collective bargaining"],
        related_docs=["REG-008"],
    ))

    # --- EXECUTIVE ORDERS (6) ---
    docs.append(GovernmentDocument(
        doc_id="EO-001", title="Executive Order on Strengthening Environmental Justice",
        doc_type=DocumentType.EXECUTIVE_ORDER, agency="Executive Office of the President",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 1, 27),
        summary="Directs federal agencies to address disproportionate environmental burdens on disadvantaged communities.",
        full_text="EXECUTIVE ORDER 14150. Strengthening Environmental Justice for All Communities. By the authority vested in me as President by the Constitution and the laws of the United States. SECTION 1. Policy. It is the policy of this Administration that every person deserves clean air, clean water, and freedom from harmful pollution. SECTION 2. Justice40 Enhancement. 40 percent of benefits from federal climate and environmental investments shall flow to disadvantaged communities. SECTION 3. Cumulative Impacts. EPA shall develop methodology for assessing cumulative environmental and health impacts. SECTION 4. Enforcement. DOJ shall prioritize environmental justice cases. SECTION 5. Interagency Council. White House Environmental Justice Council shall coordinate implementation across agencies.",
        tags=["environmental justice", "equity", "EPA", "climate", "communities"],
        related_docs=["LEG-001", "REG-001"],
    ))

    docs.append(GovernmentDocument(
        doc_id="EO-002", title="Executive Order on Strengthening American Manufacturing",
        doc_type=DocumentType.EXECUTIVE_ORDER, agency="Executive Office of the President",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 3, 5),
        summary="Enhances Buy America requirements and establishes new incentives for domestic semiconductor and critical mineral production.",
        full_text="EXECUTIVE ORDER 14155. Strengthening American Manufacturing and Supply Chains. SECTION 1. Policy. American manufacturing is essential to national security and economic resilience. SECTION 2. Buy America. All federal procurement shall apply enhanced domestic content requirements: 75% domestic content by 2029. SECTION 3. Semiconductors. Commerce Department shall accelerate CHIPS Act implementation with $10B in additional manufacturing incentives. SECTION 4. Critical Minerals. DOI and DOE shall fast-track permitting for domestic critical mineral extraction, with environmental safeguards. SECTION 5. Workforce. Labor Department shall expand registered apprenticeship programs in advanced manufacturing.",
        tags=["manufacturing", "Buy America", "semiconductors", "supply chain", "trade"],
        related_docs=["LEG-003"],
    ))

    docs.append(GovernmentDocument(
        doc_id="EO-003", title="Executive Order on National Cybersecurity Strategy Implementation",
        doc_type=DocumentType.EXECUTIVE_ORDER, agency="Executive Office of the President",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 2, 15),
        summary="Directs implementation of zero-trust architecture across federal systems and strengthens public-private cybersecurity cooperation.",
        full_text="EXECUTIVE ORDER 14152. National Cybersecurity Strategy Implementation. SECTION 1. Policy. Cybersecurity is a national security imperative. SECTION 2. Zero Trust. All federal agencies shall implement zero-trust architecture per NIST SP 800-207 by end of FY2026. SECTION 3. Software Security. Government contractors must attest to secure software development practices. Software bills of materials (SBOMs) required for all critical software. SECTION 4. Quantum Readiness. Agencies shall inventory cryptographic systems and begin migration to post-quantum cryptography. SECTION 5. Public-Private Partnership. CISA shall establish sector-specific cybersecurity performance goals.",
        tags=["cybersecurity", "zero trust", "quantum", "NIST", "national security"],
        related_docs=["LEG-005", "REG-005"],
    ))

    docs.append(GovernmentDocument(
        doc_id="EO-004", title="Executive Order on Climate-Related Financial Risk",
        doc_type=DocumentType.EXECUTIVE_ORDER, agency="Executive Office of the President",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 4, 2),
        summary="Directs federal agencies and financial regulators to assess and mitigate climate-related financial risks.",
        full_text="EXECUTIVE ORDER 14158. Climate-Related Financial Risk. SECTION 1. Policy. Climate change poses systemic risks to the U.S. financial system and federal budget. SECTION 2. Federal Lending. Federal lending programs shall incorporate climate risk into underwriting standards within 18 months. SECTION 3. Insurance. FEMA and Treasury shall assess climate risk to the National Flood Insurance Program and federal crop insurance. SECTION 4. Budget. OMB shall integrate climate risk into federal budget projections and agency capital planning. SECTION 5. Financial Stability. FSOC shall publish annual climate financial stability assessment.",
        tags=["climate risk", "financial regulation", "FSOC", "insurance", "budget"],
        related_docs=["REG-006", "BUD-005"],
    ))

    docs.append(GovernmentDocument(
        doc_id="EO-005", title="Executive Order on Safe, Secure, and Trustworthy AI",
        doc_type=DocumentType.EXECUTIVE_ORDER, agency="Executive Office of the President",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 10, 30),
        summary="Establishes comprehensive framework for AI safety, including testing requirements for frontier models and government AI use guidelines.",
        full_text="EXECUTIVE ORDER 14170. Safe, Secure, and Trustworthy Artificial Intelligence. SECTION 1. Purpose. AI offers extraordinary potential but also presents risks requiring proactive governance. SECTION 2. Safety Testing. Developers of dual-use foundation models exceeding 10^26 FLOP training compute shall report safety test results to the Department of Commerce. SECTION 3. Government Use. OMB shall issue guidance on responsible AI use by federal agencies within 120 days. SECTION 4. Workforce. Agencies shall assess AI's impact on their workforce and develop mitigation strategies. SECTION 5. Civil Rights. DOJ and civil rights agencies shall monitor AI for discrimination in housing, lending, and employment. SECTION 6. International Standards. State Department shall lead AI governance negotiations in multilateral forums.",
        tags=["AI", "safety", "governance", "civil rights", "technology"],
        related_docs=["LEG-007", "REG-007", "RPT-008"],
    ))

    docs.append(GovernmentDocument(
        doc_id="EO-006", title="Executive Order on Reducing Prescription Drug Costs",
        doc_type=DocumentType.EXECUTIVE_ORDER, agency="Executive Office of the President",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 6, 20),
        summary="Directs HHS to expand Medicare drug price negotiation and increase pharmaceutical supply chain transparency.",
        full_text="EXECUTIVE ORDER 14162. Reducing Prescription Drug Costs for Americans. SECTION 1. Policy. No American should have to choose between essential medications and basic needs. SECTION 2. Medicare Negotiation. HHS shall expand the number of drugs subject to Medicare price negotiation to 50 by 2027 and 100 by 2029. SECTION 3. Transparency. Pharmaceutical manufacturers shall report production costs and pricing rationale for drugs exceeding $1,000 per course. SECTION 4. Biosimilars. FDA shall accelerate biosimilar approvals and HHS shall promote biosimilar adoption in federal programs. SECTION 5. Importation. HHS shall finalize rules permitting state importation of prescription drugs from Canada.",
        tags=["healthcare", "prescription drugs", "Medicare", "pharmaceutical", "costs"],
        related_docs=["BUD-003"],
    ))

    # --- BUDGETS (6) ---
    docs.append(GovernmentDocument(
        doc_id="BUD-001", title="Federal Highway Administration FY2025 Budget Request",
        doc_type=DocumentType.BUDGET, agency="Federal Highway Administration",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.PROPOSED,
        date_published=date(2024, 3, 11),
        summary="$62 billion budget request for federal highway programs including bridge repair and EV charging infrastructure.",
        full_text="FEDERAL HIGHWAY ADMINISTRATION. FISCAL YEAR 2025 BUDGET REQUEST. Total Request: $62.1 billion. SECTION 1. Highway Programs. National Highway Performance Program: $29.4B. Surface Transportation Block Grant: $14.8B. Bridge Formula Program: $5.5B. SECTION 2. Safety. Highway Safety Improvement Program: $3.2B. Target: 20% reduction in fatalities by 2030. SECTION 3. Climate. Carbon Reduction Program: $1.5B. National Electric Vehicle Infrastructure: $1.0B. SECTION 4. Research. Highway Research and Development: $450M. Intelligent Transportation Systems: $100M. Reference: Infrastructure Investment and Modernization Act (LEG-003).",
        tags=["transportation", "highways", "bridges", "EV", "budget"],
        related_docs=["LEG-003"],
    ))

    docs.append(GovernmentDocument(
        doc_id="BUD-002", title="Department of Energy FY2025 Budget Request",
        doc_type=DocumentType.BUDGET, agency="Department of Energy",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.PROPOSED,
        date_published=date(2024, 3, 11),
        summary="$52 billion DOE budget emphasizing clean energy RD&D, grid modernization, and nuclear security.",
        full_text="DEPARTMENT OF ENERGY. FISCAL YEAR 2025 BUDGET IN BRIEF. Total Request: $52.0 billion. SECTION 1. Clean Energy. Office of Energy Efficiency and Renewable Energy: $4.2B. Advanced Research Projects Agency-Energy: $800M. Loan Programs Office: $4.0B in new loan authority. SECTION 2. Grid. Grid Deployment Office: $2.1B for transmission and distribution modernization. SECTION 3. Nuclear Security. National Nuclear Security Administration: $23.0B. Stockpile maintenance: $17.8B. SECTION 4. Science. Office of Science: $8.8B. Fusion energy research: $1.0B. National laboratories operations: $5.4B.",
        tags=["energy", "DOE", "clean energy", "nuclear", "grid", "budget"],
        related_docs=["LEG-004"],
    ))

    docs.append(GovernmentDocument(
        doc_id="BUD-003", title="Department of Veterans Affairs FY2025 Budget Request",
        doc_type=DocumentType.BUDGET, agency="Department of Veterans Affairs",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.PROPOSED,
        date_published=date(2024, 3, 11),
        summary="$369 billion VA budget request for healthcare, benefits, and cemetery administration.",
        full_text="DEPARTMENT OF VETERANS AFFAIRS. FISCAL YEAR 2025 BUDGET SUBMISSION. Total Request: $369.3 billion ($135.5B discretionary, $233.8B mandatory). SECTION 1. Medical Care. Veterans Health Administration: $121.4B. Mental health services: $14.8B. Suicide prevention: $627M. SECTION 2. Benefits. Veterans Benefits Administration: $218.5B. Disability compensation: $153B. Education (GI Bill): $14.2B. SECTION 3. IT Modernization. Electronic Health Record: $2.6B. Cybersecurity: $520M. SECTION 4. Infrastructure. Major/minor construction: $3.4B. 15 new community-based outpatient clinics.",
        tags=["veterans", "VA", "healthcare", "benefits", "budget"],
        related_docs=["LEG-009", "EO-006"],
    ))

    docs.append(GovernmentDocument(
        doc_id="BUD-004", title="Small Business Administration FY2025 Budget Request",
        doc_type=DocumentType.BUDGET, agency="Small Business Administration",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.PROPOSED,
        date_published=date(2024, 3, 11),
        summary="$1.2 billion SBA budget for small business lending, contracting, and disaster assistance programs.",
        full_text="SMALL BUSINESS ADMINISTRATION. FISCAL YEAR 2025 BUDGET JUSTIFICATION. Total Request: $1.2 billion. SECTION 1. Entrepreneurial Development. Small Business Development Centers: $175M. SCORE: $14M. Women's Business Centers: $40M. SECTION 2. Capital Access. 7(a) Loan Program: $32B authorization. 504 Loan Program: $7.5B authorization. SBIC: $4B in leverage. SECTION 3. Government Contracting. Small business goal: 23% of federal procurement. HUBZone: $2.5B target. SECTION 4. Disaster Assistance. Disaster loan program: $3.7B estimated demand.",
        tags=["small business", "SBA", "loans", "contracting", "budget"],
        related_docs=["LEG-010"],
    ))

    docs.append(GovernmentDocument(
        doc_id="BUD-005", title="Federal Emergency Management Agency FY2025 Budget",
        doc_type=DocumentType.BUDGET, agency="Federal Emergency Management Agency",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.PROPOSED,
        date_published=date(2024, 3, 11),
        summary="$33 billion FEMA budget for disaster relief, preparedness grants, and flood insurance modernization.",
        full_text="FEDERAL EMERGENCY MANAGEMENT AGENCY. FY2025 BUDGET OVERVIEW. Total Request: $33.1 billion. SECTION 1. Disaster Relief Fund. $22.3B for response and recovery operations. SECTION 2. Preparedness Grants. State Homeland Security Grant Program: $610M. Urban Areas Security Initiative: $615M. SECTION 3. Flood Insurance. National Flood Insurance Program reform: Risk Rating 2.0 implementation. $500M for flood mapping modernization. SECTION 4. Climate Adaptation. Building Resilient Infrastructure and Communities: $1.0B. Hazard Mitigation Grant Program: $800M. SECTION 5. Workforce. 1,200 additional reservists for surge capacity.",
        tags=["FEMA", "disaster relief", "flood insurance", "preparedness", "budget"],
        related_docs=["EO-004"],
    ))

    docs.append(GovernmentDocument(
        doc_id="BUD-006", title="City of Portland FY2025 General Fund Budget",
        doc_type=DocumentType.BUDGET, agency="City of Portland",
        jurisdiction=Jurisdiction.LOCAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 6, 30),
        summary="$815 million city general fund budget prioritizing public safety, housing, and transportation.",
        full_text="CITY OF PORTLAND, OREGON. ADOPTED BUDGET FISCAL YEAR 2024-2025. General Fund: $815.2 million. SECTION 1. Public Safety. Police Bureau: $262M. Fire & Rescue: $165M. Emergency Communications: $24M. SECTION 2. Housing. Portland Housing Bureau: $82M. Homeless services: $45M. Affordable housing development: $37M. SECTION 3. Transportation. Portland Bureau of Transportation: $98M. Road maintenance: $42M. Transit improvements: $28M. SECTION 4. Parks. Parks & Recreation: $68M. SECTION 5. Community Development. Planning & Sustainability: $32M. Economic development: $18M.",
        tags=["Portland", "municipal budget", "public safety", "housing", "local government"],
    ))

    # --- REPORTS (10) ---
    docs.append(GovernmentDocument(
        doc_id="RPT-001", title="Congressional Budget Office: Federal Deficit Projections 2025-2034",
        doc_type=DocumentType.REPORT, agency="Congressional Budget Office",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 2, 7),
        summary="CBO projects federal deficits totaling $20 trillion over the next decade with debt reaching 116% of GDP by 2034.",
        full_text="CONGRESSIONAL BUDGET OFFICE. THE BUDGET AND ECONOMIC OUTLOOK: 2025 TO 2034. SECTION 1. Summary. Federal budget deficits are projected to total $20.0 trillion over 2025-2034. Debt held by the public rises from 99% of GDP in 2024 to 116% by 2034. SECTION 2. Revenue. Revenue averages 17.8% of GDP. Individual income taxes: $31.4T cumulative. Corporate income taxes: $5.1T. SECTION 3. Spending. Outlays average 24.1% of GDP. Social Security: $18.2T. Medicare: $12.4T. Medicaid: $7.1T. Net interest: $12.4T. Defense: $9.8T. SECTION 4. Economic Assumptions. Real GDP growth averages 1.8%. Unemployment: 4.3% average. Inflation (CPI): 2.3% by 2026.",
        tags=["deficit", "CBO", "debt", "fiscal", "economic outlook"],
    ))

    docs.append(GovernmentDocument(
        doc_id="RPT-002", title="GAO Report: Federal IT Modernization Challenges",
        doc_type=DocumentType.REPORT, agency="Government Accountability Office",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 4, 18),
        summary="GAO identifies $100 billion in legacy IT spending and recommends accelerated modernization of critical federal systems.",
        full_text="GOVERNMENT ACCOUNTABILITY OFFICE. GAO-24-106359. INFORMATION TECHNOLOGY: Agencies Need to Address Ongoing Modernization Challenges. SECTION 1. Findings. Federal agencies spend $100B+ annually on IT, with 80% on operations and maintenance of legacy systems. 12 of 24 CFO Act agencies have critical systems running on unsupported platforms. SECTION 2. Risks. Legacy systems create cybersecurity vulnerabilities, interoperability failures, and increased maintenance costs. SECTION 3. Recommendations. (1) OMB should require agency-level IT modernization roadmaps. (2) Agencies should adopt cloud-first strategies per OMB M-24-08. (3) CIO authority should be strengthened per FITARA scorecard metrics. (4) Technology Modernization Fund should be replenished to $1B annually.",
        tags=["IT modernization", "GAO", "legacy systems", "cybersecurity", "federal technology"],
        related_docs=["EO-003"],
    ))

    docs.append(GovernmentDocument(
        doc_id="RPT-003", title="EPA Integrated Science Assessment: Particulate Matter",
        doc_type=DocumentType.REPORT, agency="Environmental Protection Agency",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 1, 10),
        summary="Comprehensive scientific review finding causal relationship between PM2.5 exposure and cardiovascular mortality at current standard levels.",
        full_text="ENVIRONMENTAL PROTECTION AGENCY. EPA/600/R-24/001. INTEGRATED SCIENCE ASSESSMENT FOR PARTICULATE MATTER. SECTION 1. Executive Summary. This ISA reviews over 4,000 epidemiological, toxicological, and clinical studies. SECTION 2. Health Effects. Causal relationship between short-term PM2.5 exposure and cardiovascular effects. Causal relationship between long-term PM2.5 and total mortality. Evidence strengthened since 2019 ISA at concentrations below current 12 ug/m3 standard. SECTION 3. Susceptible Populations. Children, elderly, and communities with pre-existing conditions face elevated risk. Environmental justice communities disproportionately exposed. SECTION 4. Ecological Effects. PM deposition causes acidification and nutrient loading in sensitive ecosystems.",
        tags=["PM2.5", "air quality", "health effects", "EPA", "scientific assessment"],
        related_docs=["LEG-001", "REG-001"],
    ))

    docs.append(GovernmentDocument(
        doc_id="RPT-004", title="Census Bureau: American Community Survey 2023 Summary",
        doc_type=DocumentType.REPORT, agency="U.S. Census Bureau",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 9, 12),
        summary="Annual demographic, economic, and housing statistics for the United States population.",
        full_text="U.S. CENSUS BUREAU. AMERICAN COMMUNITY SURVEY: 2023 1-YEAR ESTIMATES. SECTION 1. Demographics. U.S. population: 336.0 million. Median age: 38.9 years. Foreign-born: 14.3%. SECTION 2. Economics. Median household income: $78,538. Poverty rate: 11.1%. Unemployment: 3.6%. SECTION 3. Education. Bachelor's degree or higher: 34.2%. High school graduate or higher: 89.1%. SECTION 4. Housing. Homeownership rate: 65.2%. Median home value: $340,600. Median gross rent: $1,378. Housing cost-burdened renters: 49.7%. SECTION 5. Health Insurance. Uninsured rate: 7.9%. Employer-sponsored coverage: 54.3%.",
        tags=["census", "demographics", "economic data", "housing", "statistics"],
    ))

    docs.append(GovernmentDocument(
        doc_id="RPT-005", title="DOT National Bridge Inspection Report 2024",
        doc_type=DocumentType.REPORT, agency="Department of Transportation",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 7, 25),
        summary="Annual assessment finding 42,000 structurally deficient bridges requiring $125 billion in repair investment.",
        full_text="DEPARTMENT OF TRANSPORTATION. FEDERAL HIGHWAY ADMINISTRATION. NATIONAL BRIDGE INVENTORY: 2024 ANNUAL REPORT. SECTION 1. Inventory Summary. Total bridges: 621,000. Structurally deficient: 42,000 (6.8%). Functionally obsolete: 73,000 (11.8%). SECTION 2. Condition Trends. Deficient bridges decreased by 4,200 since 2020. Average bridge age: 44 years. 14,000 bridges over 80 years old. SECTION 3. Investment Needs. Estimated repair backlog: $125 billion. Annual funding gap: $8.3 billion above current investment levels. Bridge Formula Program (LEG-003) providing $5.5B/year. SECTION 4. Safety. Zero bridge failures resulting in fatalities in 2023. 234 bridges on weight restriction due to deterioration.",
        tags=["bridges", "infrastructure", "safety", "DOT", "transportation"],
        related_docs=["LEG-003", "BUD-001"],
    ))

    docs.append(GovernmentDocument(
        doc_id="RPT-006", title="USGS National Water Quality Assessment: PFAS Occurrence",
        doc_type=DocumentType.REPORT, agency="U.S. Geological Survey",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 5, 15),
        summary="First nationwide assessment finding PFAS in 45% of tap water samples with highest concentrations near industrial sites.",
        full_text="U.S. GEOLOGICAL SURVEY. SCIENTIFIC INVESTIGATIONS REPORT 2024-5041. PFAS IN THE NATION'S TAP WATER. SECTION 1. Study Design. 716 tap water samples from 269 public and private supply systems across 50 states. SECTION 2. Results. PFAS detected in 45% of samples. Most common: PFBS (34%), PFHxS (21%), PFOA (18%), PFOS (15%). Concentrations highest within 5 miles of known contamination sources. Urban systems: 54% detection. Rural private wells: 21% detection. SECTION 3. Health Context. 73 samples (10%) exceeded proposed EPA MCLs for PFOA or PFOS. SECTION 4. Recommendations. Expanded monitoring for private wells. Treatment technology assessment for small systems.",
        tags=["PFAS", "water quality", "USGS", "drinking water", "contamination"],
        related_docs=["REG-004", "LEG-008"],
    ))

    docs.append(GovernmentDocument(
        doc_id="RPT-007", title="VA Inspector General: Mental Health Service Wait Times",
        doc_type=DocumentType.REPORT, agency="VA Office of Inspector General",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 8, 8),
        summary="OIG audit finding 35% of veterans waited over 30 days for initial mental health appointments at surveyed facilities.",
        full_text="VA OFFICE OF INSPECTOR GENERAL. REPORT NO. 24-01234-156. AUDIT OF MENTAL HEALTH SERVICE ACCESS AT VA MEDICAL CENTERS. SECTION 1. Objective. Evaluate wait times for mental health services at 30 VA medical centers. SECTION 2. Findings. 35% of new patients waited >30 days for initial appointment. Average wait: 28 days (target: 20 days). 5 facilities exceeded 45-day average. SECTION 3. Contributing Factors. 22% vacancy rate for psychologists. 18% vacancy rate for psychiatrists. Rural facilities disproportionately affected. SECTION 4. Recommendations. (1) Implement crisis staffing plans at underperforming facilities. (2) Expand telemental health to reduce geographic barriers. (3) Increase recruitment incentives. VA management concurred with all recommendations.",
        tags=["veterans", "mental health", "wait times", "VA", "inspector general"],
        related_docs=["LEG-009", "BUD-003"],
    ))

    docs.append(GovernmentDocument(
        doc_id="RPT-008", title="NIST AI Risk Management Framework: Implementation Guide",
        doc_type=DocumentType.REPORT, agency="National Institute of Standards and Technology",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 4, 29),
        summary="Practical guidance for organizations implementing the NIST AI RMF including risk assessment methodologies and governance structures.",
        full_text="NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. NIST AI 600-1. AI RISK MANAGEMENT FRAMEWORK: IMPLEMENTATION GUIDE. SECTION 1. Overview. This guide supports implementation of the AI RMF 1.0 (NIST AI 100-1) across diverse organizations. SECTION 2. Govern Function. Establish AI governance structure. Define risk tolerance. Assign accountability. Develop AI policies aligned with organizational values. SECTION 3. Map Function. Contextualize AI risks. Identify stakeholders. Assess intended and unintended impacts. Document data provenance and model limitations. SECTION 4. Measure Function. Quantify AI risks using standardized metrics. Test for bias, robustness, and reliability. Third-party evaluations for high-risk applications. SECTION 5. Manage Function. Prioritize and treat identified risks. Monitor deployed AI systems. Incident response procedures for AI failures.",
        tags=["AI", "risk management", "NIST", "governance", "framework"],
        related_docs=["LEG-007", "EO-005"],
    ))

    docs.append(GovernmentDocument(
        doc_id="RPT-009", title="Federal Reserve Financial Stability Report: November 2024",
        doc_type=DocumentType.REPORT, agency="Board of Governors of the Federal Reserve System",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 11, 15),
        summary="Semi-annual assessment identifying commercial real estate, cyber threats, and geopolitical risks as primary financial stability concerns.",
        full_text="BOARD OF GOVERNORS OF THE FEDERAL RESERVE SYSTEM. FINANCIAL STABILITY REPORT. NOVEMBER 2024. SECTION 1. Asset Valuations. Equity valuations elevated relative to historical norms. Treasury term premiums rising. SECTION 2. Borrowing. Household debt-to-income stable at 9.8%. Corporate leverage declining modestly. Commercial real estate delinquencies rising in office sector to 8.1%. SECTION 3. Financial Leverage. Banking system well-capitalized. CET1 ratio: 12.7% aggregate. Nonbank financial intermediation continues to grow. SECTION 4. Funding Risks. Money market fund assets: $6.4T. Stablecoin market: $180B. SECTION 5. Near-Term Risks. Survey of market contacts identifies: CRE deterioration, cyber attacks, geopolitical escalation, and persistent inflation as top concerns.",
        tags=["financial stability", "Federal Reserve", "banking", "CRE", "systemic risk"],
    ))

    docs.append(GovernmentDocument(
        doc_id="RPT-010", title="Department of Education: State of Higher Education 2024",
        doc_type=DocumentType.REPORT, agency="Department of Education",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 10, 1),
        summary="Comprehensive report on enrollment trends, student debt, completion rates, and workforce outcomes in U.S. higher education.",
        full_text="U.S. DEPARTMENT OF EDUCATION. THE STATE OF HIGHER EDUCATION: 2024 ANNUAL REPORT. SECTION 1. Enrollment. Total postsecondary enrollment: 19.4 million. Decline of 1.2M since 2019. Community college enrollment stabilizing. Online enrollment: 40% of students take at least one online course. SECTION 2. Student Debt. Outstanding federal student loan debt: $1.6 trillion. Average debt at graduation: $32,800. Income-driven repayment enrollment: 9.8 million borrowers. SECTION 3. Completion. 6-year bachelor's completion rate: 64%. Associate degree 3-year rate: 33%. Completion gaps persist by race and income. SECTION 4. Workforce Outcomes. Median earnings 5 years post-graduation: $46,900. STEM graduates: $68,200. Education: $38,100.",
        tags=["higher education", "student debt", "enrollment", "workforce", "completion rates"],
    ))

    # --- Additional docs to reach 50+ ---
    docs.append(GovernmentDocument(
        doc_id="REG-009", title="FCC Broadband Labeling Requirements",
        doc_type=DocumentType.REGULATION, agency="Federal Communications Commission",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 4, 10),
        summary="Requires ISPs to display standardized broadband nutrition labels showing speed, price, and data cap information.",
        full_text="FEDERAL COMMUNICATIONS COMMISSION. 47 CFR Part 8. Broadband Consumer Labels. SECTION 1. Requirements. All ISPs must display consumer-friendly labels at point of sale. SECTION 2. Label Contents. Typical download/upload speeds, latency, monthly price including all fees, data caps, network management practices. SECTION 3. Format. Standardized format modeled on FDA nutrition labels. Available in English and Spanish. SECTION 4. Enforcement. Violations subject to forfeiture penalties under 47 U.S.C. 503(b).",
        tags=["broadband", "FCC", "consumer protection", "internet", "transparency"],
        related_docs=["LEG-003"],
    ))

    docs.append(GovernmentDocument(
        doc_id="REG-010", title="OSHA Heat Injury and Illness Prevention Standard",
        doc_type=DocumentType.REGULATION, agency="Occupational Safety and Health Administration",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.PROPOSED,
        date_published=date(2024, 7, 2),
        summary="Proposed first-ever federal standard for heat exposure in outdoor and indoor workplaces.",
        full_text="DEPARTMENT OF LABOR. 29 CFR Part 1910, 1926. Heat Injury and Illness Prevention in Outdoor and Indoor Work Settings. SECTION 1. Scope. Applies to all outdoor work and indoor work where heat index exceeds 80F. SECTION 2. Initial Heat Trigger. At 80F heat index: drinking water, shade access, acclimatization plans for new workers. SECTION 3. High Heat Trigger. At 90F heat index: mandatory 15-minute rest breaks per hour, buddy system, emergency response procedures. SECTION 4. Employer Obligations. Written heat illness prevention plan. Worker training. Monitoring for heat illness symptoms.",
        tags=["heat safety", "OSHA", "workplace safety", "worker protection", "climate"],
    ))

    docs.append(GovernmentDocument(
        doc_id="EO-007", title="Executive Order on Federal Workforce Modernization",
        doc_type=DocumentType.EXECUTIVE_ORDER, agency="Executive Office of the President",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 8, 12),
        summary="Reforms federal hiring processes and establishes skills-based assessment to replace degree requirements.",
        full_text="EXECUTIVE ORDER 14165. Modernizing the Federal Workforce. SECTION 1. Policy. Federal employment should be accessible based on skills and competencies. SECTION 2. Skills-Based Hiring. OPM shall revise qualification standards to emphasize skills assessments over degree requirements within 180 days. SECTION 3. Hiring Speed. Target: 80-day average time-to-hire. USA Staffing platform improvements. SECTION 4. Technology Talent. Digital Corps expansion to 1,000 positions. SECTION 5. Telework. Agencies shall maintain flexible work arrangements where mission-compatible.",
        tags=["federal workforce", "hiring", "OPM", "skills-based", "telework"],
    ))

    docs.append(GovernmentDocument(
        doc_id="CR-007", title="State of New York v. Social Media Platform - Child Safety",
        doc_type=DocumentType.COURT_RULING, agency="New York State Supreme Court",
        jurisdiction=Jurisdiction.STATE, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 9, 20),
        summary="Upheld New York child online safety law requiring age verification and default privacy settings for minors.",
        full_text="NEW YORK STATE SUPREME COURT. INDEX NO. 451234/2024. State of New York v. Social Media Platform Inc. DECISION AND ORDER. I. BACKGROUND. New York enacted the Child Online Safety Act requiring platforms to verify age and apply restrictive default settings for users under 18. Platform challenges on First Amendment grounds. II. ANALYSIS. Age verification requirement survives intermediate scrutiny. State's interest in protecting minors is substantial. Regulation is narrowly tailored - applies only to accounts of identified minors. III. HOLDING. Motion to dismiss DENIED. Preliminary injunction against enforcement DENIED. Law may be enforced pending trial.",
        tags=["child safety", "social media", "First Amendment", "privacy", "minors"],
    ))

    docs.append(GovernmentDocument(
        doc_id="RPT-011", title="Inspector General Report: Medicare Fraud Prevention Results FY2024",
        doc_type=DocumentType.REPORT, agency="HHS Office of Inspector General",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 12, 1),
        summary="OIG reports $4.7 billion in expected recoveries from healthcare fraud enforcement actions in FY2024.",
        full_text="HHS OFFICE OF INSPECTOR GENERAL. SEMIANNUAL REPORT TO CONGRESS. FY2024 RESULTS. SECTION 1. Overview. OIG investigations yielded $4.7B in expected recoveries. 672 criminal actions and 834 civil actions. SECTION 2. Key Cases. Opioid diversion network: $1.2B. Telemedicine fraud: $800M. DME scheme: $450M. SECTION 3. Data Analytics. AI-enhanced claims analysis identified $2.1B in suspicious billing patterns. Predictive models reduced improper payments by 12%. SECTION 4. Recommendations. 289 new recommendations to CMS. 82% acceptance rate. Estimated savings from implemented recommendations: $6.2B over 5 years.",
        tags=["Medicare", "fraud", "OIG", "healthcare", "enforcement"],
    ))

    docs.append(GovernmentDocument(
        doc_id="LEG-011", title="Disaster Resilience and Recovery Act",
        doc_type=DocumentType.LEGISLATION, agency="U.S. Congress",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 9, 30),
        summary="Reforms federal disaster assistance programs and establishes pre-disaster mitigation funding.",
        full_text="SECTION 1. Short Title. Disaster Resilience and Recovery Act. SECTION 2. Pre-Disaster Mitigation. $5B annually for FEMA Building Resilient Infrastructure and Communities program. SECTION 3. Community Disaster Loans. Authorization increased to $10M per community. Repayment period extended to 10 years. SECTION 4. Individual Assistance. Maximum FEMA individual assistance grant increased to $50,000. SECTION 5. Climate Adaptation. Federal facilities in flood zones must meet updated flood elevation standards. Reference: Stafford Act, 42 U.S.C. 5121.",
        tags=["disaster", "FEMA", "resilience", "mitigation", "recovery"],
        related_docs=["BUD-005"],
    ))

    docs.append(GovernmentDocument(
        doc_id="CR-008", title="Environmental Defense Fund v. Army Corps of Engineers",
        doc_type=DocumentType.COURT_RULING, agency="U.S. District Court, D. Montana",
        jurisdiction=Jurisdiction.FEDERAL, status=DocumentStatus.ACTIVE,
        date_published=date(2024, 7, 8),
        summary="Enjoined issuance of Nationwide Permit 12 for oil pipeline crossings pending supplemental environmental review.",
        full_text="UNITED STATES DISTRICT COURT, DISTRICT OF MONTANA. Case No. 4:23-cv-00123. Environmental Defense Fund v. U.S. Army Corps of Engineers. ORDER GRANTING PRELIMINARY INJUNCTION. I. BACKGROUND. Challenge to reissuance of NWP 12 authorizing water body crossings for oil and gas pipelines without individual permits. II. NEPA ANALYSIS. Corps failed to prepare supplemental EIS despite significant new information on climate impacts and pipeline spill frequency. III. ESA ANALYSIS. Programmatic biological opinion inadequate for individual species impacts. IV. ORDER. NWP 12 for oil and gas pipelines ENJOINED pending supplemental NEPA review. Existing authorized crossings not affected.",
        tags=["environment", "NEPA", "pipelines", "Army Corps", "injunction"],
    ))

    return docs
