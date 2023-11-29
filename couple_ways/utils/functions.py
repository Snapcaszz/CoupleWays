from datetime import datetime
from dateutil.relativedelta import relativedelta


def months_between_dates(date1: datetime, date2: datetime) -> float:
    delta = relativedelta(date2, date1)
    months = delta.years * 12 + delta.months + delta.days / 30.0
    return months

def days_between_dates(date1: datetime, date2: datetime) -> float:
    delta = date2 - date1 
    return delta.days+1

def youtube_url_to_embed(url):
    try:
        if url: 
            url_parts = url.split("https://youtu.be/")
            embed = "https://www.youtube.com/embed/"+url_parts[1]
            return embed
    except:
        return None
    
    
date1 = datetime(2022, 1, 1)
date2 = datetime(2022, 1, 2)

result = months_between_dates(date1, date2)
print(result)