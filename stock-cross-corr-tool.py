import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Input data (index pandas series)
inputdata = yf.download(tickers='SPY', period='1mo', interval='5m')['Open']

# Stock ticker
ticker = 'GME'

# Stock data interval: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
interval = '1m'

# Stock data period: always use max available period based on interval
intervals = ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo']
periods= ['7d','60d','60d','60d','60d','730d','60d','730d','max','max','max','max','max']
freq_dict = dict(zip(intervals, periods))

period = freq_dict[interval]
# Maximum time lag (in minutes)
maxtau = 60

# Plots to debug
plotdebug = True


## Function ############################
# Download stock data series
stockdata = yf.download(tickers=ticker, period=period, interval=interval)
stockdata = stockdata['Open']

# Plot times series
if plotdebug:
    fig1, ax = plt.subplots(2,1,sharex=True)
    ax[0].plot(inputdata,'b.')
    ax[0].set_ylabel('Input data')
    ax[1].plot(stockdata,'r.',label=ticker)
    ax[1].set_ylabel('Price (USD)')
    ax[1].legend()
    plt.xticks(rotation=45)

# Time lags
taus = np.arange(0,maxtau)

# Calculate cross-correlation
cc = np.zeros(len(taus))
for ii, tau in enumerate(taus):
    cc[ii] = stockdata.corr(inputdata.shift(tau, freq='T'))

# Plot cross-correlation
fig2 = plt.figure()
plt.plot(taus, cc,'.')
plt.xlabel('Time lag (min)')
plt.ylabel('Cross-correlation')
plt.show()

