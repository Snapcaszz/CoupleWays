from dataclasses import dataclass, field
from datetime import datetime
from utils.functions import months_between_dates, money_string_to_float


@dataclass
class Trip:
    # REQUIRED DATA
    _id: str
    destination: str
    start_date: datetime
    end_date: datetime
    current_budget: str
    travelers: list[str]
    # OPTIONAL DATA
    current_budget_value: float = field(init=False)
    trip_description: str = None
    videos_of_the_trip: list[str] = field(default_factory=list)
    date_to_start_saving: datetime = None
    accommodation: str = None
    hotel_link: str = None
    cost_of_stay: float = 0
    transportation_cost: float = 0
    amount_to_spend: float = 0
    total_expenses: float = field(init=False)
    amount_to_save: float = field(init=False)
    amount_to_save_per_people: float = field(init=False)

    def __post_init__(self):
        self.current_budget_value = money_string_to_float(self.current_budget)
        self._calculate_fields()

    def _calculate_fields(self):
        self.total_expenses = self.cost_of_stay + self.transportation_cost + self.amount_to_spend
        if self.date_to_start_saving:
            self.amount_to_save = (self.total_expenses - self.current_budget_value) / months_between_dates(
                self.date_to_start_saving, self.start_date
            )
        else:
            self.amount_to_save = 0
        self.amount_to_save_per_people = self.amount_to_save / len(self.travelers)

    def recalculate_fields(self):
        self._calculate_fields()