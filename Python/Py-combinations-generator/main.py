import math
def generateRange(start, end, incrementor):
    arr = []
    iterator = start
    while iterator <= end:
        arr.append(round(iterator,2))
        iterator += incrementor
    return arr

def printFirsts(who, how_many):
    split = who.split('\n')
    index = 0
    print("len here:", len(split))
    while index < how_many and index < len(split):
        print(split[index])
        index += 1

if __name__ == '__main__':

    #VARS:----------------
    candles_size = [2,1,3]
    # size_seg_unic = [40, 50, 60, 70, 80, 100, 120, 140]
    size_seg_unic = [25,30,35]


    filter_1 = [0.3]
    filter_2 = [0.5]
    future_price = [10,20]

    min_max_streching = [0,4,7]
    # abatere = [round(i,2) for i in range(1000,11000,1000)]
    # abatere.insert(0,500)

    #FORMAT MAIN:
    #  a[0] candles_size /
    #  a[1] size_seg_unic /
    #  a[2] filter_1 /
    #  a[3] filter_2 /
    #  a[4] future_price /
    #  a[5] min_max_streching /
    #  a[6] abatere

    print("candles_size", candles_size)
    print("size_seg_unic", size_seg_unic)
    print("filter_1", filter_1)
    print("filter_2", filter_2)
    print("future_price", future_price)
    print("min_max_streching", min_max_streching)
    # print("abatere", abatere)


    main_combinations = ''

    contor_main = 0
    for a in candles_size:
        for b in size_seg_unic:
            for c in filter_1:
                for d in filter_2:
                    for e in future_price:
                        for f in min_max_streching:
                            buffer_bidirectional = 20
                            # print("b=",b)
                            min_abatere = (b - buffer_bidirectional) * 100
                            max_abatere =  (b + buffer_bidirectional) * 100
                            vector_abatere = [x for x in range(min_abatere,max_abatere,1000)]
                            # print("size_seg_unic:",b)
                            # print("abateri:", vector_abatere)
                            for g in vector_abatere:
                                comb_str = ''
                                comb_str +=str(a) +"/"
                                comb_str +=str(b) +"/"
                                comb_str +=str(c) +"/"
                                comb_str +=str(d) +"/"
                                comb_str +=str(e) +"/"
                                comb_str +=str(f) +"/"
                                comb_str +=str(g) +"/"
                                main_combinations += comb_str +'\n'
                                contor_main += 1


    f = open("main_combination.txt", "w")
    f.write(main_combinations)
    f.close()

