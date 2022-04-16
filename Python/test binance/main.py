
import json
import time
from datetime import datetime
import os
from binance import Client

import pandas as pd
import datetime, time

import requests

key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

user_key = 'TJM6qO3fMv7XjRfhiNfdwwuCEwAyGMNJNSjL0o1lPWr6fnTKU7fInWxED4Oi8KVm'
secret_key = 'odcu1Jnd4uuqJaIXcNCt6FTRAyKCRIj9brWTIRAQQPBM7IGKmRNiwH5y8YQF4UJj'
class Ceva:

    def __init__(self):
        self.client = Client(user_key, secret_key)

    def GetHistoricalData(self, howLong):
        self.howLong = howLong
        # Calculate the timestamps for the binance api function
        self.untilThisDate = datetime.datetime.now()
        self.sinceThisDate = self.untilThisDate - datetime.timedelta(days = self.howLong)
        # Execute the query from binance - timestamps must be converted to strings !
        self.candle = self.client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, str(self.sinceThisDate), str(self.untilThisDate))

        print(len(self.candle))
        print(self.candle[0])
        test_stamp = self.candle[-1][0]
        print("tesT:", test_stamp)

        print("da:",datetime.datetime.fromtimestamp(test_stamp/1000.0))

if __name__ == '__main__':

    test = Ceva()
    while True:
        test.GetHistoricalData(1)
        time.sleep(1)