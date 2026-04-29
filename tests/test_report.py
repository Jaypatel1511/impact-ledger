import pytest
import pandas as pd
from impactledger.models.report import (
    cdfi_fund_report, sector_impact_report, watchlist_report
)


def test_cdfi_fund_report(sample_portfolio):
    df = cdfi_fund_report(sample_portfolio)
    assert isinstance(df, pd.DataFrame)
    assert "Metric" in df.columns
    assert "Value" in df.columns


def test_sector_impact_report(sample_portfolio):
    df = sector_impact_report(sample_portfolio)
    assert isinstance(df, pd.DataFrame)


def test_watchlist_empty(sample_portfolio):
    df = watchlist_report(sample_portfolio)
    assert isinstance(df, pd.DataFrame)


def test_watchlist_with_impaired(sample_portfolio, sample_loan):
    sample_loan.status = "watch"
    df = watchlist_report(sample_portfolio)
    assert len(df) >= 1
