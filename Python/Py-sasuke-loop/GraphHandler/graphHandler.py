# import matplotlib.pyplot as plt
import csv
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


class graphData:

    inputData = None #y values, x is incremented by 1 min value in time
    candlesData = None #arr of arr [[x,height,bottom,direction],[],[]....]
    candlesToFunction = None

    def __init__(self):
        pass

    def setInputData(self,data):
        self.inputData = data

    def printInputData(self):
        print('Print input data:')
        print('len:', len(self.inputData))
        for a in self.inputData:
            print(a)

    # def plotInputData(self,code):
    #     plt.figure(code)
    #     plt.plot(self.inputData)

    def inputToCandle(self,candleSize):
        if self.inputData == None:
            print('Input data not generated yet (cannot use inputToCandle before that)')
        else:
            candles = []
            xIndex = 0
            triggerNewCandle = 0
            startPrice = self.inputData[0]
            stopPrice = None
            direction = None  # up or down

            for x in self.inputData:
                if triggerNewCandle == candleSize:
                    stopPrice = x
                    yValue = None
                    if startPrice <= stopPrice:
                        direction='green'
                        yValue = startPrice
                    else:
                        direction = 'red'
                        yValue = stopPrice

                    height = round(abs(startPrice-stopPrice),2)

                    #nu vr sa am candles cu height 0
                    if height  <= 1:
                        height = 1

                    #PLOTTTT

                    # plt.scatter(xIndex-1,yValue)
                    # print("y check:", yValue,direction)
                    #
                    newCandle = [xIndex, height ,yValue,direction]

                    candles.append(newCandle)
                    #reseteaza contoare pt next candle
                    startPrice = stopPrice
                    stopPrice = None
                    triggerNewCandle = 0
                triggerNewCandle +=1
                xIndex +=1

                #conditie care previne eroare la startPrice = self.inputData[xIndex + 1]// index arr out of bounds
                if xIndex > len(self.inputData):
                    break
            self.candlesData = candles

    # def plotCandles(self,code):
    #     plt.figure(code)
    #     if self.candlesData == None:
    #         print("candlesData not generated yet")
    #     else:
    #         width =2
    #         for x in self.candlesData:
    #             plt.bar(x[0],x[1],width,x[2],color=x[3],align='center')

    def filterCandles(self,factor,factor_2):

        filter_1_contor = 0
        filter_2_contor = 0
        #rezultat tot in candlesData

        #factor_1 = vecini stanga_dreapta (lipiti de candle curent)
        #factor_2 = cu 2 vecini la stanga si dreapta (factor 2 << factor 1)

        counter_schimbari = 0
        candles_to_remove = []

        if self.candlesData == None:
            print('input data not generated yet (cannot use filterCandles before that)')
        else:

            for index,x in enumerate(self.candlesData):
                changeColor = False
                if index ==0 or index == 1 or index == len(self.candlesData)-1 or index == len(self.candlesData)-2:
                    continue

                leftCandle = self.candlesData[index-1]
                rightCandle = self.candlesData[index+1]

                #daca vecinii directi au culori diferite
                if leftCandle[3] != x[3] and rightCandle[3] != x[3]:

                    #x[1] represents the size of the candle
                    leftValue = leftCandle[1]
                    rightValue = rightCandle[1]

                    #factor raportat la vecini (1 vecin stanga dreapta)
                    suma_vecini= leftValue + rightValue
                    #factor = 0.5 => x[1] < jumatate din suma vecinilor
                    #factor = 1 => x[1] < suma vecinilor

                    if x[1] < suma_vecini*factor:
                        changeColor = True
                        filter_1_contor +=1
                    else:
                        #daca vecinii imediati indica sa pastram aceeasi culoare, verifica 2 vecini la stanga si la dreapta

                        vecin_stanga_2 = self.candlesData[index-2]
                        vecin_stanga_1 = self.candlesData[index-1]
                        vecin_dreapta_1 = self.candlesData[index+1]
                        vecin_dreapta_2 = self.candlesData[index+2]

                        suma_vecini_aceeasi_culoare = 0
                        if x[3] != vecin_stanga_2[3]:
                            suma_vecini_aceeasi_culoare += vecin_stanga_2[1]
                        if x[3] != vecin_stanga_1[3]:
                            suma_vecini_aceeasi_culoare += vecin_stanga_1[1]
                        if x[3] != vecin_dreapta_1[3]:
                            suma_vecini_aceeasi_culoare += vecin_dreapta_1[1]
                        if x[3] != vecin_dreapta_2[3]:
                            suma_vecini_aceeasi_culoare += vecin_dreapta_2[1]

                        if x[1] < suma_vecini_aceeasi_culoare *factor_2:
                            filter_2_contor +=1
                            changeColor = True

                    # suplimentar, factor vecin prea mare
                    factor_vecin_prea_mare = 4
                    # if x[1] * factor_vecin_prea_mare <= self.candlesData[index - 1][1] or x[1] * factor_vecin_prea_mare <= self.candlesData[index + 1][1]:
                    #     changeColor = False
                    #
                    filtru_candles_extrem_de_mici = 10
                    if x[1] < filtru_candles_extrem_de_mici:
                        pass
                    else:
                        if x[1] * factor_vecin_prea_mare <= self.candlesData[index - 1][1] or x[1] * factor_vecin_prea_mare <= self.candlesData[index + 1][1]:
                            changeColor = False

                    if changeColor == True:
                        counter_schimbari += 1
                        candles_to_remove.append(index)
                        if x[3] == 'red':

                            self.candlesData[index][3] = 'green'
                        else :
                            self.candlesData[index][3] = 'red'

        
        # print("Contor 1:", filter_1_contor)
        # print("Contor 2:", filter_2_contor)

    def candlesToFunctionWork(self,candleSize):
        print("-----Entry point candlesToFunctionWork:")
        #foloseste data din candlesData
        #data din candlesData trebuie filtrata inainte  daca vr sa il folosim ca input in candles to function

        #metoda are ca output data din points
        size = len(self.candlesData)
        index = 0
        points = []
        print("size:",size)
        while index < size-1 :

            # print("index=",index)
            if self.candlesData[index][3] != self.candlesData[index + 1][3]:
                # print("case 1:")
                if self.candlesData[index][3] == 'red':
                    # print("case 1.1:")
                    # [x, height, bottom, direction]
                    x_B = self.candlesData[index][0]
                    y_B = self.candlesData[index][2]

                    x_A = x_B - candleSize
                    y_A = self.candlesData[index][2] + self.candlesData[index][1]
                    print("append:", [x_A,y_A],[x_B,y_B])
                    points.append([x_A,y_A])
                    points.append([x_B,y_B])
                else:
                    # print("case 1.2:")
                    x_B = self.candlesData[index][0]
                    y_B = self.candlesData[index][2] + self.candlesData[index][1]

                    x_A = x_B - candleSize
                    y_A = self.candlesData[index][2]

                    # print("append:", [x_A,y_A],[x_B,y_B])

                    points.append([x_A, y_A])
                    points.append([x_B, y_B])

                index += 1
                # print("index after:", index)


            else:
                # print("case 2")
                try:

                    temp_index = index + 1
                    #or self.candlesData[temp_index][2] == self.candlesData[temp_index + 1][2]
                    # print("TEST:",self.candlesData[temp_index][2],self.candlesData[temp_index+1][2])
                    while temp_index < size - 1 and self.candlesData[temp_index][3] == self.candlesData[temp_index + 1][3] :
                        temp_index += 1
                except:
                    print("EXCEPT!!!!!!!!!!:")
                    print("candlesData len:",len(self.candlesData))
                    print("temp_index:",temp_index)


                # [x, height, bottom, direction]

                if self.candlesData[index][3] == 'red':
                    # print("case 2.1:")
                    x_A = self.candlesData[index][0] - candleSize
                    y_A = self.candlesData[index][2] + self.candlesData[index][1]

                    x_B = self.candlesData[temp_index][0]
                    y_B = self.candlesData[temp_index][2]

                    # print("append:", [x_A, y_A], [x_B, y_B])
                    points.append([x_A, y_A])
                    points.append([x_B, y_B])

                else:
                    # print("case 2.2:")
                    x_A = self.candlesData[index][0]- candleSize
                    y_A = self.candlesData[index][2]

                    x_B = self.candlesData[temp_index][0]
                    y_B = self.candlesData[temp_index][2] + self.candlesData[temp_index][1]

                    # print("append:", [x_A, y_A], [x_B, y_B])
                    points.append([x_A, y_A])
                    points.append([x_B, y_B])


                index = temp_index + 1

            #here:
            # print("index out:", index)
            if index == size - 1:
                x_ultim = self.candlesData[index][0]
                y_ultim = self.candlesData[index][2]
                # print("ultim:", x_ultim, y_ultim)
                points.append([x_ultim, y_ultim])

        self.candlesToFunction = points

    #util function
    def filter_oven_indexes(self):
        new_arr = []
        for index, x in enumerate(self.candlesToFunction):
            if index % 2 != 0 or index == 0:
                new_arr.append(x)


        self.candlesToFunction =new_arr

    def generateInternPoints(self):
        self.filter_oven_indexes()

        index = 0
        puncte_noi = []
        while index < len(self.candlesToFunction)-1:
            start_point = self.candlesToFunction[index]
            end_point = self.candlesToFunction[index+1]

            start_x = start_point[0]+1
            end_x = end_point[0] -1

            x_1 = start_point[0]
            y_1 = start_point[1]

            x_2 = end_point[0]
            y_2 = end_point[1]

            if start_x == end_x:
                #trebui adaugat doar un singur punct

                x_nou = start_x #avem un singur puncte la mijloc de adaugat
                y_nou = (y_2 - y_1)*(x_nou - x_1)/(x_2 - x_1) + y_1

                puncte_noi.append([x_nou, y_nou])

            else:
                #trebuie adaugate >1 puncte
                temp_index = start_x
                while temp_index <= end_x:
                    x_nou = temp_index
                    y_nou = (y_2 - y_1)*(x_nou - x_1)/(x_2 - x_1) + y_1
                    puncte_noi.append([x_nou, y_nou])

                    temp_index +=1

            index +=1

        #add last point TEST:
        print("before naruto:",index,len(self.candlesToFunction)-1,self.candlesToFunction[index][0],self.candlesToFunction[index][1])
        if self.candlesToFunction[index][0] < len(self.candlesData):
            print("naruto true")
            print("expand:",self.candlesData[-1])
            print("add:",[self.candlesData[-1][0], self.candlesData[-1][2] + self.candlesData[-1][1]])
            if self.candlesData[-1][3] == 'green':
                puncte_noi.append([self.candlesData[-1][0], self.candlesData[-1][2] + self.candlesData[-1][1]])
            else:
                puncte_noi.append([self.candlesData[-1][0], self.candlesData[-1][2]])

        final_list = self.candlesToFunction + puncte_noi
         #sorteaza dupa x
        final_list.sort(key=lambda x:x[0])
        self.candlesToFunction = [[round(x[0],2),round(x[1],2)] for x in final_list]
        #bug

    def printCandlesToFunction(self):
        print('Print candles to function:')
        print('len:', len(self.candlesToFunction))
        for a in self.candlesToFunction:
            print(a)

