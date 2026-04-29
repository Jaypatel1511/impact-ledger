# impact-ledger 📊

**Open source impact investment portfolio tracker for CDFIs, private debt, and community development finance.**

Track loans, NMTC deals, grants, and equity investments alongside social impact metrics —
jobs created, affordable units financed, borrower demographics, and geographic reach.
Generate standardized CDFI Fund-style reports in Python.

---

## Why impact-ledger?

Impact funds tracking private debt, community facilities, and social impact metrics
currently have two options: custom Excel spreadsheets or $50k+/year proprietary CRM software.
impact-ledger is the open source alternative — standardized, auditable, and free.

---

## Installation

    pip install impact-ledger

---

## Quickstart

    from impactledger import loan, nmtc, grant, add_impact, Portfolio
    from impactledger import cdfi_fund_report, sector_impact_report

    # Create a portfolio
    p = Portfolio(name="CDFI Impact Fund I", vintage_year=2022)

    # Add a loan with impact metrics
    inv = loan(
        name="Southside Health Center",
        amount=2_000_000,
        interest_rate=0.045,
        date_closed="2023-01-15",
        maturity_date="2033-01-15",
        state="IL",
        borrower_name="Southside Health Inc",
        borrower_type="nonprofit",
        sector="healthcare",
        is_low_income_area=True,
        is_minority_borrower=True,
    )
    add_impact(inv, jobs_created=25, jobs_retained=40, patients_served=5000)
    p.add(inv)

    # Add an NMTC deal
    deal = nmtc(
        name="Detroit Manufacturing NMTC",
        amount=8_000_000,
        date_closed="2022-06-01",
        maturity_date="2029-06-01",
        state="MI",
        borrower_name="Detroit Advanced Mfg Co",
        sector="small_business",
        is_low_income_area=True,
    )
    add_impact(deal, jobs_created=45, jobs_retained=60)
    p.add(deal)

    # Portfolio summary
    p.summary()

    # Generate reports
    cdfi_fund_report(p)
    sector_impact_report(p)

    # Export to DataFrame
    df = p.to_dataframe()

---

## Investment Types Supported

- loan          - Private debt / direct lending
- equity        - Equity investment
- grant         - Grant or forgivable loan
- nmtc          - New Markets Tax Credit investment
- guarantee     - Loan guarantee
- bond          - Bond or debenture

---

## Impact Metrics Tracked

- Jobs created and retained
- Affordable housing units financed
- Community square footage
- Businesses supported
- Patients served
- Students served
- Borrower demographics (minority, women, low-income)
- Geographic reach (state, census tract, rural/urban)

---

## Reports

- cdfi_fund_report()      - CDFI Fund Annual Certification Report format
- sector_impact_report()  - Impact breakdown by sector
- watchlist_report()      - Impaired and watch-list investments

---

## Running Tests

    PYTHONPATH=. pytest tests/ -v

27 tests across all modules.

---

## Who This Is For

- CDFI loan officers tracking portfolio performance and impact
- Impact fund managers reporting to LPs and board
- Researchers studying community development finance outcomes
- Anyone replacing a bespoke Excel impact tracker with Python

---

## License

MIT 2026 Jaypatel1511
