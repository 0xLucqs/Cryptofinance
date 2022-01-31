from functools import lru_cache
import matplotlib.pyplot as plt


@lru_cache(maxsize=None)  # Memoization
def esperance_sans_block_orphelin(a, h, n, q, c):
    """Espérance de gain maximale d'un mineur si le consensus ne prend pas en compte le nombre de blocks orphelins"""
    if n == 0:  # Plus aucune action n'est disponible, le jeu s'arrête
        if a > h:
            return a - (a - h) * c
        else:
            return 0
    elif a > h + 1:  # Le mineur a + d'un block d'avance sur la blockchain officielle
        return max(h + 1 - c + esperance_sans_block_orphelin(a - h - 1, 0, n, q, c),
                   q * esperance_sans_block_orphelin(a + 1, h, n - 1, q, c) + (1 - q) * (
                           esperance_sans_block_orphelin(a, h + 1, n - 1, q, c) - c))
    elif a == h + 1:  # Le mineur a exactement un seul block d'avance sur la blockchain officielle
        return max(h + 1 - c,
                   q * esperance_sans_block_orphelin(a + 1, h, n - 1, q, c) + (1 - q) * (
                           esperance_sans_block_orphelin(a, h + 1, n - 1, q, c) - c))
    elif a < h + 1:  # le mineur est soit a la même hauteur que la blockchain officielle soit en retard
        return max(0, q * esperance_sans_block_orphelin(a + 1, h, n - 1, q, c) + (1 - q) * (
                esperance_sans_block_orphelin(a, h + 1, n - 1, q, c) - c))


def main1():
    """Affiche l'espérance de gain en fonction de la puissance de calcul du mineur sans tenir compte des blocks
    orphelins """
    q_vals = [q / 1000 for q in range(500)]
    n_vals = [n for n in range(10, 20)]
    res = [[esperance_sans_block_orphelin(0, 0, i, q, q) for q in q_vals] for i in n_vals]
    for n, graph in zip(n_vals, res):
        plt.plot(q_vals, graph, label=f"{n=}")
    plt.legend(loc='upper left')
    plt.show()


@lru_cache(maxsize=None)  # Memoization
def esperance_avec_blocks_orphelins(a, h, n, q, c):
    """Espérance de gain maximale d'un mineur si le consensus prend en compte le nombre de blocks orphelins"""
    if n == 0:  # Plus aucune action n'est disponible, le jeu s'arrête
        if a > h:
            return a * (1 - c)
        else:
            return 0
    elif a > h + 1:  # Le mineur a + d'un block d'avance sur la blockchain officielle
        return max(h + 1 - (h + 1) * c + esperance_avec_blocks_orphelins(a - h - 1, 0, n, q, c),
                   q * esperance_avec_blocks_orphelins(a + 1, h, n - 1, q, c) + (1 - q) * (
                           esperance_avec_blocks_orphelins(a, h + 1, n - 1, q, c) - c))
    elif a == h + 1:  # Le mineur a exactement un seul block d'avance sur la blockchain officielle
        return max(h + 1 - (h + 1) * c,
                   q * esperance_avec_blocks_orphelins(a + 1, h, n - 1, q, c) + (1 - q) * (
                           esperance_avec_blocks_orphelins(a, h + 1, n - 1, q, c) - c))
    elif a < h + 1:  # le mineur est soit a la même hauteur que la blockchain officielle soit en retard
        return max(0, q * esperance_avec_blocks_orphelins(a + 1, h, n - 1, q, c) + (1 - q) * (
                esperance_avec_blocks_orphelins(a, h + 1, n - 1, q, c) - c))


def main2():
    """Affiche l'espérance de gain en fonction de la puissance de calcul du mineur en tenant compte des blocks
        orphelins """
    q_vals = [q / 1000 for q in range(500)]
    n_vals = [n for n in range(10, 20)]
    res = [[esperance_avec_blocks_orphelins(0, 0, i, q, q) for q in q_vals] for i in n_vals]
    for n, graph in zip(n_vals, res):
        plt.plot(q_vals, graph, label=f"{n=}")
    plt.legend(loc='upper left')
    plt.show()


# esperance de gain maximale d'un joueur sous les contraintes : chaque avancée de la blockchain officielle coute c
# le jeu prend fin des que n blocs ont été découverts
# le jeu prend fin des que le joueur revient miner sur le dernier block de la blockchain officielle (le joueur abandonne)
# le gain du joueur est son nombre de jetons s'il est supérieur au nombre de jetons de la banque sinon c'est 0
# n = nombre maximum de block trouvable par le reste du monde
# a = nombre de jetons du joueur
# h = nombre de jetons de la banque
main2()

