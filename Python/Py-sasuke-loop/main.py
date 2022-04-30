import random
from BinanceMaster.BinanceMaster import *
from GraphHandler.graphHandler import *
import time
import matplotlib.pyplot as plt

#TODO: check future price custom based on the current patterns
#GLOBALS
decisions = None
tik_tok = 0.1 #clock intervals
time_check_old_decisions = 20

global_fake_api_next = []
last_used = 0
test_location = 'LastWeek5.csv'

#temp declarations
fake_current_time_stamp = 111  #magic number bcs you need offset

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
    # test_location = 'LastWeek5.csv'
    raw_data = readDataFromExcelFile('LastWeeks/'+test_location)

    add_time_stamp = []
    for index, a in enumerate(raw_data):
        add_time_stamp.append([a,index])

    # print("last x:",last_x)
    # print("fake_current_time_stamp:",fake_current_time_stamp)
    # print("from:",fake_current_time_stamp-last_x)
    # print("to:",fake_current_time_stamp)

    temp_state = add_time_stamp[fake_current_time_stamp-last_x:fake_current_time_stamp ]
    # print("temp_state:",temp_state)

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

    print("Entry point graph handler")
    print("[1].Raw data:\n",points)
    print("len raw data:", len(points))

    # plotArr(points, 'data')
    graph = graphData()

    vector = points #wtf man

    #PLOT RAW DATA
    plotArr(points,'ceva')
    graph.setInputData(vector)

    graph.inputToCandle(candleSize=candleSize)
    # print("input to candle:",len(graph.candlesData))

    print("[2].Input to candle:\n", graph.candlesData)
    #PLOT INPUT TO CANDLE
    # for a in graph.candlesData:
    #     plt.bar(a[0],a[1],0.5,a[2],color=a[3])

    # plt.show()

    graph.filterCandles(filter_candles_1, filter_candles_2)
    # print("input to candle filtered:",len(graph.candlesData))
    #PLOT FILTERED CANDLES
    # plt.title('altceva')
    for a in graph.candlesData:
        plt.bar(a[0], a[1], 0.5, a[2], color=a[3])
    print("[3].Filtered candles:\n",graph.candlesData)

    graph.candlesToFunctionWork(candleSize)
    # plotArr(graph.candlesToFunction,'ceva')
    # plt.show()

    # candlesToFct_y = [a[1] for a in graph.candlesToFunction]
    # plotArr(candlesToFct_y, 'ceva')

    print("[4].Candles to function:\n",graph.candlesToFunction)
    # for a in enumerate(graph.candlesToFunction):
    #     if a[0] !=1:
    #         a[0] +=1

    graph.generateInternPoints()

    # candlesToFct_y = [a[1] for a in graph.candlesToFunction]
    # plotArr(candlesToFct_y, 'ceva')

    print("[5].Generate intern points:\n", graph.candlesToFunction)

    #FINAL DATA IN graph.candlesToFunction
    # for a in graph.candlesToFunction:
    #     print(a)

    # print("intern:")
    # print("one:",len(graph.inputData))
    # print("three:",len(graph.candlesToFunction))

    just_y = []
    for a in graph.candlesToFunction:
        just_y.append(a[1])

    plotArr(just_y,'ceva')
    plt.show()

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
            # print("p:",split_point[1])
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

def completeOldDecisions(currentStockPrice,currentTime):
    #TODO: function to fetch the current stock price
    # currentStockPrice = None

    for a in decisions:
        for index,b in enumerate(decisions[a]):
            # curentTimeStamp = round(time.time() * 1000)
            curentTimeStamp = currentTime

            if b.getEndDate() == None and curentTimeStamp - b.getStartDate() > time_check_old_decisions :
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

def judgeDecisions(decisionsParam):
    total = len(decisionsParam)
    success = 0
    for a in decisionsParam:
        if a.priceDiff() > 0:
            success +=1
    print("Judge Decisions:",decisionsParam)
    print("Total:",total)
    print("Success:",success)
    if total and success:
        print("Ratio:",(success*100)/total)

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
        if self.end_price is not None and self.start_price is not None:
            return self.end_price - self.start_price
        else:
            return -1
    def printMe(self):
        print(self.start_price,self.end_price,self.start_date,self.end_date)

def testFunction():
    raw_data = readDataFromExcelFile('LastWeeks/'+'LastWeek5.csv')
    print("raw data len:",len(raw_data))
    del raw_data[0]

    for index,a in enumerate(raw_data):
        print(index,a)

    # print("before del:",raw_data[-1])
    # del raw_data[-1]
    # raw_data.insert(0,42873)
    # print("after:",raw_data[-1])

    terr_raw_data = integratedNarutoMain(raw_data,2,0.3,0.5)

    print("terraFormed:")
    for a in terr_raw_data:
        print(a)

    plotArr(raw_data[0:200],'test')
    plotArr(terr_raw_data[0:200],'test')
    plt.show()

if __name__ == '__main__':
    # testFunction()
    #------initializare patterns------
    referinteTerraForm = [
        # {
        #     "fileName": "Patterns/pattern_55.txt",
        #     "size_seg_unic": 25,
        #     "candle_size": 2,
        #     "filter_1": 0.3,
        #     "filter_2": 0.5,
        #     "abatere_hard": 5000
        # },
        # {
        #     "fileName": "Patterns/pattern_6.txt",
        #     "size_seg_unic": 25,
        #     "candle_size": 2,
        #     "filter_1": 0.3,
        #     "filter_2": 0.5,
        #     "abatere_hard": 4000
        # },
        # {
        #     "fileName": "Patterns/pattern_65.txt",
        #     "size_seg_unic": 30,
        #     "candle_size": 2,
        #     "filter_1": 0.3,
        #     "filter_2": 0.5,
        #     "abatere_hard": 5000
        # },
        {
            "fileName": "Patterns/pattern_7.txt",
            "size_seg_unic": 30,
            "candle_size": 1,
            "filter_1": 0.3,
            "filter_2": 0.5,
            "abatere_hard": 500
        },
        # {
        #     "fileName": "Patterns/pattern_8.txt",
        #     "size_seg_unic": 25,
        #     "candle_size": 1,
        #     "filter_1": 0.3,
        #     "filter_2": 0.5,
        #     "abatere_hard": 1000
        # },
        # {
        #     "fileName": "Patterns/pattern_9.txt",
        #     "size_seg_unic": 25,
        #     "candle_size": 1,
        #     "filter_1": 0.3,
        #     "filter_2": 0.5,
        #     "abatere_hard": 200
        # },
    ]
    patterns = []
    for a in referinteTerraForm:
        patterns.append(terraFormPatterns(a["fileName"],a["size_seg_unic"],a["candle_size"],a["filter_1"],a["filter_2"],a["abatere_hard"]))
    decisions = initFormatDecisions(referinteTerraForm)
    # printFinalPattern(patterns)
    # print("len main:",len(patterns[0]["values"]))

    #------initializare Binance------ // not used yet // first pass old values iterator test
    # test = BiananceMaster()


    # print("check patterns:")
    # for a in patterns:
    #     for b in a["values"]:
    #         print(b)

    clock_time = 3
    while True:
        #clock area--------------
        clock_time += 1

        # print("time stamp:",fake_current_time_stamp)
        fake_current_time_stamp += 2
        if fake_current_time_stamp > 7000:
            break

        last_100_min = fakeApi(70)   #just_y

        #cu offset
        # last_100_min = [38991.11, 38969.7, 38978.67, 38998.08, 39000.57, 39013.83, 38991.98, 39007.43, 39015.68, 39016.62, 39009.29, 39016.84, 39016.1, 39008.17, 38996.75, 38973.26, 38996.36, 39012.07, 39043.11, 39055.01, 39054.44, 39050.87, 39050.09, 39060.59, 39085.52, 39097.88, 39076.16, 39092.67, 39080.77, 39100.0, 39097.75, 39059.1, 39045.0, 39041.93, 39012.35, 39018.75, 39025.4, 39058.71, 39017.98, 39015.06, 39027.67, 39049.01, 39041.9, 39036.99, 39052.55, 39032.8, 39014.96, 39029.86, 39025.47, 39076.96, 39113.7, 39108.11, 39094.62, 39108.26, 39103.33, 39103.69, 39070.01, 39069.08, 39083.67, 39097.58, 39044.72, 39092.96, 39081.2, 39075.27, 39058.98, 39066.43, 39059.25, 39035.74, 39050.15, 39054.73, 39047.76, 39029.99, 39035.03, 39010.03, 38953.0, 39004.2, 39000.01, 39029.57, 39065.4, 39050.67, 39055.91, 39077.46, 39092.23, 39070.47, 39050.02, 39030.98, 39031.13, 39063.29, 39025.26, 39000.01, 39023.69, 39013.92, 39005.45, 39152.21, 39181.15, 39217.55, 39233.44, 39217.0, 39210.72, 39228.08]


        #fara offset
        # last_100_min = [38938.75, 38935.04, 38991.11, 38969.7, 38978.67, 38998.08, 39000.57, 39013.83, 38991.98, 39007.43, 39015.68, 39016.62, 39009.29, 39016.84, 39016.1, 39008.17, 38996.75, 38973.26, 38996.36, 39012.07, 39043.11, 39055.01, 39054.44, 39050.87, 39050.09, 39060.59, 39085.52, 39097.88, 39076.16, 39092.67, 39080.77, 39100.0, 39097.75, 39059.1, 39045.0, 39041.93, 39012.35, 39018.75, 39025.4, 39058.71, 39017.98, 39015.06, 39027.67, 39049.01, 39041.9, 39036.99, 39052.55, 39032.8, 39014.96, 39029.86, 39025.47, 39076.96, 39113.7, 39108.11, 39094.62, 39108.26, 39103.33, 39103.69, 39070.01, 39069.08, 39083.67, 39097.58, 39044.72, 39092.96, 39081.2, 39075.27, 39058.98, 39066.43, 39059.25, 39035.74, 39050.15, 39054.73, 39047.76, 39029.99, 39035.03, 39010.03, 38953.0, 39004.2, 39000.01, 39029.57, 39065.4, 39050.67, 39055.91, 39077.46, 39092.23, 39070.47, 39050.02, 39030.98, 39031.13, 39063.29, 39025.26, 39000.01, 39023.69, 39013.92, 39005.45, 39152.21, 39181.15, 39217.55, 39233.44, 39217.0]

        # temp_last_x  = last_100_min[0:29]
        offset = 10
        # completeOldDecisions(last_100_min[len(last_100_min)-1-offset],fake_current_time_stamp-offset)

        for index, a in enumerate(patterns):
            candle_size = float(a["pytonTerraForm"]["candle_size"])
            filter_1 = float(a["pytonTerraForm"]["filter_1"])
            filter_2 = float(a["pytonTerraForm"]["filter_2"])

            # print("emtry point naruto:")
            # print("len:",len(last_100_min))
            # print(candle_size,filter_1,filter_2)
            # print(last_100_min)


            last_100_min_terraFormed = integratedNarutoMain(last_100_min,candle_size,filter_1,filter_2)
            # print("out:",last_100_min_terraFormed)
            # print("len out:", len(last_100_min_terraFormed))

            # plotArr(last_100_min, index)
            # plotArr(last_100_min_terraFormed, index)

            # print("last 100 terra")
            # for index, b in enumerate(last_100_min_terraFormed):
            #     print(index,b)
            # print("last 100 terrra:",last_100_min_terraFormed)

            size = a["size"]
            # offset =
            start_index = len(last_100_min_terraFormed)-size-offset-1
            end_index = start_index + size + 1

            # last_x_points = last_100_min_terraFormed[0:a["size"]] #x custom based on pattern specification

            last_x_points = last_100_min_terraFormed[start_index:end_index]

            # add_fake_zeros = [39000 for a in range(0,start_index)] + last_x_points


            # plotArr(add_fake_zeros,index)

            # plotArr(last_x_points, index)
            # plt.show()

            # print("a 0 len:",len(a["values"][0]))
            # print("last x len:",len(last_x_points))

            # print("last x points:", last_x_points)

            min_cross_cor = crossCorelation(a["values"][0], last_x_points)

            which_one_pattern_var = None
            for index_b,b in enumerate(a["values"]):

                if crossCorelation(b, last_x_points) < min_cross_cor:
                    min_cross_cor = crossCorelation(b, last_x_points)
                    which_one_pattern_var = b

            # print("min cross", min_cross_cor)

            if min_cross_cor < a["pytonTerraForm"]["abatere_hard"]:
                # print('patt found')
                entitate_decizie = EntityDecizie(
                    # round(time.time() * 1000),
                    fake_current_time_stamp,
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


    for a in referinteTerraForm:
        judgeDecisions(decisions[a["fileName"]])

    # judgeDecisions(decisions['Patterns/pattern_1.txt'])
    # judgeDecisions(decisions['Patterns/pattern_1.txt'])
