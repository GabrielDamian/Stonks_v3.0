# from plot import *
import matplotlib.pyplot as plt

if __name__ == '__main__':

    var1 = [119.26, 112.26, 121.62, 130.99, 140.35, 149.71, 159.08, 168.44, 177.80, 187.17, 196.53, 205.89, 215.26, 224.62, 215.98, 207.34, 198.70, 190.06, 181.42, 172.78, 164.15, 155.51, 146.87, 138.23, 129.59, 120.95, 112.31, 103.67, 95.03, 86.39, 77.75, 69.11, 60.47, 51.84, 43.20, 34.56, 25.92, 17.28, 8.64, 0.00,
]
    var2 = [142.20, 151.65, 161.11, 170.56, 180.01, 189.46, 198.92, 208.37, 217.83, 227.28, 236.74, 246.19, 255.64, 265.09, 274.55, 278.31, 266.15, 254.00, 241.84, 229.69, 217.53, 205.37, 193.22, 181.06, 168.91, 156.75, 144.60, 132.44, 120.28, 108.13, 95.97, 83.82, 71.66, 59.50, 47.34, 35.19, 23.03, 10.88, 1.59, 16.67,
]
    var3 = [233.82, 247.15, 260.48, 273.81, 287.14, 300.48, 313.82, 327.15, 340.48, 353.82, 367.15, 380.48, 393.81, 407.14, 411.07, 394.59, 378.11, 361.64, 345.16, 328.68, 312.20, 295.73, 279.24, 262.77, 246.29, 229.82, 213.34, 196.86, 180.39, 163.91, 147.43, 130.95, 114.47, 98.00, 81.52, 65.04, 48.56, 32.09, 15.61, 0.95,
]
    print(len(var1))
########################
#
#     varA1 = [13.68, 20.13, 26.57, 33.02, 39.46, 45.91, 41.32, 36.73, 32.14, 27.55, 22.95, 18.36, 13.77, 9.18, 4.59, 0.00
# ]
#
#     varA2 = [20.13, 26.57, 33.02, 39.46, 45.91, 41.32, 36.73, 32.14, 27.55, 22.95, 18.36, 13.77, 9.18, 4.59, 0.00, 4.17,
# ]
#
#     varA3 = [26.57, 33.02, 39.46, 45.91, 41.32, 36.73, 32.14, 27.55, 22.95, 18.36, 13.77, 9.18, 4.59, 0.00, 4.17, 8.33,
# ]
########################
    # varB1 = [0.00, 4.60, 9.19, 13.78, 18.38, 22.97, 27.57, 32.16, 36.75, 41.35, 45.94, 50.54, 55.13, 59.73, 64.32, 68.92, 73.51, 78.10, 82.70, 83.58,]

    # varB2 = [174.30, 157.97, 141.63, 125.28, 108.94, 92.60, 76.26, 59.92, 43.58, 27.24, 10.90, 5.52, 22.06, 38.61, 55.16, 71.71, 88.25, 104.80, 107.53, 103.35]
    #
    # varB3 = [152.52, 136.18, 119.84, 103.49, 87.15, 70.81, 54.47, 38.13, 21.79, 5.45, 11.03, 27.58, 44.12, 60.67, 77.22, 93.77, 110.31, 106.13, 101.96, 97.77]

    plt.figure('var1')
    plt.plot(var1)

    plt.figure('var2')
    plt.plot(var2)

    plt.figure('var3')
    plt.plot(var3)

    #######################
    # plt.figure('varA1')
    # plt.plot(varA1)
    #
    # plt.figure('varA2')
    # plt.plot(varA2)
    #
    # plt.figure('varA3')
    # plt.plot(varA3)

    ######################
    # plt.figure('varB1')
    # plt.plot(varB1)

    # plt.figure('varB2')
    # plt.plot(varB2)
    #
    # plt.figure('varB3')
    # plt.plot(varB3)


    plt.show()
