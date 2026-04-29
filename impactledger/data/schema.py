from dataclasses import dataclass, field
from typing import Optional
from datetime import date


# Supported investment types
INVESTMENT_TYPES = {
    "loan":             "Private debt / direct lending",
    "equity":           "Equity investment",
    "grant":            "Grant or forgivable loan",
    "nmtc":             "New Markets Tax Credit investment",
    "guarantee":        "Loan guarantee",
    "bond":             "Bond or debenture",
}

# Supported sectors
SECTORS = {
    "affordable_housing":   "Affordable housing development",
    "small_business":       "Small business lending",
    "community_facility":   "Community facility (health, education, etc.)",
    "healthcare":           "Healthcare facility",
    "education":            "Educational facility",
    "food_access":          "Food access / grocery",
    "childcare":            "Childcare facility",
    "mixed_use":            "Mixed-use development",
    "commercial_re":        "Commercial real estate",
    "microenterprise":      "Microenterprise lending",
    "other":                "Other",
}

# Borrower types
BORROWER_TYPES = {
    "nonprofit":        "Nonprofit organization",
    "for_profit":       "For-profit business",
    "cdfi":             "Community Development Financial Institution",
    "government":       "Government entity",
    "individual":       "Individual borrower",
    "cooperative":      "Cooperative",
}

# Investment status
STATUSES = {
    "active":       "Active / performing",
    "watch":        "Watch list",
    "default":      "In default",
    "repaid":       "Fully repaid",
    "written_off":  "Written off",
}


@dataclass
class ImpactMetrics:
    """
    Social impact metrics associated with a single investment.
    All metrics are optional — track what is relevant to your portfolio.
    """
    investment_id: str
    jobs_created: int = 0
    jobs_retained: int = 0
    affordable_units: int = 0
    sq_ft_community_space: float = 0.0
    businesses_supported: int = 0
    patients_served: int = 0
    students_served: int = 0
    meals_served: int = 0
    childcare_slots: int = 0
    notes: Optional[str] = None

    @property
    def total_jobs(self) -> int:
        return self.jobs_created + self.jobs_retained


@dataclass
class Investment:
    """
    Core investment record for an impact portfolio.
    Covers loans, equity, grants, NMTC deals, and guarantees.
    """
    id: str
    name: str
    investment_type: str
    sector: str
    amount: float
    date_closed: str
    maturity_date: str
    interest_rate: float
    state: str
    borrower_name: str
    borrower_type: str
    status: str = "active"
    census_tract: Optional[str] = None
    county: Optional[str] = None
    is_low_income_area: bool = False
    is_distressed_area: bool = False
    is_minority_borrower: bool = False
    is_women_borrower: bool = False
    is_rural: bool = False
    outstanding_balance: Optional[float] = None
    interest_received: float = 0.0
    principal_received: float = 0.0
    impact: Optional[ImpactMetrics] = None
    notes: Optional[str] = None

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError(f"Investment '{self.name}': amount must be positive")
        if self.investment_type not in INVESTMENT_TYPES:
            raise ValueError(
                f"Investment '{self.name}': investment_type must be one of "
                f"{list(INVESTMENT_TYPES.keys())}"
            )
        if self.sector not in SECTORS:
            raise ValueError(
                f"Investment '{self.name}': sector must be one of "
                f"{list(SECTORS.keys())}"
            )
        if self.borrower_type not in BORROWER_TYPES:
            raise ValueError(
                f"Investment '{self.name}': borrower_type must be one of "
                f"{list(BORROWER_TYPES.keys())}"
            )
        if self.status not in STATUSES:
            raise ValueError(
                f"Investment '{self.name}': status must be one of "
                f"{list(STATUSES.keys())}"
            )
        if not (0 <= self.interest_rate < 1):
            raise ValueError(
                f"Investment '{self.name}': interest_rate must be between 0 and 1"
            )
        if self.outstanding_balance is None:
            self.outstanding_balance = self.amount

    @property
    def amount_mm(self) -> float:
        return self.amount / 1_000_000

    @property
    def annual_income(self) -> float:
        return self.outstanding_balance * self.interest_rate

    @property
    def is_active(self) -> bool:
        return self.status == "active"

    @property
    def is_impaired(self) -> bool:
        return self.status in ("watch", "default")

    def __repr__(self):
        return (
            f"Investment(id='{self.id}', name='{self.name}', "
            f"type='{self.investment_type}', amount=${self.amount_mm:.2f}MM, "
            f"state='{self.state}', status='{self.status}')"
        )
