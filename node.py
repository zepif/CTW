import math
import numpy as np

nodes = []

NUMBER_OF_BITS = 32

class Node():
    def __init__(self, parent=None):
        global nodes
        self.c = [0, 0]
        self.n = None
        self.pe = self.pw = 0.0
        self.parent = parent

        self.depth = self.parent.depth + 1 if self.parent is not None else 0

        nodes.append(self)

    def __str__(self):
        return "[%d,%d]" % (self.c[0], self.c[1])

    def find(self, prevx, create=False):
        if prevx == []:
            return self
        if self.n is None:
            if create:
                self.n = [Node(self), Node(self)]
            else:
                return self
        return self.n[prevx[-1]].find(prevx[:-1], create)
    
    def update(self, x, reverse=False):
        if reverse == False:
            self.pe += np.log(self.c[x] + 0.5) - np.log(self.c[0] + self.c[1] + 1.0)
            self.c[x] += 1
        else:
            self.c[x] -= 1
            self.pe -= np.log(self.c[x] + 0.5) - np.log(self.c[0] + self.c[1] + 1.0)
        
        if self.n is not None:
            self.pw = np.log(0.5) + np.logaddexp(self.pe, self.n[0].pw + self.n[1].pw)
        elif self.depth == NUMBER_OF_BITS:
            self.pw = self.pe
        else:
            # self.pw = np.log(0.5) + self.pe
            self.pw = self.pe
        
        if self.parent is not None:
            self.parent.update(x, reverse)