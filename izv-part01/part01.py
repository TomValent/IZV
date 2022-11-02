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


    plt.xlim([-3, 4.2])
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

#TODO comments
"""
Few sentences that explain the function. 

:param x: What is it?
:param y: What is it?
:return: What it returns?
"""

def generate_sinus(show_figure: bool=False, save_path: str | None=None):    
    fig, axes = plt.subplots(ncols=1, nrows=3, constrained_layout=True, figsize=(6, 12))

    ax1, ax2, ax3 = axes

    x = np.linspace(0, 100, 1000)

    y1 = 0.5 * np.sin(1/50 * np.pi * x) #2 - perioda 
    y2 = 0.25 * np.sin(np.pi * x)
    ysum = y1 + y2

    ax1.set_xlim((0, 100))
    ax2.set_xlim((0, 100))
    ax3.set_xlim((0, 100))

    ax1.set_xlabel("$t$")
    ax1.set_ylabel("$f_1(x)$")
    ax2.set_xlabel("$t$")
    ax2.set_ylabel("$f_2(x)$")
    ax3.set_xlabel("$t$")
    ax3.set_ylabel("$f_1(x) + f_2(x)$")

    ax1.axis(ymin=-0.8, ymax=0.8)
    ax2.axis(ymin=-0.8, ymax=0.8)
    ax3.axis(ymin=-0.8, ymax=0.8)

    ax1.plot(x, y1)
    ax2.plot(x, y2)
    ax3.plot(x, ysum, color="green")
    
    mask = np.ma.masked_greater(ysum, y1)
    ax3.plot(x, mask, color="red")

    if save_path:
        fig.savefig(save_path)

    if show_figure:
        plt.show()


def download_data(url="https://ehw.fit.vutbr.cz/izv/temp.html"):
    pass


def get_avg_temp(data, year=None, month=None) -> float:
    pass
