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

"""
Funkcia k úlohe 1. Výpočet itegrálu lichobežníkovou motódou. 

:param x: Vektor integračných boodv
:param y: Hodnota integrovanej funkcie

:return: Hodnota vypočíaného integrálu
"""
def integrate(x: np.array, y: np.array) -> float:
    yPart = (y[1:] + y[:-1]) / 2
    xPart = x[1:] - x[:-1]
    return np.sum(xPart * yPart)

"""
Funkcia k úlohe 2. Generovanie grafov s rôznymi koeficientami.

:param a: Koeficienty
:param show_figure Určuje, či sa má graf zobraziť po spustení 
:param save_path Určuje, kam sa má graf uložiť ak je zadaná 

:return: Nothing
"""
def generate_graph(a: List[float], show_figure: bool = False, save_path: str | None = None):
    plt.figure(figsize=(6, 4))
    for i in a:
        x = np.linspace(-3.0, 3.0)
        y = np.multiply(i, np.multiply(x, x))
        plt.fill_between(x, y, alpha=0.1)
        plt.annotate(r"$\int f_{" + str(i) + r"}(x)dx$", xy=(3.01, np.multiply(i, np.multiply(3, 3)) - 0.5), size=8)

        plt.plot(x, y, label=r"$y_{" + str(i) + r"}(x)$")

    plt.xlim((-3, 3.99))
    plt.ylim((-20, 20))
    plt.xlabel("$x$")
    plt.ylabel("$f_a(x)$")

    plt.legend(loc='lower left', bbox_to_anchor=(0.14, 1., 0., .0), ncol=3)
    plt.tight_layout(pad=2)

    if save_path:
        plt.savefig(save_path)

    if show_figure:
        plt.show()

    plt.close()

"""
Funkcia k úlohe 3. Generovanie grafov sínusových signálov.

:param show_figure Určuje, či sa má graf zobraziť po spustení 
:param save_path Určuje, kam sa má graf uložiť ak je zadaná 

:return: Nothing
"""
def generate_sinus(show_figure: bool = False, save_path: str | None = None):
    fig, axes = plt.subplots(ncols=1, nrows=3, constrained_layout=True, figsize=(6, 12))

    ax1, ax2, ax3 = axes

    x = np.linspace(0, 100, 1000)

    y1 = 0.5 * np.sin(1 / 50 * np.pi * x)  # 2 - perioda
    y2 = 0.25 * np.sin(np.pi * x)
    ySum = y1 + y2

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
    ax3.plot(x, ySum, color="green")

    mask = np.ma.masked_greater(ySum, y1)
    ax3.plot(x, mask, color="red")

    if save_path:
        fig.savefig(save_path)

    if show_figure:
        plt.show()

"""
Funkcia k úlohe 4. Zťahovanie a ukladanie dát z internetu. 

:param url: URL adresa zdroja

:return: pole stiahnutých dát
"""
def download_data(url="https://ehw.fit.vutbr.cz/izv/temp.html"):
    r = requests.get(url, allow_redirects=True)
    content = BeautifulSoup(r.text, "html.parser")
    rows = content.find_all("tr")
    data = []

    for tr in rows:
        raw_data = np.array([float(i.p.string.replace(",", ".")) for i in tr.find_all("td") if i.p is not None])

        data.append({
            "year": int(raw_data[0]),
            "month": int(raw_data[1]),
            "temp": raw_data[2:]
        })

    return data

"""
Funkcia k úlohe 5.

:param data: stiahnuté dáta z úlohy 4
:param year: ak je zadaný, filtujeme podľa daného roku
:param month: ak je zadaný, filtrujeme podľa daného mesiaca

:return: Priemernú teplotu v danom období
"""
def get_avg_temp(data, year=None, month=None) -> float:
    if year:
        data = filter(lambda x: x["year"] == year, data)
    if month:
        data = filter(lambda x: x["month"] == month, data)

    data = list(data)

    return np.sum([np.sum(i["temp"]) for i in data]) / np.sum([len(i["temp"]) for i in data])
