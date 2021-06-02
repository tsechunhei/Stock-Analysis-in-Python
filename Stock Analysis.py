import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates

plt.style.use('ggplot')

df = pd.read_csv('NIFTY500.csv')
df.dropna(subset=['Close'], inplace=True)
ohlc = df[['Date', 'Open', 'High', 'Low', 'Close']]
ohlc['Date'] = pd.to_datetime(ohlc['Date'], dayfirst=True)
ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
ohlc = ohlc.astype(float)

###Create Subplots
fig, ax = plt.subplots()
candlestick_ohlc(ax, ohlc.values, width=0.3 , colorup='green', colordown='red', alpha = 0.8)

###Setting labels and titles
ax.set_xlabel('Date')
ax.set_ylabel('Price')
fig.suptitle('Daily Candlestick Chart of NIFTY500')

###Formatting Date
date_format = mpl_dates.DateFormatter('%d-%m-%Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()
fig.tight_layout()
plt.show()

###RSI
df2 = df
df2.index = pd.to_datetime(df2['Date'], dayfirst=True)
df2 = df2[['Close']]
df2.columns=['Close']
df2['Close']=pd.to_numeric(df2['Close'])
df2=df2['22-Nov-18':]


def get_Up(x):
    if x>=0:
        return x
    else:
        return 0
def get_Down(x):
    x=-x
    return get_Up(x)
df2['Change']=df2['Close'].diff()
df2['Up']=df2['Change'].apply(get_Up)
df2['Down']=df2['Change'].apply(get_Down)
df2['EMA_Up']=df2['Up'].ewm(span=14).mean()
df2['EMA_Down']=df2['Down'].ewm(span=14).mean()


df2['RS']=df2['EMA_Up'].div(df2['EMA_Down'])
df2['RSI']=df2['RS'].apply(lambda RS:(RS/(1+RS))*100)
def get_status(y):
    if y>=70:
        return('overbought')   
    elif y<=30:
        return('oversold')
    else:
        return('NaN')        
df2['Status_RSI']=df2['RSI'].apply(get_status)
df2.head(50)

plt.figure(figsize=(15,10))
df2['RSI'].plot()
plt.plot(df2.index,[30]*len(df2.index))
plt.plot(df2.index,[70]*len(df2.index))
plt.title('RSI for NIFTY500')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.show()


