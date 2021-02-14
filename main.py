# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as 
import urllib.request
import datetime
import csv

FN = 'TIME_SERIES_INTRADAY'
SYMBOL = 'IBM'
API_KEY = 'E00DIIJTEJSPZ8KZ'

def getApiUrl(fn, symbol):
    return "https://www.alphavantage.co/query?function={fn}&symbol={symbol}&apikey={API_KEY}&datatype=csv".format(fn=fn, symbol=symbol, API_KEY=API_KEY)

def getStonkInfo():
    date = []
    close_price = []
    url = getApiUrl(FN, SYMBOL)
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    csv_reader = csv.reader(lines)


    for line in csv_reader:
        date.append(datetime.datetime.strptime(line[0], '%m/%d/%Y'))
        close_price.append(float(line[4]))

    return date, close_price

    

# with open('SPCE_cuphandle.csv', 'r') as stock_values:
#     csv_reader = csv.reader(stock_values)

#     next(csv_reader)

#     for line in csv_reader:
#         date.append(datetime.datetime.strptime(line[0], '%m/%d/%Y'))
#         close_price.append(float(line[4]))

# print(date)
# print(close_price)

def is_cup_with_handle(time_vector, price_vector):
    date, close_price = getStonkInfo()

    # takes in a time vector (list of dates) and price vector (list of prices)
    # returns 0 (not a current cup with handle pattern) or 1 (is a current cup with handle pattern)

    window = 3
    p = pd.Series(price_vector)

    # make list of means in rolling window
    mov_mean = p.rolling(window).mean()
    mov_mean = pd.Series.tolist(mov_mean)
    mov_mean = mov_mean[window-1:]

    # make list of standard deviations in rolling window
    mov_std = p.rolling(window).std()
    mov_std = pd.Series.tolist(mov_std)
    mov_std = mov_std[window - 1:]

    # find dates with high means and standard deviations
    mov_mean_average = np.mean(mov_mean)
    mov_mean = mov_mean / mov_mean_average
    mov_std_average = np.mean(mov_std)
    mov_std = mov_std/mov_std_average
    peak_dates = []
    for i, val in enumerate(mov_mean):
        if val < 1:
            continue
        if mov_std[i] < 3.8:
            continue
        peak_dates.append(time_vector[i])

    # check if days between peaks is long enough
    days_between_peaks = (peak_dates[0]-peak_dates[1]).days
    if days_between_peaks > 25:
        return 1
    else:
        return 0

print(is_cup_with_handle(date, close_price))

# r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo')
# print(r.status_code)
# stock_data = r.json()
# symbol = stock_data['Meta Data']['2. Symbol']
# print(symbol)
# price = []
# time = []
# for timestamp in stock_data['Time Series (5min)'].items():
#     time.append(datetime.datetime.strptime(timestamp[0], '%Y-%m-%d %H:%M:%S'))
#     price.append(float(timestamp[1]['4. close']))
# time.reverse()
# price.reverse()
# print(time)
# print(price)
#
# fig, ax = plt.subplots()
# ax.plot(time,price)
# ax.set_title(f'{symbol}')
# plt.xticks(rotation=45)
#
# plt.show()
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/