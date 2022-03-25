
def readFromFile(fileName):
    file1 = open(fileName, 'r')
    lines = file1.readlines()
    return lines

def compareStructs(a,b):
    if a["abatere_hard"] == b["abatere_hard"] and a["how_many_for_foam"] == b["how_many_for_foam"] and a[
        "candles_size"] == b["candles_size"] and a["size_seg_unic"] == b["size_seg_unic"] and a[
        "filter_1"] == b["filter_1"] and a["filter_2"] == b["filter_2"] and a[
        "future_price"] == b["future_price"] and a["min_max_streching"] == b["min_max_streching"] and a[
        "abatere"] == b["abatere"]:
        return True
    else:
        return False


def splitRow(rows):
    result = []
    for a in rows:
        splittedRow = a.split('/')
        obj = {}
        obj["succes_percent"] = int(splittedRow[0])
        obj["succes_buyes"] = int(splittedRow[1])
        obj["total_buyed"] = splittedRow[2]
        obj["abatere_hard"] = splittedRow[3]
        obj["how_many_for_foam"] = splittedRow[4]
        obj["candles_size"] = splittedRow[5]
        obj["size_seg_unic"] = splittedRow[6]
        obj["filter_1"] = splittedRow[7]
        obj["filter_2"] = splittedRow[8]
        obj["future_price"] = splittedRow[9]
        obj["min_max_streching"] = splittedRow[10]
        obj["abatere"] = splittedRow[11]
        obj["test_farm"] = splittedRow[13]

        result.append(obj)

    return result

def customPrint(arr):
    result = []
    for index_1,a in enumerate(arr):
        temp_struct = []

        for index_2,b in enumerate(arr):
            if compareStructs(a,b) and index_1 != index_2:

                temp_struct.append(a)
        result.append(temp_struct)

    return result

if __name__ == '__main__':
    data = readFromFile("apollo.txt")
    splitted = splitRow(data)

    filtered =[x for x in splitted if x["test_farm"][0:6] == "Test_3"]
    sorted = sorted(filtered, key=lambda x: x['succes_buyes'], reverse=False)

    for a in sorted:
        print(a)

    # customPrintData = customPrint(filtered)
    # for a in customPrintData[1]:
    #     print(a)


