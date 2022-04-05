import time
import random

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


def terraFormPatterns(referinteTerraForm):
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
    obj["size"] = 40
    obj["source"] = referinteTerraForm
    obj["pytonTerraForm"] = {}
    obj["pytonTerraForm"]["candle_size"] = 2
    obj["pytonTerraForm"]["filter_1"] = 0.3
    obj["pytonTerraForm"]["filter_2"] = 0.5

    return obj

def fakeApi():
    return round(random.random()*100,2)

if __name__ == '__main__':
    referinteTerraForm = [
        "pattern_1.txt",
        "pattern_2.txt",
        "pattern_3.txt"
    ]
    final_patterns = []
    for a in referinteTerraForm:
        final_patterns.append(terraFormPatterns(a))

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
        time.sleep(5)
        #TODO:
        #fetch api
        new_fetch_value = fakeApi()
        global_buffer.append(new_fetch_value)
        print("global_buffer update:", global_buffer)

        #iterate final_patterns and generate new custom buffer based on candleSize, filter_1, filter_2
        #iterate patterns and basez on abatere_hard, decide if add a new decision for that specific pattern group

        #iterate old decision and decide ih 10min have passsed and close the decision or not


