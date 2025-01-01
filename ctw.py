import sys
import math
import numpy as np
from node import Node, nodes, NUMBER_OF_BITS
from coder import Coder

# P(x_i == 1 | x_0:i-1)

# enwik6: 100000000
#   gzip: 36936694
#     7z: 26080305 

# enwik4: 10000
#   gzip: 3820 <-- not easy to beat actually
#     7z: 3738
#    ctw: 5019.24

enw = open("enwik4", "rb").read()

def clip(x, mn, mx):
    if x < mn:
        x = mn
    if x > mx:
        x = mx
    return x

def bitgen(x):
    for c in x:
        for i in range(8):
            yield int((c & (0x80>>i)) != 0)

def run(fn="enwik4", compress=True):
    if compress:
        enw = open(fn, "rb").read()
        bg = bitgen(enw)
        enc = Coder()
    else:
        dec = Coder(open(fn + ".out", "rb").read())

    root = Node()
    H = 0.0
    cnt = 0
    stream = []
    try:
        prevx = [0]*NUMBER_OF_BITS
        while 1:
            cnt += 1

            # print(root.pw)
            pn = root.find(prevx, True)

            # what if a wild 0 appeared? this is wrong because creation might happen...
            prev = pn.pw
            pn.update(0)
            after_0 = pn.pw
            pn.update(0, True)
            p_0 = np.exp(after_0 - prev)

            if compress:
                x = next(bg)
                enc.code(p_0, x)
            else:
                x = dec.code(p_0)
            stream.append(x)

            p_x = p_0 if x == 0 else (1.0 - p_0)
            H += -math.log2(p_x)

            tn = root.find(prevx, create=True)
            tn.update(x)

            prevx.append(x)
            prevx = prevx[-NUMBER_OF_BITS:]
            if cnt % 5000 == 0:
                ctw_bytes = (root.pw / math.log(2)) / -8
                print("%5d: ratio %.2f%%, %d nodes, %.2f bytes, %.2f ctw" % (cnt//8, H*100.0/cnt, len(nodes), H/8.0, ctw_bytes))

            # TODO: make this generic
            if not compress and cnt == 80000:
                break

    except StopIteration:
        pass

    if compress:
        print("%.2f bytes of entropy, %d nodes, %d bits, %d bytes" % (H/8.0, len(nodes), len(stream), len(enc.ob)))

    if compress:
        with open(fn+'.out', "wb") as f:
            f.write(bytes(enc.ob))
            f.write(bytes([enc.h>>24, 0, 0, 0]))
    else:
        '''
        ob = []
        for i in range(0, len(stream), 8):
            tb = stream[i:i+8]
            rr = 0
            for j in tb:
                rr <<= 1
                rr |= j
            ob.append(rr)
        '''

        ob = [
            int(''.join(str(bit) for bit in stream[i:i+8]), 2)
            for i in range(0, len(stream), 8)
        ]

        with open(fn+".dec", "wb") as f:
            f.write(bytes(ob))

if __name__ == "__main__":
    if sys.argv[1] == "x":
        run(sys.argv[2], False)
    if sys.argv[1] == "c":
        run(sys.argv[2])