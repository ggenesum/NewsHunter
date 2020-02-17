import yfinance as yf
import matplotlib.pyplot as plt
import datetime
from yahoo_earnings_calendar import YahooEarningsCalendar

date_from = datetime.datetime.strptime(
    'May 5 2000  10:00AM', '%b %d %Y %I:%M%p')
date_to = datetime.datetime.strptime(
    'May 8 2019  1:00PM', '%b %d %Y %I:%M%p')

yec = YahooEarningsCalendar(0)

data = yec.earnings_between(date_from, date_to)
#for new in data:
#    print(new["companyshortname"])

print(len(data))

# Get the data for the stock Apple by specifying the stock ticker, start date, and end date
#data = yf.download('AAPL','2016-01-01','2018-01-01')
#print(data)
#data.Close.plot()
#plt.show()
