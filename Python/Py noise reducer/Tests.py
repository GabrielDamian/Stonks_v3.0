import matplotlib.pyplot as plt

def testRawInputData(data,cout=False, limit = 100):
    print("Raw size:",len(data))
    if cout:
        for index,a in enumerate(data):
            if index > limit:
                break
            print(a);


