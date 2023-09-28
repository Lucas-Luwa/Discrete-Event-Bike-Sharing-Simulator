import random
import numpy as np
import time
import dataStorage
from collections import deque
import queue

stationCount = 81
stationBikes = 100
totalRiders = 3500
lambdaSymbol = 2.38
avgTime = 2.78
stdTime = 0.619
stallTime = 0.0
numStalled = 0
arrived = 0
lowestRecorded = 100
probStations = dataStorage.probStations
probDestinations = dataStorage.probDestinations

currBikes = np.ones((stationCount,)) * stationBikes
lowestBikes = np.ones((stationCount,)) * stationBikes
stationQueues = [deque() for _ in range(stationCount)]
# print(currBikes)

initArrival = deque()
currtime = 0
i = 0
while i < totalRiders:
    interarrival = np.random.exponential(1/lambdaSymbol)
    stationIndex = np.random.choice(range(stationCount), p=probStations)
    initArrival.append((currtime + interarrival, stationIndex)) 
    currtime += interarrival
    i += 1

currHavingFun = deque()
def sortingHelper(input):
    return input[0]

def processor(input, isBorrowing):
    global currHavingFun
    global numStalled
    global arrived, lowestRecorded
    if (isBorrowing and currBikes[input[1]] > 0):
        # print("hi")
        # print(currBikes[input[1]])
        currBikes[input[1]] -= 1
        if (currBikes[input[1]] < lowestBikes[input[1]]):
            lowestBikes[input[1]] = currBikes[input[1]]
        timeWithBike = np.random.lognormal(avgTime, stdTime)
        # print(timeWithBike)
        destinationIndex = np.random.choice(range(stationCount + 1), p = probDestinations[input[1]])
        # print(destinationIndex)
        if (destinationIndex != 81):
            currHavingFun.append((input[0] + timeWithBike, destinationIndex))
            currHavingFun = queue.deque(sorted(currHavingFun))
    elif (isBorrowing and currBikes[input[1]] == 0):
        destinationIndex = np.random.choice(range(stationCount + 1), p = probDestinations[input[1]])
        if (destinationIndex != 81):
            numStalled +=1
            stationQueues[input[1]].append((input[0], destinationIndex))
            # stationQueues[input[1]] = queue.deque(sorted(stationQueues[input[1]]))
            sorted(stationQueues[input[1]])
        else:
            arrived +=1
    elif not isBorrowing:
        arrived +=1
        currBikes[input[1]] +=1
        if len(stationQueues[input[1]]) > 0:
            stalledPerson = stationQueues[input[1]].popleft()
            global stallTime
            stallTime += input[0] - stalledPerson[0]
            currBikes[input[1]] -= 1
            timeWithBike = np.random.lognormal(avgTime, stdTime)
            currHavingFun.append((input[0] + timeWithBike, input[1])) #We've figured out the destinationIndex in the second case. 
            currHavingFun = queue.deque(sorted(currHavingFun))
k = 0;
# print(initArrival)
# print(len(currHavingFun))
j = 0
while True:
    if (k % 1000 == 0):
        # print("arfibed " + str(arrived))
        temp = 0;
        for i in range(stationCount):
            temp += len(stationQueues[i])
        # print(temp)

    if (len(currHavingFun) == 0 and len(initArrival) == 0):
        break
    elif (len(currHavingFun) == 0):
        k+=1

        borrowingBike = initArrival.popleft()
        if borrowingBike[0] > 1440: 
            break
        processor(borrowingBike, True)
    elif (len(initArrival) == 0):
        k+=1
        returningBike = currHavingFun.popleft()
        if returningBike[0] > 1440:

            break
        processor(returningBike, False)
    else:
        k+=1
        currRiding = currHavingFun.popleft()
        currArrival = initArrival.popleft()
        if currRiding <= currArrival:
            if currRiding[0] > 1440:
                break
            initArrival.appendleft(currArrival)
            processor(currRiding, False)
        else:
            if currArrival[0] > 1440:

                break
            currHavingFun.appendleft(currRiding)
            processor(currArrival, True)
    j+=1
# print("finarfibed " + str(arrived))
# print(len(initArrival))
# print("end of program")
neverGotBike = 0
for i in range(stationCount):
    lowestBikes[i] = 100 - lowestBikes[i]
    # print(stationQueues[i])
    neverGotBike += len(stationQueues[i])
# print("Bikes needed: " + str(100-lowestRecorded))
# print(lowestBikes)
print("Bikes needed: " + str(max(lowestBikes)))

