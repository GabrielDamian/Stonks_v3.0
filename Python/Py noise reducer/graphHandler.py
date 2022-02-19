import matplotlib.pyplot as plt
import csv

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

    def plotInputData(self,code):
        plt.figure(code)
        plt.plot(self.inputData)

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

                    newCandle = [xIndex, height ,yValue,direction]

                    candles.append(newCandle)
                    #reseteaza contoare pt next candle
                    startPrice = stopPrice
                    stopPrice = None
                    triggerNewCandle = 0
                triggerNewCandle +=1
                xIndex +=1

                #conditie care previne eroare la startPrice = self.inputData[xIndex + 1]// index arr out of bounds
                if xIndex > len(self.inputData) - candleSize:
                    break
            self.candlesData = candles

    def plotCandles(self,code):
        plt.figure(code)
        if self.candlesData == None:
            print("candlesData not generated yet")
        else:
            width =2
            for x in self.candlesData:
                plt.bar(x[0],x[1],width,x[2],color=x[3],align='center')

    def filterCandles(self,factor,factor_2):
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
                            changeColor = True

                    #suplimentar, factor vecin prea mare
                    # factor_vecin_prea_mare = 4
                    # # if x[1] * factor_vecin_prea_mare <= self.candlesData[index - 1][1] or x[1] * factor_vecin_prea_mare <= self.candlesData[index + 1][1]:
                    # #     changeColor = False
                    # #
                    # filtru_candles_extrem_de_mici = 10
                    # if x[1] < filtru_candles_extrem_de_mici:
                    #     pass
                    # else:
                    #     if x[1] * factor_vecin_prea_mare <= self.candlesData[index - 1][1] or x[1] * factor_vecin_prea_mare <= self.candlesData[index + 1][1]:
                    #         changeColor = False

                    if changeColor == True:
                        counter_schimbari += 1
                        candles_to_remove.append(index)
                        if x[3] == 'red':

                            self.candlesData[index][3] = 'green'
                        else :
                            self.candlesData[index][3] = 'red'


    def candlesToFunctionWork(self,candleSize):
        #foloseste data din candlesData
        #data din candlesData trebuie filtrata inainte  daca vr sa il folosim ca input in candles to function

        #metoda are ca output data din points
        size = len(self.candlesData)
        index = 0
        points = []


        while index < size - 1:
            if self.candlesData[index][3] != self.candlesData[index + 1][3]:

                if self.candlesData[index][3] == 'red':
                    # [x, height, bottom, direction]
                    x_B = self.candlesData[index][0]+candleSize
                    y_B = self.candlesData[index][2]

                    x_A = x_B - candleSize
                    y_A = self.candlesData[index][2] + self.candlesData[index][1]
                    points.append([x_A,y_A])
                    points.append([x_B,y_B])
                else:
                    x_B = self.candlesData[index][0]
                    y_B = self.candlesData[index][2] + self.candlesData[index][1]

                    x_A = x_B - candleSize
                    y_A = self.candlesData[index][2]

                    points.append([x_A, y_A])
                    points.append([x_B, y_B])

                index += 1
            else:
                temp_index = index + 1
                while self.candlesData[temp_index][3] == self.candlesData[temp_index + 1][3] and temp_index < size - 2:
                    temp_index += 1

                # [x, height, bottom, direction]

                if self.candlesData[index][3] == 'red':
                    x_A = self.candlesData[index][0]
                    y_A = self.candlesData[index][2] + self.candlesData[index][1]

                    x_B = self.candlesData[temp_index][0]
                    y_B = self.candlesData[temp_index][2]

                    points.append([x_A, y_A])
                    points.append([x_B, y_B])

                else:
                    x_A = self.candlesData[index][0]
                    y_A = self.candlesData[index][2]

                    x_B = self.candlesData[temp_index][0]
                    y_B = self.candlesData[temp_index][2] + self.candlesData[temp_index][1]

                    points.append([x_A, y_A])
                    points.append([x_B, y_B])


                index = temp_index + 1


        self.candlesToFunction = points


    def plotCandlesToFunction(self,code):
        plt.figure(code)
        arr_1 = []
        arr_2 = []
        for a in self.candlesToFunction:
            arr_1.append(a[0])
            arr_2.append(a[1])
#upsss
        # plt.plot(arr_1,arr_2,'r')
        # plt.plot(self.inputData,'b')

        index = 0
        while index < len(self.candlesToFunction)-1:
            plt.scatter(int(self.candlesToFunction[index][0]), int(self.candlesToFunction[index][1]))
            index +=1

    #util function
    def filter_oven_indexes(self):
        new_arr = []
        for index, x in enumerate(self.candlesToFunction):
            if index % 2 !=0 or index == 0:
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

