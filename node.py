import math
import numpy as np

nodes = []

NUMBER_OF_BITS = 16

class Node():
    def __init__(self, parent=None, symbols=2):
        global nodes
        self.c = [0]*symbols
        self.n = [None]*symbols
        self.pe = self.pw = 0.0
        self.parent = parent

        self.depth = self.parent.depth + 1 if self.parent is not None else 0

        nodes.append(self)

    def __str__(self):
        return "[%d,%d]" % (self.c[0], self.c[1])

    def find(self, prevx, create=False):
        if prevx == []:
            return self
        if self.n[prevx[-1]] is None:
            if create:
                self.n[prevx[-1]] = Node(self)
            else:
                return self
        return self.n[prevx[-1]].find(prevx[:-1], create)
    
    def update(self, x, reverse=False):
        if reverse == False:
            self.pe += math.log(self.c[x] + 0.5) - math.log(sum(self.c) + 1.0)
            self.c[x] += 1
        else:
            self.c[x] -= 1
            self.pe -= math.log(self.c[x] + 0.5) - math.log(sum(self.c) + 1.0)
        
        tpw = 0
        for nn in self.n:
            if nn is not None:
                tpw += nn.pw
        
        if tpw == 0:
            # self.pw = np.log(0.5) + self.pe
            self.pw = self.pe
        else:
            self.pw = math.log(0.5) + np.logaddexp(self.pe, tpw)

        if self.parent is not None:
            self.parent.update(x, reverse)