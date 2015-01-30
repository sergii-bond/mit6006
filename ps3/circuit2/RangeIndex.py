
class RangeIndex(object):
    """AVL-tree range index implementation."""
  
    def __init__(self):
        """Initially empty range index."""
        #self.root = Node(None, None)
        self.root = None
  
    def add(self, key):
        """Inserts a key in the range index."""
        if key is None:
            raise ValueError('Cannot insert nil in the index')

        n = Node(key, None)

        if self.root == None:
            self.root = n
        else:
            self.insert(self.root, n)
            #print "Before balancing: \n", self, "\n"
            self.balance(n.p)
            #print "After balancing: \n", self, "\n"

    #
    # Updates the nodes' height recursively up the hierarchy
    # input - Node to be updated. It is assumed children 
    # have the correct hight
    #
    def update_nodes_heights(self, n):
        if n != None:

            res_h = max(n.lc.h, n.rc.h) + 1
            # think of improvement later
            #if n.h != res_h:
            n.h = res_h
            self.update_nodes_heights(n.p)
    #
    # Updates the nodes' sizes recursively up the hierarchy
    # input - Node to be updated. It is assumed children 
    # have the correct sizes
    #
    def update_nodes_sizes(self, n):
        if n != None:

            res_size = n.lc.size + n.rc.size + 1
            if n.size != res_size:
                n.size = res_size
                self.update_nodes_sizes(n.p)

    #
    # inserts the node into the tree
    # x - root of the (sub)tree
    # n - node to be inserted
    # size of all roots of all (sub)trees where the node is inserted is increased by 1
    #
    def insert(self, x, n):
        x.size += 1
        if n > x:
            if x.rc.key == None:
                n.p = x
                x.rc = n
                self.update_nodes_heights(n.p)
            else:
                self.insert(x.rc, n)
        else:
            if x.lc.key == None:
                n.p = x
                x.lc = n
                self.update_nodes_heights(n.p)
            else:
                self.insert(x.lc, n)


    #
    # balances the AVL tree
    # performs recursive rotatations if |lc - rc| > 1
    #
    def balance(self, subtree_root):
        if subtree_root == None:
            return
        lc = subtree_root.lc
        rc = subtree_root.rc

        if lc.h > rc.h + 1:
            #print "Trying to balance right", "root=", subtree_root.key, "rc.h=", rc.h, "lc.h=", lc.h
            p = self.rotate(subtree_root, 0)
            self.balance(p)
        elif rc.h > lc.h + 1:
            #print "Trying to balance left", "root=", subtree_root.key, "rc.h=", rc.h, "lc.h=", lc.h
            p = self.rotate(subtree_root, 1)
            self.balance(p)
        else:
            self.balance(subtree_root.p)

         
    #
    # Rotates the tree
    # direction is 'right' (0) or 'left' (1)
    #
    def rotate(self, subtree_root, direction):
        if direction == 0:
            lc = subtree_root.lc
            rc = subtree_root.rc
            lclc = lc.lc
            lcrc = lc.rc
        else:
            lc = subtree_root.rc
            rc = subtree_root.lc
            lclc = lc.rc
            lcrc = lc.lc

        if (lc.key == None) or (lclc.h >= lcrc.h):
            #print "rotating one time\n"
            self._rotate_op(subtree_root, direction)
            #print self
            return lc.p
        else: 
            #print "rotating two times\n"
            self._rotate_op(lc, abs(direction - 1))
            self._rotate_op(subtree_root, direction)
            #print self
            return lcrc.p 

    def _rotate_op(self, subtree_root, direction):

        if direction == 0:
            a = subtree_root
            b = a.lc
            c = a.rc
            d = b.lc
            e = b.rc

            if a.p == None:
                b.p = None
                self.root = b
            else:
                a.p.set_child(b)
                b.p = a.p

            e.p = a
            a.p = b
            a.lc = e
            b.rc = a
            self.update_nodes_heights(a)
            #update size
            a.size = e.size + c.size + 1
            b.size = b.size - e.size + a.size

        else:
            b = subtree_root
            d = b.lc
            a = b.rc
            e = a.lc
            c = a.rc

            if b.p == None:
                a.p = None
                self.root = a
            else:
                b.p.set_child(a)
                a.p = b.p

            e.p = b
            b.rc = e
            a.lc = b
            b.p = a
            self.update_nodes_heights(b)
            #update size
            b.size = d.size + e.size + 1
            a.size = a.size - e.size + b.size

    #
    # returns the number of elements that are < l
    # 
    def range(self, l):
        return self._range(l, self.root)

    def _range(self, l, x):

        while (l <= x.key):
            x = x.lc

        if x.key == None:
            return 0

        #print x.lc
        return x.lc.size + 1 + self._range(l, x.rc)

    #
    # returns the number of occurrences of 'key' in the tree
    #
    def count_by_key(self, key):
        return self._count_by_key(key, self.root)

    def _count_by_key(self, key, node):
        if node.key == None:
            return 0

        s = 0
        if node.key == key:
            s += 1

        if key >= node.key:
            s += self._count_by_key(key, node.rc)

        if key <= node.key:
            s += self._count_by_key(key, node.lc)

        return s

    #
    # returns the first occurrences of node with 'key' in the tree
    #
    def find_by_key(self, key):
        return self._find_by_key(key, self.root)

    def _find_by_key(self, key, node):
        if node.key == None:
            return None 

        if node.key == key:
            return node

        if key >= node.key:
            return self._find_by_key(key, node.rc)

        if key <= node.key:
            return self._find_by_key(key, node.lc)
    #
    # Returns the minimum element of the whole tree
    #
    def find_min(self):
        return self._find_min(self.root)
    #
    # Returns the minimum element of the sub-tree
    #
    def _find_min(self, node):
        if node.lc.key == None:
            return node 
        else:
            return self._find_min(node.lc)
    #
    # Returns the maximum element of the whole tree
    #
    def find_max(self):
        return self._find_max(self.root)
    #
    # Returns the maximum element of the sub-tree
    #
    def _find_max(self, node):
        if node.rc.key == None:
            return node 
        else:
            return self._find_max(node.rc)
            
    #
    # Returns the number of elements that are >= first_key and <= last_key
    # It is assumed last_key >= first_key
    #
    def count(self, first_key, last_key):
       low_cnt = self.range(first_key) 
       high_cnt = self.range(last_key) 

       #print high_cnt, " ", low_cnt
       #return high_cnt - low_cnt + self.count_by_key(first_key) + \
       #         self.count_by_key(last_key)
       return high_cnt - low_cnt + self.count_by_key(last_key)
  
    #
    # Removes the element from the tree
    #
    def remove(self, key):
        """Removes a key from the range index."""
        node = self.find_by_key(key)
        if node == None:
            return

        # won't work if the tree has duplicate keys
        a = node.lc
        b = node.rc

        if node.p == None:
            if a.key == None and b.key == None:
                self.root = None
            elif a.key == None:
                self.root = b
            else:
                # can optimize here and chose left or right sub-tree 
                self.root = b
                ltree_min = self._find_min(b)
                b.p = None
                ltree_min.lc = a
                a.p = ltree_min
                self.update_nodes_sizes(ltree_min)
                self.update_nodes_heights(ltree_min)
                #print "before balancing\n", self
                self.balance(ltree_min)
        elif node > node.p:
            if a.key == None and b.key == None:
                node.p.rc = Node(None, node.p)
            elif a.key == None:
                node.p.rc = b
                b.p = node.p
            elif b.key == None:
                node.p.rc = a
                a.p = node.p
            else:
                ltree_max = self._find_max(a)
                node.p.rc = a
                a.p = node.p
                ltree_max.rc = b
                b.p = ltree_max
                self.update_nodes_sizes(ltree_max)
                self.update_nodes_heights(ltree_max)
                self.balance(ltree_max)
        else:
            if a.key == None and b.key == None:
                node.p.lc = Node(None, node.p)
            elif a.key == None:
                node.p.lc = b
                b.p = node.p
            elif b.key == None:
                node.p.lc = a
                a.p = node.p
            else:
                ltree_min = self._find_min(b)
                node.p.lc = b
                b.p = node.p
                ltree_min.lc = a
                a.p = ltree_min
                self.update_nodes_sizes(ltree_min)
                self.update_nodes_heights(ltree_min)
                self.balance(ltree_min)
  
    def list(self, first_key, last_key):
        """List of values for the keys that fall within [first_key, last_key]."""
        r = self._lca(first_key, last_key)
        #print "lca:", r.key
        if r.key == None:
            return []
        else:
            lst = []
            self._add_node(r, first_key, last_key, lst)
            return lst

    #
    # Traverses a subtree and returns all nodes within the given range
    # l <= x <= h
    #
    def _add_node(self, node, l, h, lst):
        if (l <= node.key and node.key <= h):
            lst.append(node)
            #print 'appending:', node.key, "lc:", node.lc, "rc:", node.rc
            self._add_node(node.rc, l, h, lst)
            self._add_node(node.lc, l, h, lst)
        elif node.key < l and node.key != None:
            self._add_node(node.rc, l, h, lst)
        elif node.key > h:
            self._add_node(node.lc, l, h, lst)

    #
    # LCA = least common ancestor
    # Returns the node that is a root of the subtree
    # which includes both 'l' and 'h' (imaginary nodes)
    #
    def _lca(self, l, h):
        node = self.root
        while not (l <= node.key and node.key <= h):
            if node.key < l:
                node = node.rc
            else:
                node = node.lc
        return node 
  
  
    #
    #returns the string representing binary tree
    #looking good only up to tree height 6
    #
    def __str__(self):
        l = []
        l = self.out(self.root, 0, 120/2, l)
        l.sort()
        s = ""
        j = 0
        just = 0
        for i in range(len(l)):
            y, x, node = l[i][0], l[i][1], l[i][2]
            if y > j:
                j = j + 1
                s = s + '\n\n'
                just = 0

            s = s + repr(node.key).rjust(x - just) \
                    + "/" + repr(node.size) \
                    + "/" + repr(node.h)
            just = l[i][1]
        return s
            

    #returns a list of Nodes with (x, y) 'coordinates'
    #sorted by y first, then by x
    def out(self, node, y, x, l = []):
        l.append([y, x, node])
        next_y = y + 1
        d = int(120 / (2**next_y + 1) / 2)

        if node.rc.key != None:
            self.out(node.rc, next_y, x + d, l)

        if node.lc.key != None:
            self.out(node.lc, next_y, x - d, l)

        return l

class Node():
    def __init__(self, key, p):
        self.key = key
        self.p = p

        if key == None:
            self.lc = None
            self.rc = None
            self.h = -1 
            self.size = 0
        else:
            self.lc = Node(None, self)
            self.rc = Node(None, self)
            self.h = 0
            self.size = 1

    def set_child(self, node):
        if self > node:
            self.lc = node
        else:
            self.rc = node


    def __gt__(self, other_node):
        if self.key > other_node.key:
            return True
        else:
            return False

    def __str__(self):
        return str(self.key)

