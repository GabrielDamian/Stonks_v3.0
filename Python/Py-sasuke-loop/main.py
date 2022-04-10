import time
import random
from utils import *
from graphHandler import *
import datetime
import time
#TODO: check future price custom based on the current patterns
#GLOBALS
decisions = None
global_buffer = []
tik_tok = 0.1 #clock intervals
time_check_old_decisions = 600000

global_fake_api_next = []
last_used = 0


def readDataFromExcelFile(fileName, linesToRead):
    # print("Citesc date din fisier...")

    vector = []
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                pass

                y = row[1].split()

                if len(y) >= 2:
                    z = y[1].split(':')
                    final_time = int(z[1])

                vector.append(row[3])
                line_count += 1
            linesToRead -= 1
            if linesToRead < 0:
                break
        # print(f'Processed {line_count} lines.')

        # primul elem din arr este un header de tip string (trash de la citire)
        del vector[0]
        # inverseaza ordinea in vector
        # vector = vector[::-1]

        float_arr = []
        for x in vector:
            float_arr.append(float(x))
        return float_arr

def integratedNarutoMain(points, candleSize,filter_candles_1,filter_candles_2):
    graph = graphData()

    vector = points #wtf man

    graph.setInputData(vector)

    graph.inputToCandle(candleSize=candleSize)
    print("input to candle:",len(graph.candlesData))

    graph.filterCandles(filter_candles_1, filter_candles_2)
    print("input to candle filtered:",len(graph.candlesData))

    graph.candlesToFunctionWork(candleSize)

    graph.generateInternPoints()

    #FINAL DATA IN graph.candlesToFunction
    # for a in graph.candlesToFunction:
    #     print(a)

    print("intern:")
    print("one:",len(graph.inputData))
    print("three:",len(graph.candlesToFunction))

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
    #citeste pattern din fisier si adauga in structura template pentru patterns
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

def findMinSizePattern(patterns):
    min = patterns[0]["size"]
    for a in patterns:
        if(a["size"]<min):
            min = a["size"]
    return min

def initFormatDecisions(referinteTerraForm):
    final = {}
    for a in referinteTerraForm:
        final[a["fileName"]] = []
    return final

def fakeApi():
    return round(random.random()*100,2)

def crossCorelation(base, seg_2):
    print("cross cor:")
    print("base:", base)
    print("seg_2:", seg_2)

    #yScallerEnaber and powerSum are default here
    max_y_var = seg_2[0][1];

    for a  in seg_2:
        if a[1] > max_y_var:
            max_y_var = a[1]

    max_y_base = base[0]
    for a in base:
        if a > max_y_base:
           max_y_base = a

    y_ratio = max_y_base / max_y_var

    suma_scaled = 0
    i = 0
    while i < len(base):
        var = base[i] - seg_2[i][1] * y_ratio
        suma_scaled += var * var
        i += 1

    return suma_scaled

def completeOldDecisions(currentStockPrice):
    for a in decisions:
        for b in decisions[a]:
            curentTimeStamp = round(time.time() * 1000)

            if curentTimeStamp - b["start_date"] < time_check_old_decisions and b["end_data"] == None:
                decisions[a][b]["end_date"] = curentTimeStamp
                decisions[a][b]["end_price"] = currentStockPrice

    #TODO:
    #overrwrite new decision into file (! not append)

def printFinalPattern(final_patterns):
    for a in final_patterns:
        print("\n\nNew pattern:---------")
        print("source:",a["source"])
        print("size:",a["size"])
        # print(a["pytonTerraForm"])
        for x in a["pytonTerraForm"]:
            print(x,":",a["pytonTerraForm"][x])
        print("values:")
        for index,b in enumerate(a["values"]):
            if index < 5:
                print(b)

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
            "fileName": "pattern_3.txt",
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

    decisions = initFormatDecisions(referinteTerraForm)

    # printFinalPattern(final_patterns);

    min_patt_size_seg_unic = findMinSizePattern(final_patterns)


    while True:
        print("new clock")

        time.sleep(tik_tok)
        new_fetch_value = fakeApi()
        global_buffer.append(new_fetch_value)

        print("global_buffer update:", global_buffer)

        for a in final_patterns:

            #parcuge toate patterns
            # terraForm update buffer
            # verifica daca daca ultime x element trec crossCor cu abatere hard pentru fiecare din patterns

            if len(global_buffer) > min_patt_size_seg_unic:

                last_x_points = global_buffer[:a["size"]+10]
                candle_size = float(a["pytonTerraForm"]["candle_size"])
                filter_1 = float(a["pytonTerraForm"]["filter_1"])
                filter_2 = float(a["pytonTerraForm"]["filter_2"])

                #terraForm last x from buffer for this custom pattern format
                last_snap_format = integratedNarutoMain(last_x_points,candle_size, filter_1,filter_2)

                #pentru gruparea pattern_x, afla care este cel mai mic cross Corr si compara cu abatere hard
                min_cross_cor = crossCorelation(a["values"][0], last_snap_format)
                which_one_pattern_var = None

                for b in a["values"]:
                    if crossCorelation(b, last_snap_format) < min_cross_cor:
                        min_cross_cor = crossCorelation(b, last_snap_format)
                        which_one_pattern_var = b

                if min_cross_cor < a["pytonTerraForm"]["abatere_hard"]:
                    #DECIZIE CUMPARARE pentru gruparea de pattern_x
                    entitate_decizie = {
                        "start_date": round(time.time() * 1000),
                        "start_price": global_buffer[len(global_buffer)-1], #ultimul element din buffer
                        "end_data": None,
                        "end_price": None,
                        "more":{
                            "which_one_pattern_var": which_one_pattern_var,
                            "min_cross_cor": min_cross_cor
                        }
                    }
                    decisions[a["source"]].append(entitate_decizie)
            else:
                print("buffer loading")

        #completare decizii in asteptare
        completeOldDecisions(new_fetch_value)
