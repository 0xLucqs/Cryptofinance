from math import *
from random import *
from tkinter import BOTH, TOP, Entry, Button, Tk, Scale, HORIZONTAL

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from constants import *
from gui import *

global top
constants = Constants()


def BLOCK_TIME() -> int:
    return constants.BLOCK_TIME


def BLOCK_REWARD() -> float:
    return constants.BLOCK_REWARD


def X() -> np.ndarray:
    return np.linspace(0, 0.5, 100)


def init_graph() -> None:
    if len(Frame2.winfo_children()) > 1:
        for i in range(len(Frame2.winfo_children()) - 1):
            Frame2.winfo_children()[1].destroy()


def B(a: int, b: int) -> float:
    return factorial(a - 1) * factorial(b - 1) / factorial(a + b - 1)


def simulation_doublespend(relative_mining_power: float, nb_of_cycles: int, nb_of_confirmations: int,
                           tolerance_threshold: float, double_spend_amount: float) -> (float, int):
    reward = 0
    attack_time = BLOCK_TIME()
    i = 0
    while i < nb_of_cycles:
        i += 1
        if random() < relative_mining_power:
            mineur_h, mineur_a, retard = 0, 0, 0  # tout le monde commence à miner
            while retard < tolerance_threshold and mineur_h < nb_of_confirmations and mineur_a < nb_of_confirmations:
                # tant que l'attaquant n'a pas trop de retard, qu'aucun des mineurs n'a miné assez pour produire les blocs de confirmations l'attaque continue
                if random() < relative_mining_power:
                    mineur_a += 1
                else:
                    mineur_h += 1
                retard = mineur_h - mineur_a
            reward += BLOCK_REWARD() * mineur_a + double_spend_amount if mineur_a == nb_of_confirmations else 0
            # si l'attaquant mine plus de blocs que les mineurs honnête il remporte les blocs rewards + récupère sa mise
            attack_time += BLOCK_TIME() * max(mineur_a, mineur_h)
    return reward, attack_time


# if we assume: A>=2 and A>=z>=1
def attacker_revenue_ratio(z, v, q) -> float:
    # calcul of the binomial coefficient zC(2z-1)
    Cnk = factorial(2 * z - 1) / (factorial(z - 1) * factorial(z))
    # revenue ratio of the attacker
    revenue_ratio = BLOCK_REWARD() / BLOCK_TIME()
    Ra = revenue_ratio * (2 * Cnk * (v / BLOCK_REWARD() + 1) + 2 / B(z, z)) * q ** (z + 1)
    return Ra


def RMT() -> None:
    init_graph()
    x, y = X(), []
    *_, nb_of_confirmations, _, double_spend_amount = valider()
    for el in x:
        y.append(attacker_revenue_ratio(nb_of_confirmations, double_spend_amount, el))
    fig = Figure(figsize=(6, 5), dpi=100)
    fig.add_subplot(111).plot(x, y)
    fig.legend(["Rendement malhonnête Théorique"])
    display_fig(fig)


def RMP() -> None:
    # Rendement pratique en fonction de q
    init_graph()
    x, y = X(), []
    _, nb_of_cycles, nb_of_confirmations, tolerance_threshold, double_spend_amount = valider()
    for el in x:
        reward, attack_time = simulation_doublespend(el, nb_of_cycles, nb_of_confirmations, tolerance_threshold,
                                                     double_spend_amount)
        y.append(reward / attack_time)  # rendement de l'attaque
    fig = Figure(figsize=(6, 5), dpi=100)
    fig.add_subplot(111).plot(x, y)
    fig.legend(["Rendement malhonnête Pratique"])
    display_fig(fig)


def RHT() -> None:
    init_graph()
    x1, y1 = X(), []
    # revenu honnete théorique en fonction de q
    for el in x1:
        y1.append(el * BLOCK_REWARD() / BLOCK_TIME())
    fig = Figure(figsize=(6, 5), dpi=100)
    fig.add_subplot(111).plot(x1, y1)
    fig.legend(["Rendement Honnête"])
    display_fig(fig)


def RMP_RHT() -> None:
    init_graph()
    x, y = X(), []
    _, nb_of_cycles, nb_of_confirmations, tolerance_threshold, double_spend_amount = valider()
    # revenu malhonnête pratique en fonction de q
    for el in x:
        reward, attack_time = simulation_doublespend(el, nb_of_cycles, nb_of_confirmations, tolerance_threshold,
                                                     double_spend_amount)
        y.append(reward / attack_time)
    x1, y1 = X(), []

    # revenu malhonnête théorique en fonction de q
    for el in x1:
        y1.append(el * BLOCK_REWARD() / BLOCK_TIME())
    fig = Figure(figsize=(6, 5), dpi=100)
    fig.add_subplot(111).plot(x, y, x1, y1)
    fig.legend(["Rendement malhonnête Pratique", "Rendement Honnête"])
    display_fig(fig)


def display_fig(fig) -> None:
    canvas = FigureCanvasTkAgg(fig, master=Frame2)  # A tk.DrawingArea.
    canvas.draw()
    toolbar = NavigationToolbar2Tk(canvas, Frame2)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


def RMT_RHT() -> None:
    init_graph()
    x, y = X(), []
    *_, nb_of_confirmations, _, double_spend_amount = valider()
    # rendement honnête théorique en fonction de q
    for el in x:
        y.append(attacker_revenue_ratio(nb_of_confirmations, double_spend_amount, el))
    x1, y1 = X(), []

    # rendement honnête théorique en fonction de q
    for el in x1:
        y1.append(el * BLOCK_REWARD() / BLOCK_TIME())
    fig = Figure(figsize=(6, 5), dpi=100)
    fig.add_subplot(111).plot(x, y, x1, y1)
    fig.legend(["Rendement malhonnête Théorique", "Rendement Honnête"])
    display_fig(fig)


top = Tk()


def double() -> None:
    relative_mining_power, nb_of_cycles, nb_of_confirmations, tolerance_threshold, double_spend_amount = valider()
    double_spend = simulation_doublespend(relative_mining_power, nb_of_cycles, nb_of_confirmations,
                                          tolerance_threshold, double_spend_amount)
    Res.delete(0, 50)
    Res.insert(0, f"Gain(BTC): {double_spend[0]} Temps(s): {double_spend[1]}")


def valider() -> (float, int, int, float, float):
    relative_mining_power = float(q.get()) / 100
    nb_of_cycles = int(n.get())
    nb_of_confirmations = int(z.get())
    tolerance_threshold = int(a.get())
    double_spend_amount = float(v.get())
    return relative_mining_power, nb_of_cycles, nb_of_confirmations, tolerance_threshold, double_spend_amount


Frame1 = Frame(top)
Frame2 = Frame(top)

Frame1.pack()
Frame2.pack()

lblQ = create_label(frame=Frame1, text="Puissance de minage relative de l'attaquant", row=1, col=1)
q = Scale(Frame1, from_=0, to=100, orient=HORIZONTAL)
q.set(20)
q.grid(column=1, row=2)

lblN = create_label(frame=Frame1, text="n (à 10000 pour des graphiques plus lisibles)", row=1, col=2)
n = create_entry(frame=Frame1, text="Nombre de cycles d'attaques", row=2, col=2, value=10000)

lblZ = create_label(frame=Frame1, text="Nombre de blocks de confirmation", row=3, col=1)
z = create_entry(frame=Frame1, text="Nombre de blocks de confirmation", row=4, col=1, value=10)

lblA = create_label(frame=Frame1, text="Seuil de tolérance", row=3, col=2)
a = create_entry(frame=Frame1, text="Seuil de tolérance", row=4, col=2, value=5)

lblV = create_label(frame=Frame1, text="Montant de la double dépense", row=1, col=3)
v = create_entry(frame=Frame1, text="Montant de la double dépense", row=2, col=3, value=10)

C = Button(Frame1, text="double spend", command=double)
C.grid(row=3, column=3)

Res = Entry(Frame1, width=50)
Res.grid(row=4, column=3)

lbl1 = create_label(frame=Frame1, text="", row=5, col=3)

A = Button(Frame1, text="rendement malhonnête pratique", command=RMP)
A.grid(row=6, column=1)

AB = Button(Frame1, text="rendement malhonnête pratique et honnête théorique", command=RMP_RHT)
AB.grid(row=7, column=1)

B1 = Button(Frame1, text="rendement malhonnête théorique", command=RMT)
B1.grid(row=6, column=2)

D = Button(Frame1, text="rendement honnête théorique", command=RHT)
D.grid(row=7, column=2)

E = Button(Frame1, text="Rendement honnête et malhonnête théorique", command=RMT_RHT)
E.grid(row=6, column=3)

lblG = Label(Frame2, text="Graphique")
lblG.pack()


def _quit():
    top.quit()  # stops mainloop
    top.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = Button(master=Frame1, text="Quit here don't close the window", command=_quit)
button.grid(row=7, column=3)
top.mainloop()
