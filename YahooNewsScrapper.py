import datetime
from yahoo_earnings_calendar import YahooEarningsCalendar
import pickle

date_from = datetime.datetime.strptime(
    'Jan 29 2017  10:00AM', '%b %d %Y %I:%M%p')
date_to = datetime.datetime.strptime(
    'Feb 16 2020  1:00PM', '%b %d %Y %I:%M%p')

yec = YahooEarningsCalendar()

data = yec.earnings_between(date_from, date_to)

print(len(data))

with open("earnings.pkl","wb") as f:
    pickle.dump(data,f)
