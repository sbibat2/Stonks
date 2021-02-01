# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import matplotlib.pyplot as plt
import numpy as np
import datetime

r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo')
print(r.status_code)
stock_data = r.json()
symbol = stock_data['Meta Data']['2. Symbol']
print(symbol)
price = []
time = []
for timestamp in stock_data['Time Series (5min)'].items():
    time.append(datetime.datetime.strptime(timestamp[0], '%Y-%m-%d %H:%M:%S'))
    price.append(float(timestamp[1]['4. close']))
time.reverse()
price.reverse()
print(time)
print(price)

fig, ax = plt.subplots()
ax.plot(time,price)
ax.set_title(f'{symbol}')
plt.xticks(rotation=45)

plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/