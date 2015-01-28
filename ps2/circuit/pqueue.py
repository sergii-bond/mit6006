
class PriorityQueue:
    """Array-based priority queue implementation."""
    def __init__(self):
        """Initially empty priority queue."""
        self.queue = []
    
    def __len__(self):
        # Number of elements in the queue.
        return len(self.queue)
    
    def append(self, key):
        """Inserts an element in the priority queue."""
        if key is None:
            raise ValueError('Cannot insert None in the queue')
        self.queue.append(key)
        #print 'Append ', key
        #print 'Before heapify ', self.queue
        self.heapify_up(len(self.queue) - 1)
        #print 'After heapify ', self.queue
    
    def min(self):
        """The smallest element in the queue."""
        if len(self.queue) == 0:
            return None
        return self.queue[0]
    
    def pop(self):
        """Removes the minimum element in the queue.
    
        Returns:
            The value of the removed element.
        """
        n = len(self.queue) 
        if n == 0:
            return None
        tmp = self.queue[n - 1]
        self.queue[n - 1] = self.queue[0] 
        self.queue[0] = tmp
        popped_key = self.queue.pop()
        self.heapify_down()
        return popped_key
    
    def heapify(self, parent_i):
        if parent_i >= 0 and parent_i < len(self.queue):
            child_i = self.get_min_child_index(parent_i)
            #print "indices, parent: ", parent_i, 'child: ', child_i

            if child_i != None:
                if self.queue[parent_i] > self.queue[child_i]:
                    tmp = self.queue[parent_i]
                    self.queue[parent_i] = self.queue[child_i] 
                    self.queue[child_i] = tmp
                    return child_i

        return False

    #input is a parent index
    def heapify_down(self, ind = 0):
        x = self.heapify(ind)
        if x != False:
            self.heapify_down(x)

    #input is the child index
    def heapify_up(self, ind):
        parent_i = self.get_parent_index(ind)
        x = self.heapify(parent_i)
        if x != False:
            self.heapify_up(parent_i)

    def get_parent_index(self, i):
        return (i + 1) // 2 - 1

    def get_min_child_index(self, i):
        (lc, rc) = (2 * (i + 1) - 1, 2 * (i + 1))
        if lc >= len(self.queue) and rc >= len(self.queue):
            return None
        elif lc >= len(self.queue):
            return rc
        elif rc >= len(self.queue):
            return lc
        else: 
            lc_val = self.queue[lc]
            rc_val = self.queue[rc]
            if rc_val < lc_val:
                return rc
            else:
                return lc 
