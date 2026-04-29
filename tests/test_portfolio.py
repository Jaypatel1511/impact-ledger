import pytest
import pandas as pd
from impactledger import Portfolio


def test_portfolio_count(sample_portfolio):
    assert sample_portfolio.count() == 3


def test_total_committed(sample_portfolio):
    assert sample_portfolio.total_committed == pytest.approx(10_500_000)


def test_add_duplicate_raises(sample_portfolio, sample_loan):
    with pytest.raises(ValueError, match="already exists"):
        sample_portfolio.add(sample_loan)


def test_filter_state(sample_portfolio):
    il = sample_portfolio.filter_state("IL")
    assert len(il) == 1
    assert il[0].state == "IL"


def test_filter_type(sample_portfolio):
    loans = sample_portfolio.filter_type("loan")
    assert len(loans) == 1


def test_filter_sector(sample_portfolio):
    health = sample_portfolio.filter_sector("healthcare")
    assert len(health) == 1


def test_weighted_avg_rate(sample_portfolio):
    assert 0 < sample_portfolio.weighted_avg_rate < 0.10


def test_total_jobs(sample_portfolio):
    assert sample_portfolio.total_jobs_created == 70
    assert sample_portfolio.total_jobs_retained == 100


def test_affordable_units(sample_portfolio):
    assert sample_portfolio.total_affordable_units == 0


def test_pct_low_income_area(sample_portfolio):
    assert sample_portfolio.pct_low_income_area == pytest.approx(1.0)


def test_pct_minority_borrower(sample_portfolio):
    assert sample_portfolio.pct_minority_borrower == pytest.approx(2/3, rel=1e-3)


def test_to_dataframe(sample_portfolio):
    df = sample_portfolio.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3


def test_sector_breakdown(sample_portfolio):
    df = sample_portfolio.sector_breakdown()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3


def test_state_breakdown(sample_portfolio):
    df = sample_portfolio.state_breakdown()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3


def test_summary_runs(sample_portfolio):
    sample_portfolio.summary()


def test_remove(sample_portfolio, sample_loan):
    sample_portfolio.remove(sample_loan.id)
    assert sample_portfolio.count() == 2
