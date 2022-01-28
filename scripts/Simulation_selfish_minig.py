from tkinter import Button, Tk, TOP, BOTH, Scale, HORIZONTAL
from math import *
from random import *
from gui import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from constants import Constants

constants = Constants()


def X() -> np.ndarray:
    return np.linspace(0, 0.5, 100)


def show_graph(data, legend: [str]) -> None:
    fig = Figure(figsize=(6, 5), dpi=100)
    fig.add_subplot(111).plot(*data)
    fig.legend(legend)
    canvas = FigureCanvasTkAgg(fig, master=Frame2)  # A tk.DrawingArea.
    canvas.draw()
    toolbar = NavigationToolbar2Tk(canvas, Frame2)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


def init_graph() -> None:
    limit = len(Frame2.winfo_children())
    if limit > 1:
        for i in range(limit - 1):
            Frame2.winfo_children()[1].destroy()


def BLOCK_TIME() -> int:
    return constants.BLOCK_TIME


def BLOCK_REWARD() -> float:
    return constants.BLOCK_REWARD


def simulation_selfish_mining(n, q, gamma) -> (float, int):
    reward = 0
    time = 0
    i = 0
    while i < n:
        i += 1
        stop = False
        block = 0
        while not stop:
            while random() < q:  # l'attaquant mine un block
                block += 1
                time += BLOCK_TIME()
            if block >= 2:  # l'attaquant écrase la blockchain officielle
                block -= 2
                reward += 2 * BLOCK_REWARD()
            elif block == 1 and random() > q:  # l'attaquant perd
                block = 0
                if random() < gamma:  # il tente de diffuser son block aux grace a sa connectivité
                    reward += BLOCK_REWARD()
            elif block == 0:  # l'attaquant est en retard
                time += BLOCK_TIME()
            stop = block == 0

    return reward, time


def RMP() -> None:
    init_graph()
    # Rendement malhonnete pratique
    x, y = X(), []
    _, nb_of_cycles, connectivity = valider()
    for el in x:
        R, T = simulation_selfish_mining(nb_of_cycles, el, connectivity)
        y.append(R / T)
    *_, connectivity = valider()
    plt.text(0.1, 0.004, f"{connectivity =}")
    show_graph((x, y), ["Rendement Malhonnete Pratique"])


def RMP_RHT() -> None:
    init_graph()
    # Rendement malhonnete pratique
    x, y = X(), []
    _, nb_of_cycles, connectivity = valider()
    for el in x:
        RT = simulation_selfish_mining(nb_of_cycles, el, connectivity)
        y.append(RT[0] / RT[1])
    # Rendement honnete theorique
    x1, y1 = X(), []
    for el in x:
        y1.append(el * constants.BLOCK_REWARD / constants.BLOCK_TIME)
    show_graph((x, y, x1, y1), ["Rendement malhonnete Pratique", "Rendement Honnete"])


def rendement_theorique(q: float, gamma: float) -> float:
    p = 1 - q

    earning = q * BLOCK_REWARD() / BLOCK_TIME()
    rendement = earning - (1 - gamma) * (
                p ** 2 * q * (p - q) * BLOCK_REWARD() / (((1 + p * q) * (p - q) + p * q) * BLOCK_TIME()))
    return rendement


# Rendement malhonnete theorique
def RMT() -> None:
    init_graph()
    x, y = X(), []
    *_, connectivity = valider()
    for el in x:
        y.append(rendement_theorique(el, connectivity))
    show_graph((x, y), ["Rendement Malhonnete Theorique"])


def RHT() -> None:
    init_graph()
    x1, y1 = X(), []
    for el in x1:
        y1.append(el * 6.25 / 600)
    show_graph((x1, y1), ["Rendement Honnete"])


def RMT_RHT() -> None:
    init_graph()
    x, y = X(), []
    *_, connectivity = valider()
    for el in x:
        y.append(rendement_theorique(el, connectivity))
    x1, y1 = X(), []
    for el in x1:
        y1.append(el * 6.25 / 600)
    show_graph((x, y, x1, y1), ["Rendement malhonnete Theorique", "Rendement Honnete"])


top = Tk()
top.wm_title("Simulation selfish Mining")


def selfish() -> None:
    relative_mining_power, nb_of_cycles, connectivity = valider()
    selfish = simulation_selfish_mining(nb_of_cycles, relative_mining_power, connectivity)
    Res.delete(0, 50)
    Res.insert(0, f"Gain(BTC): {selfish[0]} Temps(s): {selfish[1]}")


def valider() -> (float, int, float):
    relative_mining_power = float(q.get())/100
    nb_of_cycles = int(n.get())
    connectivity = float(gamma.get())/100
    return relative_mining_power, nb_of_cycles, connectivity


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

lblGAMMA = create_label(frame=Frame1, text="Connectivité", row=3, col=1)
gamma = Scale(Frame1, from_=0, to=100, orient=HORIZONTAL)
gamma.set(20)
gamma.grid(column=1, row=4)

Res = Entry(Frame1, width=50)
Res.grid(row=4, column=2)

lbl1 = create_label(frame=Frame1, text="", row=5, col=1)

C = Button(Frame1, text="selfish mining", command=selfish)
C.grid(row=3, column=2)

A = Button(Frame1, text="rendement malhonnête pratique", command=RMP)
A.grid(row=6, column=1)

AB = Button(Frame1, text="rendement malhonnête pratique et honnête théorique", command=RMP_RHT)
AB.grid(row=7, column=1)

B = Button(Frame1, text="rendement malhonnête théorique", command=RMT)
B.grid(row=6, column=2)

D = Button(Frame1, text="rendement honnête théorique", command=RHT)
D.grid(row=7, column=2)

E = Button(Frame1, text="Rendement honnête et malhonnête théorique", command=RMT_RHT)
E.grid(row=8, column=1)

lbl3 = create_label(frame=Frame1, text="", row=9, col=1)

lblG = Label(Frame2, text="Graphique")
lblG.pack()


def _quit():
    top.quit()  # stops mainloop
    top.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = Button(master=Frame1, text="Quit here don't close the window", command=_quit)
button.grid(row=8, column=2)

top.mainloop()
