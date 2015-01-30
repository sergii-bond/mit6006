
import random
from RangeIndex import RangeIndex

r = RangeIndex() 

#for i in [5, 7, 9, 4, 1, 0, 24, 45, 34, 21, 38]: 
#    r.add(i)

#for i in range(15):
#    r.add(random.randint(10,30))
#for i in random.sample(range(10,25), 15):

l = []
for i in random.sample(range(0,10), 9):
    l.append(i)
#l = [7, 0, 9, 2, 8, 3, 6, 5, 4]
#l = [1, 5, 0, 8, 3, 7, 9, 2, 4] 
#l = [0, 1, 2, 5, 6, 4, 7, 9, 8] 
print l
for i in l:
    r.add(i)

#print "Range:", r.range(100)
#print "Count_by_key:", r.count_by_key(2)
print "Count:", r.count(2, 7)
print "List:", 
for n in r.list(2, 7):
    print n.key

print r
x = random.sample(range(0,10), 1)[0]
r.remove(x)
print "after removal of", x, ":\n", r
#for i in [9, 6, 3, 0, 5, 4, 7, 2, 1]:
#    r.add(i)
    

