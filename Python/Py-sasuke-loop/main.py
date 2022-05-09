import random
from BinanceMaster.BinanceMaster import *
from GraphHandler.graphHandler import *
import time
import matplotlib.pyplot as plt

# TODO: check future price custom based on the current patterns

#Change tp move on fakeTimeStamp:
#disable time.sleep(tik_tok)
#enable while break for 10k points
#get last_100_from from fakeApi
#change completeOldDecisions call
#change entitateDecison start_date
#change offset_to_ignore check
#
#

decisions = None
tik_tok = 5  #while clock, in second
time_check_old_decisions = 10 #minutes

offset_to_ignore_decisions = 20 #minutes

offset = 3 #indexes

global_fake_api_next = []
last_used = 0
test_location = 'LastWeek5.csv'

# temp declarations
fake_current_time_stamp = 111  # magic number bcs you need offset

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
    raw_data = readDataFromExcelFile('LastWeeks/' + test_location)

    add_time_stamp = []
    for index, a in enumerate(raw_data):
        add_time_stamp.append([a, index])

    # print("last x:",last_x)
    # print("fake_current_time_stamp:",fake_current_time_stamp)
    # print("from:",fake_current_time_stamp-last_x)
    # print("to:",fake_current_time_stamp)

    temp_state = add_time_stamp[fake_current_time_stamp - last_x:fake_current_time_stamp]
    # print("temp_state:",temp_state)

    just_y = []
    for a in temp_state:
        just_y.append(a[0])
    return just_y
def plotArr(arr, id):
    # arr, just y's
    plt.figure(id)
    plt.plot(arr)
# end of temp declarations

def integratedNarutoMain(points, candleSize, filter_candles_1, filter_candles_2):
    # print("Entry point graph handler")
    # print("[1].Raw data:\n",points)
    # print("len raw data:", len(points))

    # plotArr(points, 'data')
    graph = graphData()

    vector = points  # wtf man

    # PLOT RAW DATA
    # plotArr(points,'ceva')
    graph.setInputData(vector)

    graph.inputToCandle(candleSize=candleSize)
    # print("input to candle:",len(graph.candlesData))

    # print("[2].Input to candle:\n", graph.candlesData)
    # PLOT INPUT TO CANDLE
    # for a in graph.candlesData:
    #     plt.bar(a[0],a[1],0.5,a[2],color=a[3])

    # plt.show()

    graph.filterCandles(filter_candles_1, filter_candles_2)
    # print("input to candle filtered:",len(graph.candlesData))
    # PLOT FILTERED CANDLES
    # plt.title('altceva')
    # for a in graph.candlesData:
    #     plt.bar(a[0], a[1], 0.5, a[2], color=a[3])
    # print("[3].Filtered candles:\n",graph.candlesData)

    graph.candlesToFunctionWork(candleSize)
    # plotArr(graph.candlesToFunction,'ceva')
    # plt.show()

    # candlesToFct_y = [a[1] for a in graph.candlesToFunction]
    # plotArr(candlesToFct_y, 'ceva')

    # print("[4].Candles to function:\n",graph.candlesToFunction)
    # for a in enumerate(graph.candlesToFunction):
    #     if a[0] !=1:
    #         a[0] +=1

    graph.generateInternPoints()

    # candlesToFct_y = [a[1] for a in graph.candlesToFunction]
    # plotArr(candlesToFct_y, 'ceva')

    # print("[5].Generate intern points:\n", graph.candlesToFunction)

    # FINAL DATA IN graph.candlesToFunction
    # for a in graph.candlesToFunction:
    #     print(a)

    # print("intern:")
    # print("one:",len(graph.inputData))
    # print("three:",len(graph.candlesToFunction))

    just_y = []
    for a in graph.candlesToFunction:
        just_y.append(a[1])

    # plotArr(just_y,'ceva')
    # plt.show()

    return just_y

def readFromFile(fileName):
    file1 = open(fileName, 'r')
    lines = file1.readlines()
    patterns = []
    for a in lines:
        print("line:",a)
        pairs_str = a.split("/")
        del pairs_str[-1]
        single_pattern = []

        for b in pairs_str:
            split_point = b.split(",")
            print("split_point:",split_point)
            # print("p:",split_point[1])
            single_pattern.append(float(split_point[1]))
        patterns.append(single_pattern)
    return patterns

def terraFormPatterns(referinteTerraForm, size_seg_unic, candleSize, filter_1, filter_2, abatere_hard):
    # citeste pattern din fisier si adauga in structura template pentru patterns
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
        if (a["size"] < min):
            min = a["size"]
    return min

def initFormatDecisions(referinteTerraForm):
    final = {}
    for a in referinteTerraForm:
        final[a["fileName"]] = []
    return final

def crossCorelation(pattern, lastSnapTerraFormed):
    # yScallerEnaber and powerSum are default here

    # print("inside cros cor:")
    # print("patt:", pattern)
    # print("last_snap:", lastSnapTerraFormed)

    max_y_snap = max(lastSnapTerraFormed)
    max_y_patt = max(pattern)

    # print("max_y_snap:",max_y_snap)
    # print("max_y_base:",max_y_patt)
    # print("min spnap:",min(lastSnapTerraFormed))

    # test
    minus_min = [a - min(lastSnapTerraFormed) for a in lastSnapTerraFormed]

    y_ratio = max_y_patt / max(minus_min)
    test = [a * y_ratio for a in minus_min]

    # print("ratio:", y_ratio)

    # print("test:",test)

    # plotArr(test,'ceva')
    # plotArr(pattern,'ceva')
    # plt.show()

    suma_scaled = 0
    for index, a in enumerate(pattern):
        var = a - test[index] * y_ratio
        suma_scaled += var * var

    return suma_scaled

def completeOldDecisions(currentStockPrice, currentTime):

    for a in decisions:
        for index, b in enumerate(decisions[a]):

            # if b.getEndDate() == None and currentTime - b.getStartDate() > time_check_old_decisions * 60: #time_check_old_decisions is in minutes
            if b.getEndDate() == None and currentTime - b.getStartDate() > time_check_old_decisions: #test production mode
                print("decision completed")
                decisions[a][index].completeazaEndMomentum(currentTime, currentStockPrice)

def printFinalPattern(final_patterns):
    for a in final_patterns:
        print("\n\nNew pattern:---------")
        print("source:", a["source"])
        print("size:", a["size"])
        # print(a["pytonTerraForm"])
        for x in a["pytonTerraForm"]:
            print(x, ":", a["pytonTerraForm"][x])
        print("values:")
        for index, b in enumerate(a["values"]):
            if index < 5:
                print(b)

def judgeDecisions(decisionsParam):
    total = len(decisionsParam)
    success = 0
    for a in decisionsParam:
        if a.priceDiff() > 0:
            success += 1
    print("Judge Decisions:", decisionsParam)
    print("Total:", total)
    print("Success:", success)
    if total and success:
        print("Ratio:", (success * 100) / total)

class EntityDecizie:
    def __init__(self, startDate, startPrice, endDate, endPrice, whichPatt, minCross):
        self.start_date = startDate
        self.start_price = startPrice
        self.end_date = endDate
        self.end_price = endPrice
        self.which_one_pattern_var = whichPatt
        self.min_cross_cor = minCross

    def print(self):
        print("todo print patt")

    def completeazaEndMomentum(self, endDate, endPrice):
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
        print(self.start_price, self.end_price, self.start_date, self.end_date)

    def toFileFormat(self):
        string = ""
        # FORMAT"
        # YES or NO = end_price - start_price > 0
        # YES/start_price/end_price/start_date/end_date
        if self.end_price is not None and self.start_price is not None and self.end_price - self.start_price > 0:
            string += 'YES/'
        else:
            string += 'NO /'

        string += str(self.start_price) + '/'
        string += str(self.end_price) + '/'
        string += str(self.start_date) + '/'
        string += str(self.end_date) + '/'

        return string

    def areYouOk(self):
        if self.start_price is None or self.end_price is None:
            return None
        else:
            return self.end_price - self.start_price

def testFunction():
    raw_data = readDataFromExcelFile('LastWeeks/' + 'LastWeek5.csv')
    print("raw data:", raw_data)
    terr_raw_data = integratedNarutoMain(raw_data, 1, 0.3, 0.5)
    print("terra:", terr_raw_data)

    # plotArr(raw_data[0:200],'testFct')
    plotArr(terr_raw_data[0:200], 'testFct')
    plt.show()

def outputAtClock(newDecision, destination):
    with open(destination, "a") as myfile:
        myfile.write(newDecision.toFileFormat() +"\n")
    # function that write into file when patterns where generated / append each time

def parsePatternIntoFile(source, destination):
    # write pattern into file format, overwrite each time

    string = ""
    for a in source:
        string += "\n"
        string += a + "\n"
        string += "Ratio:" + str(round(extractRatioFromPattern(source[a]),2)) + "\n"
        string += "Total:" + str(len(source[a])) + "\n"

        for b in source[a]:
            string += b.toFileFormat() + "\n"

    with open(destination, 'w') as f:
        f.write(string)

def extractRatioFromPattern(sourceArr):
    total = 0
    good = 0
    for decision in sourceArr:
        if decision.areYouOk() is not None:
            total += 1
            if decision.areYouOk() > 0:
                good +=1

    if total == 0:
        return 0
    else:
        return (good*100)/total

if __name__ == '__main__':
    # testFunction()
    # ------initializare patterns------
    referinteTerraForm = [
        {
            "fileName": "Patterns/pattern_55.txt",
            "size_seg_unic": 25,
            "candle_size": 2,
            "filter_1": 0.3,
            "filter_2": 0.5,
            "abatere_hard": 5000
        },
        {
            "fileName": "Patterns/pattern_60.txt",
            "size_seg_unic": 25,
            "candle_size": 2,
            "filter_1": 0.3,
            "filter_2": 0.5,
            "abatere_hard": 4000
        },
        {
            "fileName": "Patterns/pattern_65.txt",
            "size_seg_unic": 30,
            "candle_size": 2,
            "filter_1": 0.3,
            "filter_2": 0.5,
            "abatere_hard": 5000
        },
        {
            "fileName": "Patterns/pattern_70.txt",
            "size_seg_unic": 30,
            "candle_size": 2,
            "filter_1": 0.3,
            "filter_2": 0.5,
            "abatere_hard": 500
            #future_price: 20 !!!!!
        },
        {
            "fileName": "Patterns/pattern_80.txt",
            "size_seg_unic": 25,
            "candle_size": 1,
            "filter_1": 0.3,
            "filter_2": 0.5,
            "abatere_hard": 1000
        }
    ]

    patterns = []
    for a in referinteTerraForm:
        print("A:",a)
        patterns.append(
            terraFormPatterns(a["fileName"], a["size_seg_unic"], a["candle_size"], a["filter_1"], a["filter_2"],
                              a["abatere_hard"]))
    decisions = initFormatDecisions(referinteTerraForm)

    binanceMasterNode = BiananceMaster()

    clock_time = 3
    while True:
        # time.sleep(tik_tok)
        print("clock:", clock_time)
        clock_time += 1

        fake_current_time_stamp += 1    #production test mode
        if fake_current_time_stamp > 10950:
            break

        parsePatternIntoFile(decisions, 'decisionsMars.txt')

        last_100_min = fakeApi(70)  # just_y #production test mode
        # last_100_min = binanceMasterNode.GetHistoricalData(1)
        print("last 100:",last_100_min)

        completeOldDecisions(last_100_min[-1], fake_current_time_stamp) #production test mode
        # completeOldDecisions(last_100_min[-1], time.time()) #(x,curent_time_in_second)

        for index, a in enumerate(patterns):
            candle_size = float(a["pytonTerraForm"]["candle_size"])
            filter_1 = float(a["pytonTerraForm"]["filter_1"])
            filter_2 = float(a["pytonTerraForm"]["filter_2"])

            last_100_min_terraFormed = integratedNarutoMain(last_100_min, candle_size, filter_1, filter_2)
            # print("last 100 min terra:", last_100_min_terraFormed)

            size = a["size"]
            start_index = len(last_100_min_terraFormed) - size - offset - 1
            end_index = start_index + size + 1

            # print("start:end->",start_index,end_index)

            last_x_points = last_100_min_terraFormed[start_index:end_index]
            # print("last x points:", last_x_points)

            min_cross_cor = crossCorelation(a["values"][0], last_x_points)

            which_one_pattern_var = None
            for index_b, b in enumerate(a["values"]):

                if crossCorelation(b, last_x_points) < min_cross_cor:
                    min_cross_cor = crossCorelation(b, last_x_points)
                    which_one_pattern_var = b

            if min_cross_cor < a["pytonTerraForm"]["abatere_hard"]:
                print("patt found")
                entitate_decizie = EntityDecizie(
                    # round(time.time()) - offset * 60, #offset is in minutes
                    fake_current_time_stamp - offset,
                    last_x_points[-1],
                    None,
                    None,
                    which_one_pattern_var,
                    min_cross_cor
                )
                if len(decisions[a["source"]]) > 0:
                    print("ignore new decision")
                    # if  entitate_decizie.getStartDate() - decisions[a["source"]][-1].getStartDate() < offset_to_ignore_decisions * 60: #offset_to_ignore are minutes
                    if  entitate_decizie.getStartDate() - decisions[a["source"]][-1].getStartDate() < offset_to_ignore_decisions: #test production mode
                        print("IGNORE")
                    else:
                        decisions[a["source"]].append(entitate_decizie)
                else:
                    decisions[a["source"]].append(entitate_decizie)
                    outputAtClock(entitate_decizie, "outputAtClock.txt")

    # print("decision:", len(decisions))
    # print(decisions)
    #
    # for a in decisions:
    #     for b in decisions[a]:
    #         b.printMe()
    #
    # # for a in referinteTerraForm:
    # #     judgeDecisions(decisions[a["fileName"]])
    # judgeDecisions(decisions['Patterns/pattern_65.txt'])