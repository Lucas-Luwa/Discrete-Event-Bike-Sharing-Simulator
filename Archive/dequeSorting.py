import random
import numpy as np
import time
import dataStorage
from collections import deque
import queue

initArrival = deque()
initArrival.append((1,2));
initArrival.append((3,5));
initArrival.append((5,1));
initArrival.append((2,2));
initArrival.append((20,-2));
initArrival.appendleft((21,100));
print(initArrival)
print(sorted(initArrival))
initArrival = queue.deque(sorted(initArrival))
initArrival.appendleft(2)
print(initArrival)


