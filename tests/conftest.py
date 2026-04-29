import pytest
from impactledger import loan, nmtc, grant, add_impact, Portfolio


@pytest.fixture
def sample_loan():
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
    return add_impact(inv, jobs_created=25, jobs_retained=40,
                      patients_served=5000)


@pytest.fixture
def sample_nmtc():
    inv = nmtc(
        name="Detroit Manufacturing NMTC",
        amount=8_000_000,
        date_closed="2022-06-01",
        maturity_date="2029-06-01",
        state="MI",
        borrower_name="Detroit Advanced Mfg Co",
        sector="small_business",
        is_low_income_area=True,
    )
    return add_impact(inv, jobs_created=45, jobs_retained=60)


@pytest.fixture
def sample_grant():
    return grant(
        name="Atlanta Housing Grant",
        amount=500_000,
        date_closed="2023-03-01",
        state="GA",
        borrower_name="Atlanta Housing Corp",
        sector="affordable_housing",
        is_low_income_area=True,
        is_minority_borrower=True,
        is_women_borrower=True,
    )


@pytest.fixture
def sample_portfolio(sample_loan, sample_nmtc, sample_grant):
    p = Portfolio(name="CDFI Impact Fund I", vintage_year=2022)
    p.add(sample_loan)
    p.add(sample_nmtc)
    p.add(sample_grant)
    return p
