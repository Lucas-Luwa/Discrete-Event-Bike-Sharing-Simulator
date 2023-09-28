import random
import numpy as np
import time
import dataStorage
from collections import deque
import queue

stationCount = 81
stationBikes = 10
totalRiders = 3500
lambdaSymbol = 2.38
avgTime = 2.78
stdTime = 0.619
stallTime = 0.0
probStations = dataStorage.probStations
probDestinations = dataStorage.probDestinations

currBikes = np.ones((stationCount,)) * stationBikes
stationQueues = [deque() for _ in range(stationCount)]

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
    if isBorrowing and currBikes[input[1]] > 0:
        currBikes[input[1]] -= 1
        timeWithBike = np.random.lognormal(avgTime, stdTime)
        destinationIndex = np.random.choice(range(stationCount + 1), p = probDestinations[input[1]])
        if (destinationIndex != 81):
            currHavingFun.append((input[0] + timeWithBike, destinationIndex))
            currHavingFun = queue.deque(sorted(currHavingFun))
    elif isBorrowing and currBikes[input[1]] == 0:
        destinationIndex = np.random.choice(range(stationCount + 1), p = probDestinations[input[1]])
        if (destinationIndex != 81):
            stationQueues[input[1]].append((input[0], destinationIndex))
            currHavingFun = queue.deque(sorted(stationQueues[input[1]]))
    else:
        currBikes[input[1]] +=1
        if len(stationQueues[input[1]]) > 0:
            stalledPerson = stationQueues[input[1]].popleft()
            global stallTime
            stallTime += input[0] - stalledPerson[0]
            currBikes[input[1]] -= 1
            timeWithBike = np.random.lognormal(avgTime, stdTime)
            currHavingFun.append((input[0] + timeWithBike, input[1])) #We've figured out the destinationIndex in the second case. 
            currHavingFun = queue.deque(sorted(currHavingFun))
while True:
    if (len(currHavingFun) == 0 and len(initArrival) == 0):
        break
    elif (len(currHavingFun) == 0):
        borrowingBike = initArrival.popleft()
        if borrowingBike[0] > 1440: break
        processor(borrowingBike, True)
    elif (len(initArrival) == 0):
        returningBike = currHavingFun.popleft()
        if returningBike[0] > 1440: break
        processor(returningBike, False)
    else:
        currRiding = currHavingFun.popleft()
        currArrival = initArrival.popleft()
        if currRiding <= currArrival:
            if currRiding[0] > 1440: break
            initArrival.appendleft(currArrival)
            processor(currRiding, False)
        else:
            if currArrival[0] > 1440: break
            currHavingFun.appendleft(currRiding)
            processor(currArrival, True)

print("Stalling " + str(stallTime))
