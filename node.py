nodes = []

class Node():
    def __init__(self):
        global nodes
        self.c = [0, 0]
        self.n = [None, None]
        nodes.append(self)

    def __str__(self):
        return "[%d,%d]" % (self.c[0], self.c[1])

    def getp(self, x):
        np = (self.c[x[-1]] + 0.5) / (self.c[0] + self.c[1] + 1)
        if self.n[x[-1]] is not None:
            return self.n[x[-1]].getp(x[:-1])
        return np

    def add(self, x):
        t = x[-1]
        self.c[t] += 1
        if x[:-1] == []:
            return
        if self.n[t] is None:
            self.n[t] = Node()
        self.n[t].add(x[:-1])
