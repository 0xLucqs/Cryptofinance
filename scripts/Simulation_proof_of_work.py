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
times = []
counter = 0
nb_iter = 10000
while counter < nb_iter:
    block = urandom(200)
    while int(hash, 16) > limit:
        hash = sha256(urandom(32) + block).hexdigest()
        if time() - start > 3:
            print("Moins difficile")
            start = time()
            diff += 1
            limit = val**diff

    times.append(time() - start)
    start = time()
    hash = hex(limit + 1)
    counter += 1
times = sorted(times, reverse=True)
print(kstest(times, 'expon'))  # kolmogorov smrinoff test expliquer
plt.plot(list(range(nb_iter)), times)
plt.show()
