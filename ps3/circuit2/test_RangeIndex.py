
import random
from RangeIndex import RangeIndex


class KeyWirePair(object):
  """Wraps a wire and the key representing it in the range index.
  
  Once created, a key-wire pair is immutable."""
  
  def __init__(self, key, wire):
    """Creates a new key for insertion in the range index."""
    self.key = key
    if wire is None:
      raise ValueError('Use KeyWirePairL or KeyWirePairH for queries')
    self.wire = wire
    #self.wire_id = wire.object_id
    self.wire_id = wire

  def __lt__(self, other):
    # :nodoc: Delegate comparison to keys.
    return (self.key < other.key or
            (self.key == other.key and self.wire_id < other.wire_id))
  
  def __le__(self, other):
    # :nodoc: Delegate comparison to keys.
    return (self.key < other.key or
            (self.key == other.key and self.wire_id <= other.wire_id))  

  def __gt__(self, other):
    # :nodoc: Delegate comparison to keys.
    return (self.key > other.key or
            (self.key == other.key and self.wire_id > other.wire_id))
  
  def __ge__(self, other):
    # :nodoc: Delegate comparison to keys.
    return (self.key > other.key or
            (self.key == other.key and self.wire_id >= other.wire_id))

  def __eq__(self, other):
    # :nodoc: Delegate comparison to keys.
    return self.key == other.key and self.wire_id == other.wire_id
  
  def __ne__(self, other):
    # :nodoc: Delegate comparison to keys.
    return self.key == other.key and self.wire_id == other.wire_id

  def __hash__(self):
    # :nodoc: Delegate comparison to keys.
    return hash([self.key, self.wire_id])

  def __repr__(self):
    # :nodoc: nicer formatting to help with debugging
    return '<key: ' + str(self.key) + ' wire: ' + str(self.wire) + '>'


class KeyWirePairL(KeyWirePair):
  """A KeyWirePair that is used as the low end of a range query.
  
  This KeyWirePair is smaller than all other KeyWirePairs with the same key."""
  def __init__(self, key):
    self.key = key
    self.wire = None
    self.wire_id = -1000000000

class KeyWirePairH(KeyWirePair):
  """A KeyWirePair that is used as the high end of a range query.
  
  This KeyWirePair is larger than all other KeyWirePairs with the same key."""
  def __init__(self, key):
    self.key = key
    self.wire = None
    # HACK(pwnall): assuming 1 billion objects won't fit into RAM.
    self.wire_id = 1000000000

r = RangeIndex() 

l = []
#b = [2, 9, 1, 8, 0, 4, 6, 5, 7]
b = random.sample(range(0,10), 9)
#b = []
for i in b:
    l.append(KeyWirePair(i, i))
print [x.key for x in l]
for i in l:
    r.add(i)

print "Original:\n", r

low = -100 
high = 1000 

#array of elem to remove
lr = []
c = random.sample(range(0,10), 9)
for i in c:
    lr.append(KeyWirePair(i, i))

for x in lr:
    print "remove", x.key
    r.remove(x)
    l1 = r.list(KeyWirePairL(low), KeyWirePairH(high))
    #print r
    print "By list:", len(l1)
    #print [i.key for i in l1]
    cnt = r.count(KeyWirePairL(low), KeyWirePairH(high))
    print "By count:", cnt 
    if len(l1) != cnt:
        print r

#print "remove", l[0]
#r.remove(l[0])
#print r
