from math import floor
from dataclasses import dataclass, asdict
from datetime import datetime
from couple_ways.utils.functions import (
    months_between_dates,
    youtube_url_to_embed,
    days_between_dates,
)


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
    embed_video: str = None
    date_to_start_saving: datetime = None
    hotel: str = None
    hotel_description: str = None
    hotel_link: str = None
    cost_of_stay: float = 0  # daily cost of stay
    transportation_cost: float = 0  # plane ticket for a round trip
    amount_to_spend: float = 0
    total_expenses: float = 0
    amount_to_save: float = 0
    amount_to_save_per_people: float = 0

    def calculate_fields(self):
        if self.cost_of_stay and self.transportation_cost and self.amount_to_spend:
            self.total_expenses = (
                self.cost_of_stay * days_between_dates(self.start_date, self.end_date)
                + self.transportation_cost * len(self.travelers)
                + self.amount_to_spend
            )
            if floor(months_between_dates(self.date_to_start_saving, self.start_date)) >= 1:
                self.amount_to_save = (
                    self.total_expenses - self.current_budget
                ) / floor(months_between_dates(self.date_to_start_saving, self.start_date))
            else:
                self.amount_to_save = self.total_expenses - self.current_budget
            self.amount_to_save_per_people = self.amount_to_save / len(self.travelers)

    def get_embed(self):
        if self.video_of_the_trip:
            self.embed_video = youtube_url_to_embed(self.video_of_the_trip)
