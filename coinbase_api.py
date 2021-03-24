import cbpro
import pandas as pd
import matplotlib.pyplot as plt



public_client = cbpro.PublicClient()


def historic_price (product, start= None, end= None, granularity=300):
    #product example: 'REN-USD'
    #possible granularities: [60, 300, 900, 3600, 21600, 86400]
    historic= pd.DataFrame(public_client.get_product_historic_rates(product,start=None, end=None,granularity= granularity))
    historic[0]= pd.to_datetime(historic[0], unit='s')
    historic= historic.rename(columns={0: "time", 1: "low",2: "high", 3: "open",4: "close", 5: "volume"})
    return historic


price_hist= historic_price ('BTC-EUR', granularity = 60)



plt.plot(price_hist.time, price_hist.close)
plt.ylabel('€/BTC')
#plt.plot(price_hist.time, price_hist.open)
#plt.bar(eth_hist.time, eth_hist.volume)

plt.xticks(rotation=45)
