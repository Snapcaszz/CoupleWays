from datetime import datetime
from dateutil.relativedelta import relativedelta


def months_between_dates(date1: datetime, date2: datetime) -> float:
    delta = relativedelta(date2, date1)
    months = delta.years * 12 + delta.months + delta.days / 30.0
    return months

def money_string_to_float(value):
    try:
        # Remove currency symbols and commas
        value = value.replace('R$', '').replace('$', '').replace(',', '')

        # Convert the string to a float
        result = float(value)
        return result
    except ValueError:
        return None
