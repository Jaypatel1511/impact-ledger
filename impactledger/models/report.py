"""
Standardized impact report generator.
Produces CDFI Fund, GIIRS, and custom report formats.
"""
import pandas as pd
from impactledger.models.portfolio import Portfolio


def cdfi_fund_report(portfolio: Portfolio) -> pd.DataFrame:
    """
    Generate a CDFI Fund-style impact report.
    Matches the format used in CDFI Fund Annual Certification Reports.
    """
    df = portfolio.to_dataframe()

    report = {
        "Total Financing ($MM)":        round(portfolio.total_committed / 1e6, 2),
        "Number of Transactions":       portfolio.count(),
        "Avg Transaction Size ($)":     round(portfolio.total_committed / max(portfolio.count(), 1)),
        "% in Low-Income Areas":        f"{portfolio.pct_low_income_area*100:.1f}%",
        "% Minority Borrowers":         f"{portfolio.pct_minority_borrower*100:.1f}%",
        "% Women Borrowers":            f"{portfolio.pct_women_borrower*100:.1f}%",
        "Jobs Created":                 portfolio.total_jobs_created,
        "Jobs Retained":                portfolio.total_jobs_retained,
        "Affordable Units Financed":    portfolio.total_affordable_units,
        "Community Sq Ft":              round(portfolio.total_sq_ft),
        "States Served":                len(set(i.state for i in portfolio._investments)),
        "Weighted Avg Interest Rate":   f"{portfolio.weighted_avg_rate*100:.2f}%",
    }

    result = pd.DataFrame(
        list(report.items()), columns=["Metric", "Value"]
    )

    print(f"\nCDFI Fund Impact Report — {portfolio.name}")
    print("=" * 50)
    print(result.to_string(index=False))
    print()

    return result


def sector_impact_report(portfolio: Portfolio) -> pd.DataFrame:
    """
    Generate a sector-level impact breakdown.
    """
    df = portfolio.to_dataframe()

    impact_cols = ["jobs_created", "jobs_retained", "affordable_units",
                   "sq_ft", "patients", "students", "businesses"]
    available = [c for c in impact_cols if c in df.columns]

    agg_dict = {"amount": ["count", "sum"]}
    for col in available:
        agg_dict[col] = "sum"

    result = df.groupby("sector").agg(agg_dict).reset_index()
    result.columns = ["_".join(c).strip("_") for c in result.columns]
    result = result.sort_values("amount_sum", ascending=False)

    print(f"\nSector Impact Report — {portfolio.name}")
    print("=" * 60)
    print(result.to_string(index=False))
    print()

    return result


def watchlist_report(portfolio: Portfolio) -> pd.DataFrame:
    """
    Generate a watchlist of impaired investments.
    """
    impaired = portfolio.impaired_investments
    if not impaired:
        print(f"\nNo impaired investments in {portfolio.name}")
        return pd.DataFrame()

    rows = [{
        "ID": i.id,
        "Name": i.name,
        "Status": i.status,
        "Amount ($MM)": round(i.amount / 1e6, 2),
        "Outstanding ($MM)": round(i.outstanding_balance / 1e6, 2),
        "State": i.state,
        "Sector": i.sector,
    } for i in impaired]

    df = pd.DataFrame(rows)
    print(f"\nWatchlist Report — {portfolio.name}")
    print("=" * 60)
    print(df.to_string(index=False))
    print()
    return df
