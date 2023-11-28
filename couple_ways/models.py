from dataclasses import dataclass, asdict
from datetime import datetime
from couple_ways.utils.functions import months_between_dates


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
    rating: int = 0
    trip_itinerary: str = None
    video_of_the_trip: str = None
    date_to_start_saving: datetime = None
    hotel: str = None
    hotel_description: str = None
    hotel_link: str = None
    cost_of_stay: float = 0
    transportation_cost: float = 0
    amount_to_spend: float = 0
    total_expenses: float = 0
    amount_to_save: float = 0
    amount_to_save_per_people: float = 0

    def _calculate_fields(self):
        
        if self.cost_of_stay and self.transportation_cost and self.amount_to_spend:
            self.total_expenses = self.cost_of_stay + self.transportation_cost + self.amount_to_spend
            if self.date_to_start_saving:
                self.amount_to_save = (self.total_expenses - self.current_budget) / months_between_dates(
                    self.date_to_start_saving, self.start_date
                )
            else:
                self.amount_to_save = 0
            self.amount_to_save_per_people = self.amount_to_save / len(self.travelers)

    def recalculate_fields(self):
        self._calculate_fields()
        
    def to_dict(self):
        trip_dict = asdict(self)
        trip_dict["start_date"] = datetime.combine(self.start_date, datetime.min.time())
        trip_dict["end_date"] = datetime.combine(self.end_date, datetime.min.time())
        return trip_dict