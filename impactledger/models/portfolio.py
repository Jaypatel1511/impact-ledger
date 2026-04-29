"""
Portfolio aggregator — tracks a collection of impact investments.
"""
from dataclasses import dataclass
from typing import Optional
import pandas as pd

from impactledger.data.schema import Investment, INVESTMENT_TYPES, SECTORS


class Portfolio:
    """
    Tracks a collection of impact investments with financial
    and social impact aggregation.

    Usage:
        p = Portfolio(name="CDFI Impact Fund I")
        p.add(investment1)
        p.add(investment2)
        p.summary()
        df = p.to_dataframe()
    """

    def __init__(self, name: str, vintage_year: Optional[int] = None):
        self.name = name
        self.vintage_year = vintage_year
        self._investments: list[Investment] = []

    def add(self, investment: Investment) -> None:
        """Add an investment to the portfolio."""
        if not isinstance(investment, Investment):
            raise TypeError("Only Investment objects can be added.")
        if any(i.id == investment.id for i in self._investments):
            raise ValueError(f"Investment '{investment.id}' already exists.")
        self._investments.append(investment)

    def remove(self, investment_id: str) -> None:
        """Remove an investment by ID."""
        self._investments = [
            i for i in self._investments if i.id != investment_id
        ]

    def count(self) -> int:
        return len(self._investments)

    def get(self, investment_id: str) -> Optional[Investment]:
        """Get a single investment by ID."""
        for inv in self._investments:
            if inv.id == investment_id:
                return inv
        return None

    def filter_state(self, state: str) -> list:
        return [i for i in self._investments if i.state == state.upper()]

    def filter_type(self, investment_type: str) -> list:
        return [i for i in self._investments if i.investment_type == investment_type]

    def filter_sector(self, sector: str) -> list:
        return [i for i in self._investments if i.sector == sector]

    def filter_status(self, status: str) -> list:
        return [i for i in self._investments if i.status == status]

    @property
    def total_committed(self) -> float:
        return sum(i.amount for i in self._investments)

    @property
    def total_outstanding(self) -> float:
        return sum(
            i.outstanding_balance for i in self._investments
            if i.outstanding_balance is not None
        )

    @property
    def active_investments(self) -> list:
        return [i for i in self._investments if i.is_active]

    @property
    def impaired_investments(self) -> list:
        return [i for i in self._investments if i.is_impaired]

    @property
    def weighted_avg_rate(self) -> float:
        total = self.total_outstanding
        if total == 0:
            return 0.0
        return sum(
            i.outstanding_balance * i.interest_rate
            for i in self._investments
            if i.outstanding_balance
        ) / total

    @property
    def annual_income(self) -> float:
        return sum(i.annual_income for i in self._investments)

    # ── Impact aggregations ───────────────────────────────────────────────────

    @property
    def total_jobs_created(self) -> int:
        return sum(
            i.impact.jobs_created for i in self._investments
            if i.impact
        )

    @property
    def total_jobs_retained(self) -> int:
        return sum(
            i.impact.jobs_retained for i in self._investments
            if i.impact
        )

    @property
    def total_jobs(self) -> int:
        return self.total_jobs_created + self.total_jobs_retained

    @property
    def total_affordable_units(self) -> int:
        return sum(
            i.impact.affordable_units for i in self._investments
            if i.impact
        )

    @property
    def total_sq_ft(self) -> float:
        return sum(
            i.impact.sq_ft_community_space for i in self._investments
            if i.impact
        )

    @property
    def pct_low_income_area(self) -> float:
        if not self._investments:
            return 0.0
        return sum(
            1 for i in self._investments if i.is_low_income_area
        ) / len(self._investments)

    @property
    def pct_minority_borrower(self) -> float:
        if not self._investments:
            return 0.0
        return sum(
            1 for i in self._investments if i.is_minority_borrower
        ) / len(self._investments)

    @property
    def pct_women_borrower(self) -> float:
        if not self._investments:
            return 0.0
        return sum(
            1 for i in self._investments if i.is_women_borrower
        ) / len(self._investments)

    @property
    def cost_per_job(self) -> float:
        if self.total_jobs == 0:
            return 0.0
        return self.total_committed / self.total_jobs

    def summary(self) -> None:
        """Print a full portfolio summary."""
        print(f"\nImpact Portfolio Summary — {self.name}")
        print("=" * 55)
        print(f"\nFINANCIAL METRICS")
        print(f"  Total Committed:       ${self.total_committed/1e6:.2f}MM")
        print(f"  Total Outstanding:     ${self.total_outstanding/1e6:.2f}MM")
        print(f"  Annual Income:         ${self.annual_income/1e6:.2f}MM")
        print(f"  Weighted Avg Yield:    {self.weighted_avg_rate*100:.2f}%")
        print(f"  Total Investments:     {self.count()}")
        print(f"  Active:                {len(self.active_investments)}")
        print(f"  Impaired:              {len(self.impaired_investments)}")
        print(f"\nIMPACT METRICS")
        print(f"  Jobs Created:          {self.total_jobs_created:,}")
        print(f"  Jobs Retained:         {self.total_jobs_retained:,}")
        print(f"  Total Jobs:            {self.total_jobs:,}")
        print(f"  Affordable Units:      {self.total_affordable_units:,}")
        print(f"  Community Sq Ft:       {self.total_sq_ft:,.0f}")
        if self.cost_per_job > 0:
            print(f"  Cost per Job:          ${self.cost_per_job:,.0f}")
        print(f"\nDEMOGRAPHICS")
        print(f"  % Low-Income Area:     {self.pct_low_income_area*100:.1f}%")
        print(f"  % Minority Borrower:   {self.pct_minority_borrower*100:.1f}%")
        print(f"  % Women Borrower:      {self.pct_women_borrower*100:.1f}%")
        print(f"\nGEOGRAPHIC REACH")
        states = set(i.state for i in self._investments)
        print(f"  States:                {len(states)}")
        print(f"  States:                {', '.join(sorted(states))}")
        print()

    def to_dataframe(self) -> pd.DataFrame:
        """Return all investments as a pandas DataFrame."""
        rows = []
        for i in self._investments:
            row = {
                "id": i.id,
                "name": i.name,
                "type": i.investment_type,
                "sector": i.sector,
                "amount": i.amount,
                "outstanding": i.outstanding_balance,
                "rate": i.interest_rate,
                "state": i.state,
                "borrower": i.borrower_name,
                "borrower_type": i.borrower_type,
                "status": i.status,
                "date_closed": i.date_closed,
                "maturity_date": i.maturity_date,
                "low_income_area": i.is_low_income_area,
                "minority_borrower": i.is_minority_borrower,
                "women_borrower": i.is_women_borrower,
                "rural": i.is_rural,
            }
            if i.impact:
                row.update({
                    "jobs_created": i.impact.jobs_created,
                    "jobs_retained": i.impact.jobs_retained,
                    "affordable_units": i.impact.affordable_units,
                    "sq_ft": i.impact.sq_ft_community_space,
                    "businesses": i.impact.businesses_supported,
                    "patients": i.impact.patients_served,
                    "students": i.impact.students_served,
                })
            rows.append(row)
        return pd.DataFrame(rows)

    def sector_breakdown(self) -> pd.DataFrame:
        """Return a sector-level summary DataFrame."""
        df = self.to_dataframe()
        return df.groupby("sector").agg(
            count=("amount", "count"),
            total_amount=("amount", "sum"),
            avg_amount=("amount", "mean"),
        ).reset_index().sort_values("total_amount", ascending=False)

    def state_breakdown(self) -> pd.DataFrame:
        """Return a state-level summary DataFrame."""
        df = self.to_dataframe()
        return df.groupby("state").agg(
            count=("amount", "count"),
            total_amount=("amount", "sum"),
        ).reset_index().sort_values("total_amount", ascending=False)
