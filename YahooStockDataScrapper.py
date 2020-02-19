import yfinance as yf
import matplotlib.pyplot as plt
import datetime
from yahoo_earnings_calendar import YahooEarningsCalendar
import pickle
import numpy as np

historydays = 200 #how many days before the report are we looking to predict the news impact
futurdays = 50 #maximum trend duration after report is released

date_from = datetime.datetime.strptime(
    'Jan 29 2017  10:00AM', '%b %d %Y %I:%M%p')
date_to = datetime.datetime.strptime(
    'Feb 16 2020  1:00PM', '%b %d %Y %I:%M%p')

def parsedate(date):
    sd = date.split('-')
    sd[-1] = sd[-1].split('T')[0]
    d = datetime.date(int(sd[0]),int(sd[1]),int(sd[2]))
    return d

def slicedate(pendasarr):
    return pendasarr.loc[d:d+datetime.timedelta(days=futuredays)]
    #+datetime.timedelta(days=1)

with open("earnings.pkl","rb") as f:
    data = pickle.load(f)

usable = [d for d in data if d["epsestimate"] and d["epssurprisepct"]]
#print(usable[0])

for n in usable: 
    d = parsedate(n["startdatetime"])
    try:
        if (d<(datetime.datetime.strptime('Feb 16 2020  1:00PM', '%b %d %Y %I:%M%p')-datetime.timedelta(days=futurdays)).date()):
            n["data"] = yf.download(n["ticker"],(d-datetime.timedelta(days=historydays)).strftime("%Y-%m-%d"),(d+datetime.timedelta(days=futurdays)).strftime("%Y-%m-%d"))
        else:
            usable.remove(n)
    except:
            usable.remove(n)        
                 
print(len(data))
print(len(usable))
print(len(usable)/len(data)) #71% of 50720 reports are usable : 36367

with open("dataset.pkl","wb") as f:
    pickle.dump(usable,f)


# Get the data for the stock Apple by specifying the stock ticker, start date, and end date
#data = yf.download('AAPL','2016-01-01','2018-01-01')
#print(data)
#data.Close.plot()
#plt.show()
