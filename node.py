nodes = []

class Node():
    def __init__(self):
        global nodes
        self.c = [0, 0]
        self.n = [None, None]
        nodes.append(self)

    def __str__(self):
        return "[%d,%d]" % (self.c[0], self.c[1])

    def getp_recurse(self, x, p):
        np = (self.c[p] + 0.5) / (self.c[0] + self.c[1] + 1)
        if x != [] and self.n[x[-1]] is not None:
            ret = self.n[x[-1]].getp_recurse(x[:-1], p)
            return ret + [np]
        return [np]

    def getp(self, x, p):
        l = self.getp_recurse(x, p)
        ret = l[-1]
        for x in l[:-1][::-1]:
            ret = 0.5 * ret + 0.5*x
        return ret

    def add(self, x, p):
        self.c[p] += 1
        if x == []:
            return
        t = x[-1]
        if self.n[t] is None:
            self.n[t] = Node()
        self.n[t].add(x[:-1], p)
