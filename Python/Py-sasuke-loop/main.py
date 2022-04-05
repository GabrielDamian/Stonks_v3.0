import time
import random
from utils import *
from graphHandler import *

def integratedNarutoMain(points, candleSize,filter_candles_1,filter_candles_2):
    graph = graphData()

    vector = points #wtf man

    graph.setInputData(vector)

    graph.inputToCandle(candleSize=candleSize)

    graph.filterCandles(filter_candles_1, filter_candles_2)

    graph.candlesToFunctionWork(candleSize)

    graph.generateInternPoints()

    #FINAL DATA IN graph.candlesToFunction
    for a in graph.candlesToFunction:
        print(a)

    return graph.candlesToFunction

def readFromFile(fileName):
    file1 = open(fileName, 'r')
    lines = file1.readlines()
    patterns = []
    for a in lines:
        pairs_str = a[0:len(a)-2].split("/")
        single_pattern = []

        for b in pairs_str:
            split_point = b.split(",")
            single_pattern.append(float(split_point[1]))
        patterns.append(single_pattern)
    return patterns

def terraFormPatterns(referinteTerraForm, size_seg_unic, candleSize, filter_1, filter_2, abatere_hard):
    # obj = {
    #     values: [..],
    #     size: 10,
    #     pythonTerraForm:{
    #         candle_size: 10,
    #         filter_1: 20,
    #         filter_2: 30
    #     }
    # }

    patterns = readFromFile(referinteTerraForm)

    obj = {}

    obj["values"] = patterns
    obj["size"] = size_seg_unic
    obj["source"] = referinteTerraForm
    obj["pytonTerraForm"] = {}
    obj["pytonTerraForm"]["candle_size"] = candleSize
    obj["pytonTerraForm"]["filter_1"] = filter_1
    obj["pytonTerraForm"]["filter_2"] = filter_2
    obj["pytonTerraForm"]["abatere_hard"] = abatere_hard

    return obj

def fakeApi():
    return round(random.random()*100,2)

if __name__ == '__main__':

    referinteTerraForm = [
        {
            "fileName": "pattern_1.txt",
            "seg_seg_unic":40,
            "candle_size": 2,
            "filter_1": 0.3,
            "filter_2": 0.5,
            "abatere_hard": 500
        },
        {
            "fileName": "pattern_2.txt",
            "seg_seg_unic": 40,
            "candle_size": 2,
            "filter_1": 0.3,
            "filter_2": 0.5,
            "abatere_hard": 1000
        },
        {
            "fileName": "pattern_2.txt",
            "seg_seg_unic": 40,
            "candle_size": 2,
            "filter_1": 0.3,
            "filter_2": 0.5,
            "abatere_hard": 2000
        }
]

    final_patterns = []

    for a in referinteTerraForm:
        final_patterns.append(terraFormPatterns(a["fileName"],a["seg_seg_unic"],a["candle_size"],a["filter_1"],a["filter_2"],a["abatere_hard"]))

    global_buffer = []
    decisions = []

    for a in final_patterns:
        print("\n\nnew patt")
        print("source:",a["source"])
        print("values:")
        for index,b in enumerate(a["values"]):
            if(index < 20):
                print(b)

    while True:
        print("new clock")
        time.sleep(0.1)
        #TODO:
        #fetch api
        new_fetch_value = fakeApi()
        global_buffer.append(new_fetch_value)
        print("global_buffer update:", global_buffer)

        #iterate final_patterns and generate new custom buffer based on candleSize, filter_1, filter_2
        for a in final_patterns:
            #temp structure

            if len(global_buffer) > 40: #40 = maxim of the size_seg_unic use cases
                print("caz 1")
                last_40_points = global_buffer[:a["size"]]
                candle_size = float(a["pytonTerraForm"]["candle_size"])
                filter_1 = float(a["pytonTerraForm"]["filter_1"])
                filter_2 = float(a["pytonTerraForm"]["filter_2"])

                last_snap_format = integratedNarutoMain(last_40_points,candle_size, filter_1,filter_2)
                print("last_snap_format:",last_snap_format)

                #TODO:
                #cross corelation with all pattern in the "value"
                #if current_cross < specific_abatere_hard, simulate a buy
            else:
                print("buffer loading")

    #iterate decision and decide if is the correct time to complete a decision (buyed_time + 10m = NOW)


