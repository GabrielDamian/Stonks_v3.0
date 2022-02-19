from utils import *
from graphHandler import *
from Tests import *

if __name__ == '__main__':

    print('-->Start Stage 1:')

    graph = graphData()
    candleSize = 5
    filter_candles_1 = 0.3
    filter_candles_2 = 0.3

    vector = readDataFromFile('AAPL.csv', linesToRead=180007)
    # testRawInputData(data=vector, cout=True,limit=10)  # x y

    graph.setInputData(vector)
    # graph.printInputData()
    # graph.plotInputData('data')

    graph.inputToCandle(candleSize=candleSize)
    # graph.plotCandles('Candle Data')

    graph.filterCandles(filter_candles_1,filter_candles_2)
    # graph.plotCandles('Candle Filtered Data')

    graph.candlesToFunctionWork(candleSize)
    # graph.plotCandlesToFunction('Without intern points')

    print("Adaug puncte intermediare...")
    graph.generateInternPoints()
    # graph.plotCandlesToFunction('data')
    # graph.printCandlesToFunction()

    print("Initializez C++ string...")
    string_file = ''

    last_x = None
    for a in graph.candlesToFunction:
        if a[0] == last_x:
            continue
        string_file +=f'{a[0]} {a[1]}\n'
        last_x = a[0]

    f = open("Cdata.txt","w")
    f.write(string_file)
    f.close()

    plt.show()
