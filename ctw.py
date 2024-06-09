import math
from node import Node, nodes

# P(x_i == 1 | x_0:i-1)

# enwik6: 100000000
#   gzip: 36936694
#     7z: 26080305 

# enwik4: 10000
#   gzip: 3820
#     7z: 3738

enw = open("enwik4", "rb").read()

def bitgen(x):
    for c in x:
        for i in range(8):
            yield int((c & (0x80>>i)) != 0)

def setgen(x, l):
    bg = bitgen(x)
    ret = []
    while 1:
        ret.append(next(bg))
        ret = ret[-l:]
        if len(ret) == l:
            yield ret


NUMBER_OF_BITS = 24
sg = setgen(enw, NUMBER_OF_BITS)    
bg = bitgen(enw)

root = Node()
H = 0.0
try:
    prevx = [0]*(NUMBER_OF_BITS+1)
    while 1:
        x = next(bg)

        p_x = root.getp(prevx)
        H += -math.log2(p_x)

        prevx.append(x)
        prevx = prevx[-NUMBER_OF_BITS-1:]
        root.add(prevx)
except StopIteration:
    pass

print(NUMBER_OF_BITS)
print("%.2f bytes of entropy, %d nodes" % (H/8.0, len(nodes)))

from collections import defaultdict

NUMBER_OF_BITS = 16

lookup = defaultdict(lambda: [0, 0])
bg = bitgen(enw)
H = 0.0
try: 
    prevx = [0]*NUMBER_OF_BITS
    while 1:
        x = next(bg)

        # use tables
        px = tuple(prevx)

        # lookup[px] = P(x_i == 1 | x_i-5:i-1)
        # https://en.wikipedia.org/wiki/Krichevsky–Trofimov_estimator
        p_x = (lookup[px][x] + 0.5) / (lookup[px][0] + lookup[px][1] + 1)
        H += -math.log2(p_x)

        # increment tables
        lookup[px][x] += 1
        prevx.append(x)
        prevx = prevx[-NUMBER_OF_BITS:]

except StopIteration:
    pass

print("%.2f bytes of entropy" % (H/8.0))