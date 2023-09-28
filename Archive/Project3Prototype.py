import random
import numpy as np
import time
import dataStorage
from collections import deque
import queue

# Simulation parameters
stationCount = 81
stationBikes = 10
totalRiders = 3500 #10 Originally for debugging
lambdaSymbol = 2.38 #This is riders per minute 1/144 for 10 riders debugging
avgTime = 2.78 #Originally 2.5 for testing
stdTime = 0.619 #Originally 1.0 for testing
stallTime = 0.0 #Holds delay for all riders.
# probStations = [0.2, 0.2, 0.2, 0.2, 0.2] #Testing function
probStations = dataStorage.probStations
probDestinations = dataStorage.probDestinations
# print(len(probDestinations))

currBikes = np.ones((stationCount,)) * stationBikes
stationQueues = [deque() for _ in range(stationCount)]

initArrival = deque()
currtime = 0
i = 0
while i < totalRiders:
    interarrival = np.random.exponential(1/lambdaSymbol)
    stationIndex = np.random.choice(range(stationCount), p=probStations)
    # print(stationIndex)
    initArrival.append((currtime + interarrival, stationIndex)) 
    # initArrival.append((currtime + interarrival, random.randint(0, stationCount-1))) # Replace randomizer later
    currtime += interarrival
    i += 1
# print(currBikes)

j = 0
currHavingFun = deque()
def sortingHelper(input):
    return input[0]

def processor(input, isBorrowing):
    global currHavingFun
    if isBorrowing and currBikes[input[1]] > 0:
        currBikes[input[1]] -= 1
        timeWithBike = np.random.lognormal(avgTime, stdTime)
        destinationIndex = np.random.choice(range(stationCount + 1), p = probDestinations[input[1]])

        # destinationIndex = random.randint(0, stationCount-1) # Replace with real code
        if (destinationIndex != 81):
            currHavingFun.append((input[0] + timeWithBike, destinationIndex))
            currHavingFun = queue.deque(sorted(currHavingFun))
        # print(timeWithBike)
        # print("1bikes "+str(currBikes))
        # print("1havingfun "+str(currHavingFun))
    elif isBorrowing and currBikes[input[1]] == 0:
        destinationIndex = np.random.choice(range(stationCount + 1), p = probDestinations[input[1]])
        #1 The plus one above is intended to account for station 82, which represents all destination indices that doesn't ever have bikes leaving. 
        # destinationIndex = random.randint(0, stationCount-1) # Replace with real code
        if (destinationIndex != 81):
            stationQueues[input[1]].append((input[0], destinationIndex))
            currHavingFun = queue.deque(sorted(stationQueues[input[1]]))
        # print("2bikes "+str(currBikes))
        # print("2station "+str(stationQueues[input[1]]))
    else:
        currBikes[input[1]] +=1
        if len(stationQueues[input[1]]) > 0:
            # print(stationQueues[input[1]])
            stalledPerson = stationQueues[input[1]].popleft()
            global stallTime
            stallTime += input[0] - stalledPerson[0]
            # print("init: "+ str(input[0]) + "x " + str(stalledPerson[0]))
            currBikes[input[1]] -= 1
            timeWithBike = np.random.lognormal(avgTime, stdTime)
            # destinationIndex = random.randint(0, stationCount-1) #Only for testing purposes
            currHavingFun.append((input[0] + timeWithBike, input[1])) #We've figured out the destinationIndex in the second case. 
            currHavingFun = queue.deque(sorted(currHavingFun))
        #     print("3bikes "+str(currBikes))
        #     print("3havingfun "+str(currHavingFun))
        # print("thxforbikeback "+str(currBikes))
        # print("thxforbikeback "+str(currHavingFun))
# i = 0;
while True:
    # print(currHavingFun)
    if (len(currHavingFun) == 0 and len(initArrival) == 0):
        break
    elif (len(currHavingFun) == 0):
        borrowingBike = initArrival.popleft()
        if borrowingBike[0] > 1440: break
        processor(borrowingBike, True)
    elif (len(initArrival) == 0):
        returningBike = currHavingFun.popleft()
        if returningBike[0] > 1440: break
        # print(currHavingFun)
        processor(returningBike, False)
    else:
        currRiding = currHavingFun.popleft()
        currArrival = initArrival.popleft()
        if currRiding <= currArrival:
            if currRiding[0] > 1440: break
            initArrival.appendleft(currArrival)
            # print(currHavingFun)

            processor(currRiding, False)
        else:
            if currArrival[0] > 1440: break
            currHavingFun.appendleft(currRiding)
            processor(currArrival, True)
    # i+=1
print("Stalling " + str(stallTime))
