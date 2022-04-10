from utils import *
from graphHandler import *
# import matplotlib.pyplot as plt
import sys

if __name__ == '__main__':

    #print("new py");
    #print('-->Start Stage 1:')

    candleSize = float(sys.argv[1])
    filter_candles_1 = float(sys.argv[2])
    filter_candles_2 = float(sys.argv[3])
    source = sys.argv[4]
    destination = sys.argv[5]
    

    #print("-candle size py:", candleSize)
    #print("-filter_1 py:", filter_candles_1)
    #print("-filter_2 py:", filter_candles_2)
    #print("-source py", source);
    #print("-destination py",destination);


    #candleSize = 3
    #filter_candles_1 = 0.1
    #filter_candles_2 = 0.5

    graph = graphData()

    vector = readDataFromFile(source, linesToRead=40000)
    #vector = readDataFromFile('AAPL.csv', linesToRead=6000)

    graph.setInputData(vector)
    # graph.printInputData()
    # graph.plotInputData('data')

    graph.inputToCandle(candleSize=candleSize)
    # graph.plotCandles('Candle Data')

    graph.filterCandles(filter_candles_1,filter_candles_2)
    # graph.plotCandles('Candle Filtered Data')

    graph.candlesToFunctionWork(candleSize)
    # graph.plotCandlesToFunction('Without intern points')

    #print("Adaug puncte intermediare...")
    graph.generateInternPoints()
    # graph.plotCandlesToFunction('data')
    # graph.printCandlesToFunction()

    #print("Initializez C++ string...")
    string_file = ''

    last_x = None
    for a in graph.candlesToFunction:
        if a[0] == last_x:
            continue
        string_file +='{} {}\n'.format(a[0],a[1])
        last_x = a[0]

    # f = open("Cdata.txt","w")
    # f = open("../../ConsoleApplication1/data.txt","w")

    #print("CEVA",string_file)
    
    f = open(destination, "w")

    f.write(string_file)
    f.close()
    # plt.show()
