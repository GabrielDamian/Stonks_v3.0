import time
from datetime import datetime
from binance import Client
import datetime, time


key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

user_key = 'TJM6qO3fMv7XjRfhiNfdwwuCEwAyGMNJNSjL0o1lPWr6fnTKU7fInWxED4Oi8KVm'
secret_key = 'odcu1Jnd4uuqJaIXcNCt6FTRAyKCRIj9brWTIRAQQPBM7IGKmRNiwH5y8YQF4UJj'


class BiananceMaster:

    def __init__(self):
        self.client = Client(user_key, secret_key)

    def GetHistoricalData(self, howLong):
        self.howLong = howLong
        # Calculate the timestamps for the binance api function
        self.untilThisDate = datetime.datetime.now()
        self.sinceThisDate = self.untilThisDate - datetime.timedelta(days = self.howLong)
        # Execute the query from binance - timestamps must be converted to strings !
        self.candle = self.client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, str(self.sinceThisDate), str(self.untilThisDate))

        # print(len(self.candle))
        # print(self.candle[0])
        test_stamp = self.candle
        # print("tesT:", test_stamp)

        # print("da:",datetime.datetime.fromtimestamp(test_stamp/1000.0))
        last_x_minutes = self.extractLastIndexes(100,test_stamp)

        return [float(a[1]) for a in last_x_minutes]
        # return last_x_minutes

    def extractLastIndexes(self,howMany, source):
        raw_prices = []
        howManyConsumer = howMany
        for a in reversed(source):
            if howManyConsumer == 0:
                break
            concat_arr = []
            concat_arr.append(a[0]) #timestamp
            concat_arr.append(a[1]) #open price

            raw_prices.append(concat_arr)
            howManyConsumer -=1

        return raw_prices
