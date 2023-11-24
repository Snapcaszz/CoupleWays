from dataclasses import dataclass, field
from datetime import datetime
from dateutil.relativedelta import relativedelta


def months_between_dates(date1, date2):
    delta = relativedelta(date2, date1)
    months = delta.years * 12 + delta.months + delta.days / 30.0
    return months


@dataclass
class Trip:
    # REQUIRED DATA
    _id: str
    destination: str
    start_date: datetime
    end_date: datetime
    current_budget: float
    travelers: list[str]
    # OPTIONAL DATA
    trip_description: str = None
    videos_of_the_trip: list[str] = field(default_factory=list)
    travelers: list[str] = field(default_factory=list)
    date_to_start_saving: datetime = None
    accommodation: str = None
    hotel_link: str = None
    cost_of_stay: float = 0
    transportation_cost: float = 0
    amount_to_spend: float = 0
    total_expenses: float = cost_of_stay + transportation_cost + amount_to_spend
    amount_to_save: float = total_expenses / months_between_dates(
        date_to_start_saving, start_date
    )  # Amount to save per people per month
