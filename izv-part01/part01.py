#!/usr/bin/env python3
"""
IZV cast1 projektu
Autor: Tomáš Valent
Detailni zadani projektu je v samostatnem projektu e-learningu.
Nezapomente na to, ze python soubory maji dane formatovani.

Muzete pouzit libovolnou vestavenou knihovnu a knihovny predstavene na prednasce
"""


from bs4 import BeautifulSoup
import requests
import numpy as np
import matplotlib.pyplot as plt
from typing import List


def integrate(x: np.array, y: np.array) -> float:
    yPart = (y[1:] + y[:-1]) / 2
    xPart = x[1:] - x[:-1]
    return np.sum(xPart * yPart)


def generate_graph(a: List[float], show_figure: bool = False, save_path: str | None=None):
    plt.figure(figsize=(6,4))
    for i in a:
        x = np.linspace(-3.0, 3.0)
        y = np.multiply(i, np.multiply(x, x))
        plt.fill_between(x, y, alpha=0.1)
        plt.annotate(r"$\int f_{" + str(i) + r"}(x)dx$", xy=(3.01, np.multiply(i, np.multiply(3, 3)) - 0.5))

        plt.plot(x, y, label = r"$y_{" + str(i) + r"}(x)$")


    ax = plt.subplot()
    ax.spines["top"].set_bounds(-3, 4.1)
    ax.spines["bottom"].set_bounds(-3, 4.1)
    ax.spines["right"].set_position(("axes", 1.12))
    ax.spines["left"].set_position(("axes", 0.046))

    plt.ylim((-20,20))
    plt.xlabel("$x$")
    plt.ylabel("$f_a(x)$")

    plt.legend(loc='lower left', bbox_to_anchor=(0.14, 1., 0., .0), ncol=3)
    plt.tight_layout(pad=2)

    if save_path:
        plt.savefig(save_path)

    if show_figure:
        plt.show()

    plt.close()


def generate_sinus(show_figure: bool=False, save_path: str | None=None):
    pass


def download_data(url="https://ehw.fit.vutbr.cz/izv/temp.html"):
    pass


def get_avg_temp(data, year=None, month=None) -> float:
    pass
