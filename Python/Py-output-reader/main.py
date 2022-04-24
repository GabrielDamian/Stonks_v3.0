#succes 280 / 560 = 50%
#succes 124 / 223 = 55% //min_max strec = 0
#
import sys

def readFromFile(fileName):
    file1 = open(fileName, 'r')
    lines = file1.readlines()
    return lines

def compareStructs(a,b):
    if a["abatere_hard"] == b["abatere_hard"] and a["how_many_for_foam"] == b["how_many_for_foam"] and a[
        "succes_ratio_filter"] == b["succes_ratio_filter"] and a[
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
        obj["succes_ratio_filter"] = splittedRow[5]
        obj["candles_size"] = splittedRow[6]
        obj["size_seg_unic"] = splittedRow[7]
        obj["filter_1"] = splittedRow[8]
        obj["filter_2"] = splittedRow[9]
        obj["future_price"] = splittedRow[10]
        obj["min_max_streching"] = int(splittedRow[11])
        obj["abatere"] = splittedRow[12]
        obj["test_farm"] = splittedRow[14]

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

def giveMeSucces_score(values):
    # score = 0
    # for a in values:
    #     score += a["succes_percent"]
    # return score

    total_buyed_local = 0
    succes_buyes_local = 0

    for b in values:
        total_buyed_local += int(b["total_buyed"])
        succes_buyes_local += int(b["succes_buyes"])

    # print("ratio:", (100 * succes_buyes_local) / total_buyed_local)

    ratio =(100 * succes_buyes_local) / total_buyed_local
    return total_buyed_local

if __name__ == '__main__':
    succes_param = float(sys.argv[1])
    print("succes param:",int(succes_param))
    # succes_param = 70

    print("succes:", succes_param)

    data = readFromFile("apollo.txt")
    splitted = splitRow(data)

    grouped_by_params = []
    # {
    #     "occ_index": [],
    #     "values":[]
    # }
    used_indexes = []
    for index_a,a in enumerate(splitted):
        print("index:",index_a,"/",len(splitted))
        inserted = False
        for index_b, b in enumerate(grouped_by_params):
            if compareStructs(b["values"][0], a):
                # print("object before insertion:",grouped_by_params[index_b] )
                # print("index to insert:", index_a)
                # print("value to insert:", a)
                grouped_by_params[index_b]["values"].append(a)
                grouped_by_params[index_b]["occ_index"].append(index_a)
                inserted = True
                break
        if not inserted: #create a new struct and insert
            new_struct = {
                "occ_index": [],
                "values": [],
                "ceva":"da"
            }
            new_struct["occ_index"].append(index_a)
            new_struct["values"].append(a)

            grouped_by_params.append(new_struct)

    #filter 50%+ for all terraforms
    final_list = []
    for a in grouped_by_params:
        check = True
        for b in a["values"]:
            if b["succes_percent"] < succes_param or b["min_max_streching"] == 4 or b["min_max_streching"] == 7:
                check = False

        if check:
            final_list.append(a)

    #sort by best succes_percent result:

    final_list_sorted = newlist = sorted(final_list, key=lambda x: giveMeSucces_score(x["values"]), reverse=False)
    for a in final_list_sorted:
        total_buyed = 0
        succes_buyes = 0
        for b in a["values"]:
            total_buyed += int(b["total_buyed"])
            succes_buyes += int(b["succes_buyes"])

        print("ratio:",(100*succes_buyes) / total_buyed )

        print("---->New Group:")
        print("score:",giveMeSucces_score(a["values"]))
        print(a["occ_index"])
        for b in a["values"]:
            print(b)