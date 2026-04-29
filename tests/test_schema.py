import pytest
from impactledger.data.schema import Investment, ImpactMetrics


def test_investment_created(sample_loan):
    assert sample_loan.name == "Southside Health Center"
    assert sample_loan.amount == 2_000_000
    assert sample_loan.investment_type == "loan"


def test_invalid_type_raises():
    with pytest.raises(ValueError, match="investment_type"):
        Investment(
            id="TEST01",
            name="Bad",
            investment_type="invalid",
            sector="healthcare",
            amount=1_000_000,
            date_closed="2023-01-01",
            maturity_date="2033-01-01",
            interest_rate=0.05,
            state="IL",
            borrower_name="Test",
            borrower_type="nonprofit",
        )


def test_invalid_sector_raises():
    with pytest.raises(ValueError, match="sector"):
        Investment(
            id="TEST01",
            name="Bad",
            investment_type="loan",
            sector="invalid_sector",
            amount=1_000_000,
            date_closed="2023-01-01",
            maturity_date="2033-01-01",
            interest_rate=0.05,
            state="IL",
            borrower_name="Test",
            borrower_type="nonprofit",
        )


def test_negative_amount_raises():
    with pytest.raises(ValueError, match="amount must be positive"):
        Investment(
            id="TEST01",
            name="Bad",
            investment_type="loan",
            sector="healthcare",
            amount=-1_000_000,
            date_closed="2023-01-01",
            maturity_date="2033-01-01",
            interest_rate=0.05,
            state="IL",
            borrower_name="Test",
            borrower_type="nonprofit",
        )


def test_impact_metrics(sample_loan):
    assert sample_loan.impact.jobs_created == 25
    assert sample_loan.impact.jobs_retained == 40
    assert sample_loan.impact.total_jobs == 65


def test_annual_income(sample_loan):
    expected = 2_000_000 * 0.045
    assert sample_loan.annual_income == pytest.approx(expected)


def test_amount_mm(sample_loan):
    assert sample_loan.amount_mm == pytest.approx(2.0)
