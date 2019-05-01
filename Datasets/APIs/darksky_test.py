from darksky import forecast
from datetime import datetime as dt

BOSTON = 42.3601, 71.0589
key = "e53a7fb47f4d7ba0b9ed61f4ff7d2fed"
with forecast('e53a7fb47f4d7ba0b9ed61f4ff7d2fed', *BOSTON) as boston:
    print(boston.daily.summary, end='\n---\n')
    for day in boston.daily:
        day = dict(day = date.strftime(weekday, '%a'),
                   sum = day.summary,
                   tempMin = day.temperatureMin,
                   tempMax = day.temperatureMax
                   )
        print('{day}: {sum} Temp range: {tempMin} - {tempMax}'.format(**day))
        weekday += timedelta(days=1)