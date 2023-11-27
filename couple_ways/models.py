from dataclasses import dataclass, field
from datetime import datetime
from couple_ways.utils.functions import months_between_dates, money_string_to_float


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
    rate: int = 0
    current_budget_value: float = 0
    trip_description: str = None
    videos_of_the_trip: list[str] = field(default_factory=list)
    date_to_start_saving: datetime = None
    accommodation: str = None
    hotel_link: str = None
    cost_of_stay: float = 0
    transportation_cost: float = 0
    amount_to_spend: float = 0
    total_expenses: float = 0
    amount_to_save: float = 0
    amount_to_save_per_people: float = 0

    def __post_init__(self):
        self.current_budget_value = money_string_to_float(self.current_budget)

    def _calculate_fields(self):
        
        if self.cost_of_stay and self.transportation_cost and self.amount_to_spend:
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