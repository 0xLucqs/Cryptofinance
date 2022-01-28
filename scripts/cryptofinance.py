from hashlib import sha256
from time import time
from os import urandom
import matplotlib.pyplot as plt
from scipy.stats import kstest

val = 2
diff = 256
diff -= int(input("Difficulty?"))

limit = val ** diff
hash = hex(val ** diff + 1)
start = time()
i = 0
j = 0
a = []
con = 0
nb_iter = 10000
while con < nb_iter:
    block = urandom(200)
    while int(hash, 16) > limit:
        hash = sha256(urandom(32) + block).hexdigest()
        if time() - start > 20:
            i += 1
            print("Moins difficile")
            start = time()
            diff += 1
            limit = val**diff

    j += 1
    a.append(time() - start)
    start = time()
    hash = hex(limit + 1)
    con += 1
a = sorted(a, reverse=True)
print(kstest(a, 'expon'))  # kolmogorov smrinoff test expliquer
plt.plot(list(range(nb_iter)), a)
plt.show()
