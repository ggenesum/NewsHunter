import yfinance as yf
import matplotlib.pyplot as plt
import datetime
from yahoo_earnings_calendar import YahooEarningsCalendar
import pickle
import numpy as np

historydays = 200 #how many days before the report are we looking to predict the news impact
futuredays = 50 #maximum trend duration after report is released
slowMAdays = 30
fastMAdays = 4
ignore_breakpoints_days = 0 #ignore breakpoints if it is right after the report is released.
#this is because sometimes surprise was somehow anticipated, but sometimes not and there is a breakpoint after the new is released

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

def breakpoint(fastMA,slowMA,d):
    diff = slowMA - fastMA
    dates = []
    prevs = 0 if diff[0] > 0 else 1
    for date in diff.index:
        s = 0 if diff[date] > 0 else 1
        if s != prevs:
            prevs = s
            if date > d + datetime.timedelta(days=ignore_breakpoints_days):
                return (date,s)
    return (d+datetime.timedelta(days=futuredays-1),2)
    
with open("earnings.pkl","rb") as f:
    data = pickle.load(f)

usable = [d for d in data if d["epsestimate"] and d["epssurprisepct"] and d["startdatetime"]]
#print(usable[0])

for n in usable: 
    d = parsedate(n["startdatetime"])
    if (d<(datetime.datetime.strptime('Feb 16 2020  1:00PM', '%b %d %Y %I:%M%p')-datetime.timedelta(days=50)).date()):
        n["pastdata"] = yf.download(n["ticker"],(d-datetime.timedelta(days=historydays)).strftime("%Y-%m-%d"),(d-datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
        futurdata = yf.download(n["ticker"],(d-datetime.timedelta(days=slowMAdays)).strftime("%Y-%m-%d"),(d+datetime.timedelta(days=futuredays)).strftime("%Y-%m-%d"))

        fastMA = futurdata[["Open","High","Low","Close"]].rolling(str(fastMAdays)+'d').mean().mean(axis=1)
        slowMA = futurdata[["Open","High","Low","Close"]].rolling(str(slowMAdays)+'d').mean().mean(axis=1)

        fastMA = slicedate(fastMA)
        slowMA = slicedate(slowMA)
        plt.plot(fastMA,label="fastMA")
        plt.plot(slowMA,label="slowMA")
        plt.plot(futurdata[["Open","High","Low","Close"]].mean(axis=1),label="OHLC")
        plt.title(n["ticker"] + "@" + d.strftime("%Y-%m-%d") + ": surprise " + str(n["epssurprisepct"]))
        plt.legend()
        bp = breakpoint(fastMA,slowMA,d)
        if bp[1] == 0: #sell
            plt.axvline(bp[0], color='r')
        elif bp[1] == 1:
            plt.axvline(bp[0], color='g')
        else:
            plt.axvline(bp[0], color='b')
        plt.axvline(d, color='k')   
        plt.show()
        #input()
    else:
        usable.remove(n)
                 
print(len(data))
print(len(usable))
print(len(usable)/len(data)) #71% of 50720 reports are usable : 36367 

# Get the data for the stock Apple by specifying the stock ticker, start date, and end date
#data = yf.download('AAPL','2016-01-01','2018-01-01')
#print(data)
#data.Close.plot()
#plt.show()
