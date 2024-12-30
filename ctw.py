import math
from node import Node, nodes

# P(x_i == 1 | x_0:i-1)

# enwik6: 100000000
#   gzip: 36936694
#     7z: 26080305 

# enwik4: 10000
#   gzip: 3820
#     7z: 3738
#    ctw: 2941.22 how it feels gzip to be beaten in 90 lines???

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

def quantize(x):
    x = int(x*256.0 + 0.5)
    if x == 0:  
        x = 1
    if x == 255:
        x = 254
    return x

class Encoder():
    def __init__(self, f):
        self.l = 0
        self.h = 1
        self.d = 1
        self.sd = 0
        self.ob = []

    def code(self, p_0, x):
        # this is implied times 256
        pn = p_0 * (self.h - self.l)

        # ok to multiply all by 256
        self.l *= 256
        self.h *= 256
        self.d *= 256
        self.sd += 8

        if x == 0:
            self.h -= pn
        else:
            self.l += pn

        # reduce fractions
        while self.l%2 == 0 and self.h%2 == 0 and self.d%2 == 0:
            self.l //= 2
            self.h //= 2
            self.d //= 2
            self.sd -= 1

        # output bit
        sr = self.sd
        if sr > 8:
            lb = self.l >> (sr-8)
            hb = self.h >> (sr-8)
            if lb == hb:
                self.ob.append(lb)
                self.l -= lb << (sr-8)
                self.h -= lb << (sr-8)
                self.d /= 256
                self.sd -= 8
        #print(hex(self.l), hex(self.h))

enc = Encoder(open("enwik4.out", "wb"))

NUMBER_OF_BITS = 16
sg = setgen(enw, NUMBER_OF_BITS)    
bg = bitgen(enw)

root = Node()
H = 0.0
cnt = 0
try:
    prevx = [0]*(NUMBER_OF_BITS+1)
    while 1:
        cnt += 1
        x = next(bg)

        # finite precision bro
        p_0 = root.getp(prevx, 0)
        enc.code(quantize(p_0), x)

        p_x = p_0 if x == 0 else (1.0 - p_0)
        H += math.log2(1/p_x)

        root.add(prevx, x)
        prevx.append(x)
        prevx = prevx[-NUMBER_OF_BITS-1:]
        if cnt % 5000 == 0:
            print("ratio %.2f%%, %d nodes, %f bytes, %f realbytes" % (H*100.0/cnt, len(nodes), H/8.0, len(enc.ob)))
except StopIteration:
    pass

#print(NUMBER_OF_BITS)
print("%.2f bytes of entropy, %d nodes" % (H/8.0, len(nodes)))
#for n in nodes:
#    print(n)

exit(0)

from collections import defaultdict

NUMBER_OF_BITS = 16

lookup = defaultdict(lambda: [0, 0])
bg = bitgen(enw)
H = 0.0
cnt = 0
try: 
    prevx = [0]*NUMBER_OF_BITS
    while 1:
        cnt += 1
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
        #if cnt % 1000 == 0:
        #    print("ratio %f" % (H*100/cnt))

except StopIteration:
    pass

print("%.2f bytes of entropy" % (H/8.0))