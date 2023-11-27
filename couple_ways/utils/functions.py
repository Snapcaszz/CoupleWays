from datetime import datetime
from dateutil.relativedelta import relativedelta


def months_between_dates(date1: datetime, date2: datetime) -> float:
    delta = relativedelta(date2, date1)
    months = delta.years * 12 + delta.months + delta.days / 30.0
    return months

def money_string_to_float(money_string):
    if money_string == '': 
        return 0
    
    # Remove currency symbols, spaces, and everything that is not a digit, dot, or comma
    cleaned_money = ''.join(char for char in money_string if char.isdigit() or char in {'.', ','})

    # Replace comma with dot as the decimal separator
    cleaned_money = cleaned_money.replace(',', '.')

    # Convert to float
    float_value = float(cleaned_money)

    return float_value