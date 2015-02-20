#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.d = {}
        for p in pairs:
            k, v = p
            self.put(k, v)

    # Associates the value v with the key k.
    def put(self, k, v):
        vlist = self.get(k)
        vlist.append(v)
        self.d[k] = vlist 

    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        if k in self.d:
            return self.d[k]
        else:
            return []
        #raise Exception("Not implemented!")

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    try:
        subseq=''

        while len(subseq) < k:
            subseq += seq.next() 

        rh = RollingHash(subseq)
        p = 0
        while True:
            yield (subseq, rh.current_hash(), p)
            subseq += seq.next() 
            rh.slide(subseq[0], subseq[k])
            subseq = subseq[1:]
            p = p + 1
        
    except StopIteration:
        return 

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    try:
        subseq=''

        while len(subseq) < k:
            subseq += seq.next() 

        rh = RollingHash(subseq)
        p = 0
        j = 1
        while True:
            if j == m:
                yield (subseq, rh.current_hash(), p)
                j = 0

            j += 1
            subseq += seq.next() 
            rh.slide(subseq[0], subseq[k])
            subseq = subseq[1:]
            p = p + 1
        
    except StopIteration:
        return 
    #raise Exception("Not implemented!")

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    d1 = Multidict()
    #for x in subsequenceHashes(a, k):
    for x in intervalSubsequenceHashes(a, k, m):
        (subseq, h1, pos) = x
        #print x
        d1.put(h1, pos)
    #print '\n'
    for y in subsequenceHashes(b, k):
        (subseq, h2, pos2) = y
        #print y 
        positions_a = d1.get(h2)
        if positions_a != []:
            for p in positions_a: 
                yield (p, pos2)

    #raise StopIteration

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
