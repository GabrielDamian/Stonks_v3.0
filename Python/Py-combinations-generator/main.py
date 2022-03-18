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
    candles_size = [round(i,2) for i in range(1,6,1)]
    size_seg_unic = [round(i,2) for i in range(50,160,10)]

    filter_1 = generateRange(0.1,1.0,0.3)
    filter_2 = generateRange(0.1,0.9,0.4)
    future_price = [5,10,20]

    min_max_streching = [round(i,2) for i in range(1,10,3)]
    abatere = [round(i,2) for i in range(1000,11000,1000)]


    #VARS TEST:----------------
    abatere_hard = [round(i,2) for i in range(1000,11000,1000)]
    succes_ratio = generateRange(0.6,1,0.1)
    how_many_represent_10_percentage = [25,15,10,5,3,1]

    #FORMAT MAIN:
    #  a[0] candles_size /
    #  a[1] size_seg_unic /
    #  a[2] filter_1 /
    #  a[3] filter_2 /
    #  a[4] future_price /
    #  a[5] min_max_streching /
    #  a[6] abatere

    #FORMAT TEST:
    #  abatere_hard /
    #  succes_ratio / 
    #  how_many_represent_10_percetange /

    print("candles_size", candles_size)
    print("size_seg_unic", size_seg_unic)
    print("filter_1", filter_1)
    print("filter_2", filter_2)
    print("future_price", future_price)
    print("min_max_streching", min_max_streching)
    print("abatere", abatere)

    print("succes_ratio", succes_ratio, len(succes_ratio))
    print("how_many_represent_10_percentage", how_many_represent_10_percentage, len(how_many_represent_10_percentage))

    main_combinations = ''
    test_combination = ''

    contor_main = 0
    for a in candles_size:
        for b in size_seg_unic:
            for c in filter_1:
                for d in filter_2:
                    for e in future_price:
                        for f in min_max_streching:
                            for g in abatere:
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

    contor_test = 0
    for a in abatere_hard:
        for b in succes_ratio:
            for c in how_many_represent_10_percentage:
                comb_str = ''
                comb_str += str(a) + "/"
                comb_str += str(b) + "/"
                comb_str += str(c) + "/"
                test_combination += comb_str + '\n'
                contor_test += 1

    # print("main contor:", contor_main)
    # printFirsts(main_combinations,1000)
    #
    # print("test comb len:", contor_test);
    # printFirsts(test_combination,1000)

    what_to_export = 0
    #0 = main combination
    #1 = test combination

    if what_to_export == 0:
        f = open("main_combination.txt", "w")
        f.write(main_combinations)
        f.close()
    else:
        f = open("test_combination.txt", "w")
        f.write(test_combination)
        f.close()

