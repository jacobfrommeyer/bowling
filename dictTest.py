
pinData = {}
pinData[1] = [37, 49, 37, 46]
pinData[2] = [43, 44, 83, 66]

for pinNum in pinData:
    print("Pin num: ", pinNum)
    for x in range(4):
        print(x)
        print("cord: ", pinData[pinNum][x])
