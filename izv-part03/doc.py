#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def getDataframe(filename: str) -> pd.DataFrame:
    """
    Funkcia k úlohe 3. Naèíta a ulo¾í dáta zo zadaného súboru

    :param filename: názov súboru

    :return: výsledný dataframe
    """
    df = pd.read_pickle(filename)

    df["p2a"] = pd.to_datetime(df["p2a"])
    df.rename(columns={"p2a": "date"}, inplace=True)

    return df


def plotFig(df: pd.DataFrame, fig_location: str, show_figure: bool):
    """
    Funkcia k úlohe 3. Vytvára graf k druhom zrá¾ok vozidiel z dataframe, ktorý vráti funkcia getDataframe.

    :param df: dataframe s udajmi
    :param fig_location: miesto kam sa graf ulozi
    :param show_figure: parameter na zobrazenie grafu pri spusteni
    """

    dictionary = {1: "celni", 2: "bocni", 3: "bocni", 4: "zezadu", 0: "0"}

    sns.set_style("darkgrid")

    data = df[["region", "date", "p7", "p1"]].copy()
    data = data[data["p7"] != 0]
    data.set_index("region", inplace=True)
    data = data.loc[["PHA", "STC", "JHC", "PLK"]].reset_index()

    data["p7"] = data["p7"].map(dictionary)
    data["date"] = data["date"].dt.month

    data = data.groupby(["region", "p7", "date"]).agg({"p1": "count"}).reset_index()

    g = sns.catplot(x="date", y="p1", col="region", col_wrap=2, sharey=False, sharex=False,
                    hue="p7", data=data, legend=True, kind="bar")

    g.set_titles("Kraj: {col_name}")
    g.legend.set_title("Druh srazky")
    g.legend.set_frame_on(True)

    for axe in g.axes.flat:
        axe.set_xlabel("Mesic")
        axe.set_ylabel("Pocet nehod")

    g.tight_layout()

    # save and show graph
    if fig_location:
        plt.savefig(fig_location)

    if show_figure:
        plt.show()

    plt.close()


def plotTable(df: pd.DataFrame):
    pass


if __name__ == "__main__":  
    df = getDataframe("accidents.pkl.gz")
    plotFig(df, fig_location="fig.pdf", show_figure=True)
    plotTable(df)