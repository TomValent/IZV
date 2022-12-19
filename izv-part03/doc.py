#!/usr/bin/python3.10
# coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def getDataframe(filename: str) -> pd.DataFrame:
    """
    Funkcia k úlohe 3. Načíta a uloží dáta zo zadaného súboru

    :param filename: názov súboru

    :return: výsledný dataframe
    """
    df = pd.read_pickle(filename)

    df["p2a"] = pd.to_datetime(df["p2a"])
    df.rename(columns={"p2a": "date"}, inplace=True)

    return df


def plotFig(df: pd.DataFrame, fig_location: str, show_figure: bool):
    """
    Funkcia k úlohe 3. Vytvára graf k druhom zrážok vozidiel z dataframe, ktorý vráti funkcia getDataframe.

    :param df: dataframe s udajmi
    :param fig_location: miesto kam sa graf ulozi
    :param show_figure: parameter na zobrazenie grafu pri spusteni
    """

    dictionary = {1: "čelní", 2: "boční", 3: "boční", 4: "zezadu", 0: "0"}

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

    plt.suptitle("Zrážky vo vybraných krajoch ČR")
    g.set_titles("Kraj: {col_name}")
    g.legend.set_title("Druh zrážky")
    g.legend.set_frame_on(True)

    for axe in g.axes.flat:
        axe.set_xlabel("Mesiac")
        axe.set_ylabel("Počet nehôd")

    g.tight_layout()

    if fig_location:
        plt.savefig(fig_location)

    if show_figure:
        plt.show()

    plt.close()


def printCSVTable(table: pd.DataFrame, printAsTable: bool):
    """
    Pomocná funkcia. Vypisuje tabulku v CSV formáte.

    :param table: tabulka s udajmi
    :param printAsTable: pre výjovové účely vypíše na stdout ako tabulku, inak ako CSV
    """

    if printAsTable:
        print("======== Start table =========")
        print(table)
        print("======== End table =========")
        exit(0)

    #print CSV header
    print("======== Start CSV =========")
    print("Type;Year;Count")

    #print data
    for index, row in table.iterrows():
        for year in table:
            print(str(index) + ";" + str(year[1]) + ";" + str(row[year]))

    print("======== End CSV ========")


def createCSVTable(df: pd.DataFrame, printAsTable: bool):
    """
    Funkcia k úlohe 3. Vytvára tabulku k druhom zrážok vozidiel z dataframe, ktorý vráti funkcia getDataframe.

    :param df: dataframe s udajmi
    :param printAsTable: pre výjovové účely vypíše na stdout ako tabulku, inak ako CSV
    """

    dictionary = {1: "čelní", 2: "boční", 3: "boční", 4: "zezadu", 0: "0"}

    sns.set_style("darkgrid")

    data = df[["region", "date", "p7", "p1"]].copy()
    data = data[data["p7"] != 0]
    data.set_index("region", inplace=True)
    data = data.loc[["PHA"]].reset_index()

    data["p7"] = data["p7"].map(dictionary)

    data["date"] = data["date"].dt.year
    data.rename(columns={"p7": "Druh"}, inplace=True)
    data.rename(columns={"date": "Rok"}, inplace=True)

    data = data.groupby(["region", "Druh", "Rok"]).agg({"count"}).reset_index()
    data.reset_index(inplace=True)
    data.sort_index()

    table = pd.pivot_table(data, index="Druh", columns="Rok", values="p1")
    table = table.astype(int)

    printCSVTable(table, printAsTable)


if __name__ == "__main__":
    df = getDataframe("accidents.pkl.gz")
    plotFig(df, fig_location="fig.png", show_figure=True)
    createCSVTable(df, printAsTable=False)