# CTW

CTW compressor. How long before we beat gzip

gzip: 3728 bytes <-- not easy to beat actually
xz:   3656 bytes


## comparing to existing CTW implementations

# https://github.com/cberzan/ctw.git ctw_baseline
gets 3484, so CTW can do better than gzip

Though this code has tons of hacks, notably MAXCOUNTS
If you remove MAXCOUNTS it's crap, but this could be other things
That's the annoying thing about this problem, little bug = slightly worse

And I don't understand it's tree depth

# https://github.com/fumin/ctw.git
gets 4616, err, not good

# https://github.com/gkassel/pyaixi
CTW implementation seems numerically unstable...
