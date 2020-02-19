import yfinance as yf
import matplotlib.pyplot as plt
import datetime
from yahoo_earnings_calendar import YahooEarningsCalendar
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

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

#with open("dataset.pkl","rb") as f:
#    data = pickle.load(f)





# Get the data for the stock Apple by specifying the stock ticker, start date, and end date
#data = yf.download('AAPL','2016-01-01','2018-01-01')
#print(data)
#data.Close.plot()
#plt.show()
