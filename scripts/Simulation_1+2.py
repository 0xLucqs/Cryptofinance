from secrets import randbelow

import matplotlib.pyplot as plt
import numpy as np


def attack(cycles, q):
    alice_blocks = []
    for _ in range(cycles):
        block = 0
        h = 0
        for i in range(3):
            rand = randbelow(101)
            if rand <= q:  # l'attaquant mine un block
                block += 1
                h += 1
            elif i == 0 and rand > q:  # les mineurs honnêtes minent le premier block
                h = 1
                break
        if block == 1:  # si l'attaquant n'a miné qu'un seul block il ne gagne donc rien
            h = 2
            block = 0
        alice_blocks.append((block, h))
    return alice_blocks
def main():
    q_vals = [q / 10 for q in range(0, 500, 2)]
    cycles = 10000

    res = [[x for x in attack(cycles, q)] for q in q_vals]
    val = [sum(num for num, den in x)/sum(den for num, den in x) for x in res]
    q_vals = [q / 100 for q in q_vals]
    plt.plot(q_vals, val, label="rendement malhonnête pratique")
    plt.plot(np.linspace(0, 0.5, 100), np.linspace(0, 0.5, 100), label="rendement honnête théorique")
    plt.legend(loc='upper left')
    plt.show()
main()
