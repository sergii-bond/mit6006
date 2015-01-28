
from pqueue import PriorityQueue
import random

p = PriorityQueue()
for i in range(10):
    k = random.randrange(0, 10)
    p.append(k)
    
#for k in [3,7,7,2,0]:
#    p.append(k)

s = []
for i in range(len(p)):
    s.append(p.pop())

print 'Sorted list: ', s
