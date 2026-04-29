"""
Investment model — factory functions and helpers for creating investments.
"""
from impactledger.data.schema import Investment, ImpactMetrics
import uuid


def make_id() -> str:
    """Generate a short unique investment ID."""
    return str(uuid.uuid4())[:8].upper()


def loan(
    name: str,
    amount: float,
    interest_rate: float,
    date_closed: str,
    maturity_date: str,
    state: str,
    borrower_name: str,
    borrower_type: str = "nonprofit",
    sector: str = "community_facility",
    **kwargs,
) -> Investment:
    """Convenience factory for creating a loan investment."""
    return Investment(
        id=make_id(),
        name=name,
        investment_type="loan",
        sector=sector,
        amount=amount,
        date_closed=date_closed,
        maturity_date=maturity_date,
        interest_rate=interest_rate,
        state=state,
        borrower_name=borrower_name,
        borrower_type=borrower_type,
        **kwargs,
    )


def nmtc(
    name: str,
    amount: float,
    date_closed: str,
    maturity_date: str,
    state: str,
    borrower_name: str,
    **kwargs,
) -> Investment:
    """Convenience factory for creating an NMTC investment."""
    return Investment(
        id=make_id(),
        name=name,
        investment_type="nmtc",
        sector=kwargs.pop("sector", "community_facility"),
        amount=amount,
        date_closed=date_closed,
        maturity_date=maturity_date,
        interest_rate=kwargs.pop("interest_rate", 0.01),
        state=state,
        borrower_name=borrower_name,
        borrower_type=kwargs.pop("borrower_type", "nonprofit"),
        is_low_income_area=kwargs.pop("is_low_income_area", True),
        **kwargs,
    )


def grant(
    name: str,
    amount: float,
    date_closed: str,
    state: str,
    borrower_name: str,
    **kwargs,
) -> Investment:
    """Convenience factory for creating a grant."""
    return Investment(
        id=make_id(),
        name=name,
        investment_type="grant",
        sector=kwargs.pop("sector", "community_facility"),
        amount=amount,
        date_closed=date_closed,
        maturity_date=kwargs.pop("maturity_date", date_closed),
        interest_rate=0.0,
        state=state,
        borrower_name=borrower_name,
        borrower_type=kwargs.pop("borrower_type", "nonprofit"),
        outstanding_balance=0.0,
        **kwargs,
    )


def add_impact(
    investment: Investment,
    jobs_created: int = 0,
    jobs_retained: int = 0,
    affordable_units: int = 0,
    sq_ft_community_space: float = 0.0,
    businesses_supported: int = 0,
    patients_served: int = 0,
    students_served: int = 0,
    **kwargs,
) -> Investment:
    """Attach impact metrics to an existing investment."""
    investment.impact = ImpactMetrics(
        investment_id=investment.id,
        jobs_created=jobs_created,
        jobs_retained=jobs_retained,
        affordable_units=affordable_units,
        sq_ft_community_space=sq_ft_community_space,
        businesses_supported=businesses_supported,
        patients_served=patients_served,
        students_served=students_served,
        **kwargs,
    )
    return investment
