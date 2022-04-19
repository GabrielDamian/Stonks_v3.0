import random

from BinanceMaster.BinanceMaster import *
from GraphHandler.graphHandler import *
import time
import matplotlib.pyplot as plt

#TODO: check future price custom based on the current patterns
#GLOBALS
decisions = None
tik_tok = 0.1 #clock intervals
time_check_old_decisions = 600000

global_fake_api_next = []
last_used = 0

#temp declarations
fake_current_time_stamp = 110  #magic number bcs you need offset

def readDataFromExcelFile(fileName):
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
        # print(f'Processed {line_count} lines.')

        # primul elem din arr este un header de tip string (trash de la citire)
        del vector[0]
        # inverseaza ordinea in vector
        # vector = vector[::-1]

        float_arr = []
        for x in vector:
            float_arr.append(float(x))
        return float_arr

def fakeApi(last_x):
    test_location = 'LastWeek2.csv'
    raw_data = readDataFromExcelFile('LastWeeks/'+test_location)

    add_time_stamp = []
    for index, a in enumerate(raw_data):
        add_time_stamp.append([a,index])

    temp_state = add_time_stamp[fake_current_time_stamp-last_x:fake_current_time_stamp ]
    just_y = []
    for a in temp_state:
        just_y.append(a[0])
    return just_y

def plotArr(arr, id):
    #arr, just y's
    plt.figure(id)
    plt.plot(arr)

#end of temp declarations

def integratedNarutoMain(points, candleSize,filter_candles_1,filter_candles_2):
    graph = graphData()

    vector = points #wtf man

    graph.setInputData(vector)

    graph.inputToCandle(candleSize=candleSize)
    # print("input to candle:",len(graph.candlesData))

    graph.filterCandles(filter_candles_1, filter_candles_2)
    # print("input to candle filtered:",len(graph.candlesData))

    graph.candlesToFunctionWork(candleSize)

    graph.generateInternPoints()

    #FINAL DATA IN graph.candlesToFunction
    # for a in graph.candlesToFunction:
    #     print(a)

    # print("intern:")
    # print("one:",len(graph.inputData))
    # print("three:",len(graph.candlesToFunction))

    just_y = []
    for a in graph.candlesToFunction:
        just_y.append(a[1])

    return just_y

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

    print("len test:",len(patterns))

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

def crossCorelation(pattern, lastSnapTerraFormed):
    #yScallerEnaber and powerSum are default here

    # print("inside cros cor:")
    # print("patt:", pattern)
    # print("last_snap:", lastSnapTerraFormed)

    max_y_snap = max(lastSnapTerraFormed)
    max_y_patt = max(pattern)

    # print("max_y_snap:",max_y_snap)
    # print("max_y_base:",max_y_patt)
    # print("min spnap:",min(lastSnapTerraFormed))


    #test
    minus_min = [a-min(lastSnapTerraFormed) for a in lastSnapTerraFormed]

    y_ratio = max_y_patt / max(minus_min)
    test = [a*y_ratio for a in minus_min]

    # print("ratio:", y_ratio)

    # print("test:",test)

    # plotArr(test,'ceva')
    # plotArr(pattern,'ceva')
    # plt.show()


    suma_scaled = 0
    for index, a in enumerate(pattern):
        var = a - test[index]*y_ratio
        suma_scaled += var*var

    return suma_scaled

def completeOldDecisions(currentStockPrice):
    #TODO: function to fetch the current stock price
    # currentStockPrice = None

    for a in decisions:
        for index,b in enumerate(decisions[a]):
            curentTimeStamp = round(time.time() * 1000)

            if b.getEndDate() == None and curentTimeStamp - b.getStartDate() < time_check_old_decisions :
                print("decision completed")
                decisions[a][index].completeazaEndMomentum(curentTimeStamp,currentStockPrice)

    #TODO: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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

class EntityDecizie:
    def __init__(self,startDate,startPrice,endDate,endPrice,whichPatt,minCross):
            self.start_date = startDate
            self.start_price = startPrice
            self.end_date = endDate
            self.end_price = endPrice
            self.which_one_pattern_var = whichPatt
            self.min_cross_cor = minCross

    def print(self):
        print("todo print patt")
    def completeazaEndMomentum(self,endDate,endPrice):
        self.end_date = endDate
        self.end_price = endPrice

    def getStartDate(self):
        return self.start_date

    def getEndDate(self):
        return self.end_date

    def priceDiff(self):
        return self.end_price - self.start_price
    def printMe(self):
        print(self.start_price,self.end_price,self.start_date,self.end_date)

def judgeDecisions(decisionsParam):
    total = len(decisionsParam)
    success = 0
    for a in decisionsParam:
        if a.priceDiff() > 0:
            success +=1
    print("Judge Decisions:")
    print("Total:",total)
    print("Success:",success)
    print("Ratio:",(success*100)/total)

if __name__ == '__main__':

    #------initializare patterns------
    referinteTerraForm = [
        {
            "fileName": "Patterns/pattern_1.txt",
            "size_seg_unic": 30,
            "candle_size": 2,
            "filter_1": 0.3,
            "filter_2": 0.5,
            "abatere_hard": 1000
        },
]
    patterns = []
    for a in referinteTerraForm:
        patterns.append(terraFormPatterns(a["fileName"],a["size_seg_unic"],a["candle_size"],a["filter_1"],a["filter_2"],a["abatere_hard"]))
    decisions = initFormatDecisions(referinteTerraForm)
    # printFinalPattern(patterns)
    # print("len main:",len(patterns[0]["values"]))

    #------initializare Binance------ // not used yet // first pass old values iterator test
    test = BiananceMaster()

    clock_time = 3
    while True:
        print(clock_time)
        clock_time+=1

        fake_current_time_stamp +=2
        if fake_current_time_stamp == 7000:
            break

        #TODO: check how y is extracted inside fakeAPi
        last_100_min = fakeApi(100)   #just_y

        temp_last_x  = last_100_min[0:29]
        completeOldDecisions(temp_last_x[-1])

        for index, a in enumerate(patterns):
            candle_size = float(a["pytonTerraForm"]["candle_size"])
            filter_1 = float(a["pytonTerraForm"]["filter_1"])
            filter_2 = float(a["pytonTerraForm"]["filter_2"])

            last_100_min_terraFormed = integratedNarutoMain(last_100_min,candle_size,filter_1,filter_2)

            last_x_points = last_100_min_terraFormed[0:a["size"]] #x custom based on pattern specification

            # plotArr(last_100_min,index)
            # plotArr(last_100_min_terraFormed,index)
            # plotArr(last_x_points, index)
            # plt.show()

            # print("a 0 len:",len(a["values"][0]))
            # print("last x len:",len(last_x_points))

            min_cross_cor = crossCorelation(a["values"][0], last_x_points)

            which_one_pattern_var = None
            for index_b,b in enumerate(a["values"]):


                if crossCorelation(b, last_x_points) < min_cross_cor:
                    min_cross_cor = crossCorelation(b, last_x_points)
                    which_one_pattern_var = b

            print("min cross", min_cross_cor)

            if min_cross_cor < a["pytonTerraForm"]["abatere_hard"]:
                print('patt found')
                entitate_decizie = EntityDecizie(
                    round(time.time() * 1000),
                    last_x_points[-1],
                    None,
                    None,
                    which_one_pattern_var,
                    min_cross_cor
                )
                decisions[a["source"]].append(entitate_decizie)

    print("decision:",len(decisions))
    print(decisions)

    for a in decisions:
        for b in decisions[a]:
            b.printMe()
    judgeDecisions(decisions['Patterns/pattern_1.txt'])
