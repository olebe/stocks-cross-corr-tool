import cbpro
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#public client
public_client = cbpro.PublicClient()

#authenticate private client
auth= pd.read_csv('auth.txt',header=None)
key = auth.iloc[0][0]
secret = auth.iloc[1][0]
passphrase = auth.iloc[2][0]
auth_client = cbpro.AuthenticatedClient(key, secret, passphrase)



##  public client functions

def historic_price (product, start= None, end= None, granularity=300):
    #product example: 'REN-USD'
    #possible granularities: [60, 300, 900, 3600, 21600, 86400]
    historic= pd.DataFrame(public_client.get_product_historic_rates(product,start=None, end=None,granularity= granularity))
    historic[0]= pd.to_datetime(historic[0], unit='s')
    historic= historic.rename(columns={0: "time", 1: "low",2: "high", 3: "open",4: "close", 5: "volume"})
    historic=historic.sort_values ('time')
    return historic

def bollinger (df, window=15, no_of_std=2 ):
    #Set number of days (window) and standard deviations (no_of_std) to use for rolling lookback period for Bollinger band calculation

    #Calculate rolling mean and standard deviation using number of days set above
    rolling_mean = df['close'].rolling(window).mean()
    rolling_std = df['close'].rolling(window,min_periods=window).std()

    #create two new DataFrame columns to hold values of upper and lower Bollinger bands
    
    df['Rolling Mean'] = rolling_mean
    df['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
    df['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)
    df= df.set_index('time')
    
    return df


## private client functions

def show_account():
    account = pd.DataFrame(auth_client.get_accounts())
    account_num = account
    account_num['balance'] = pd.to_numeric(account.balance, downcast = 'float')
    account_num['available'] = pd.to_numeric(account.available, downcast = 'float')
    account_num['hold'] = pd.to_numeric(account.hold, downcast = 'float')
    return account_num

def get_current_account_prices(accounts):
    # Initiate array
    currentprice = np.zeros(len(accounts))

    for i in range(len(accounts)):

        #print (accounts['currency'].iloc[i])
        temp_currency=accounts['currency'].iloc[i]

        # Get ticker
        ticker = public_client.get_product_ticker(product_id=temp_currency+'-EUR')

        # Check for reply error
        if 'bid' in ticker.keys():
            # Extract bid from reply
            temp_price = pd.to_numeric(ticker['bid'], downcast = 'float')

            # Add to array
            currentprice[i] = temp_price
        else:
            currentprice[i] = np.nan

        # Insert array in dataframe
        accounts['Current_price_in_EUR'] = currentprice
            
    return accounts



print('Which coins do I own?')

accounts = show_account()
accounts_notzero = accounts[accounts['balance']!=0].reset_index()
accounts_with_prices = get_current_account_prices(accounts_notzero)
print(accounts_with_prices.to_string())


print('\n\n\n\nShow Bollinger Bands for EOS-EUR')


price_hist= historic_price ('BTC-EUR', granularity = 21600)
price = bollinger(price_hist,20,2)

# Plot time trace
price[['close','Bollinger High','Bollinger Low','Rolling Mean']].plot(figsize= (20,10))
plt.ylabel('Price (EUR)')
plt.title('BTC-EUR')
plt.show()
