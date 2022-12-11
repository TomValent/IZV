#!/usr/bin/env python3.9
# coding=utf-8

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import zipfile


# muzete pridat libovolnou zakladni knihovnu ci knihovnu predstavenou na prednaskach
# dalsi knihovny pak na dotaz

# Ukol 1: nacteni dat ze ZIP souboru
def load_data(filename: str) -> pd.DataFrame:
    """
    Funkcia k úlohe 1. Funkcia načítava dáta zo zipov z csv súborov a ukladá
    ich do dataframe.

    :param filename: cesta k súboru s dátami

    :return: Dataframe s pridaným stlpcom region
    """
    # tyto konstanty nemente, pomuzou vam pri nacitani
    headers = ["p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13a",
               "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p27",
               "p28",
               "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53", "p55a",
               "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "n", "o", "p", "q", "r", "s", "t",
               "p5a", "region"]

    # def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
    regions = {
        "PHA": "00",
        "STC": "01",
        "JHC": "02",
        "PLK": "03",
        "ULK": "04",
        "HKK": "05",
        "JHM": "06",
        "MSK": "07",
        "OLK": "14",
        "ZLK": "15",
        "VYS": "16",
        "PAK": "17",
        "LBK": "18",
        "KVK": "19",
    }

    dictionary = {f"{value}.csv": key for (key, value) in regions.items()}

    root = zipfile.ZipFile(filename, "r")
    df = pd.DataFrame()

    for i in range(0, len(root.filelist)):
        nestedFile = root.filelist[i]
        fileData = zipfile.ZipFile(root.open(nestedFile))

        for j in range(0, len(fileData.filelist)):
            csvFile = fileData.filelist[j]
            csv = fileData.open(csvFile)

            if csv.name != "CHODCI.csv" and csv.name in dictionary.keys():
                csvObj = pd.read_csv(csv, encoding="cp1250", low_memory=False, delimiter=";", names=headers)
                csvObj["region"] = dictionary[csv.name]

                df = pd.concat([df, csvObj])

        fileData.close()

    root.close()
    return df


# Ukol 2: zpracovani dat
def parse_data(df: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:
    """
    Funkcia k úlohe 2. Funkcia počíta velkost použitej pamäte a vymazáva duplicity stlpca p1,
    premenováva stlpec 'p2a' na 'date' a meni datovy typ hodnot podla potreby.

    :param df: dataframe s udajmi
    :param verbose: parameter na zobrazenie velkosti pouzitej pamati

    :return: Upravený dataframe
    """
    if verbose:
        print(f"orig_size={df.memory_usage(index=True, deep=True).sum() / (10 ** 6):.1f} MB")

    df = df.drop_duplicates(subset=["p1"])
    df2 = df.copy()

    df2["p2a"] = pd.to_datetime(df2["p2a"])
    df2.rename(columns={"p2a": "date"}, inplace=True)

    df2_headers = list(df2)
    df2_headers.pop()
    floatCols = ["d", "e"]

    for header in df2_headers:
        if header in floatCols:
            df2[header] = df2[header].str.replace(",", ".").apply(pd.to_numeric, errors="coerce")
        else:
            df2[df2_headers] = df2[df2_headers].astype("category")

    if verbose:
        print(f"new_size={df2.memory_usage(index=True, deep=True).sum() / (10 ** 6):.1f} MB")

    return df2


# Ukol 3: po�ty nehod v jednotliv�ch regionech podle viditelnosti
def plot_visibility(df: pd.DataFrame, fig_location: str = None,
                    show_figure: bool = False):
    """
    Funkcia k úlohe 3. Vytvára graf počtu nehôd z dataframe, ktorý vráti funkcia parse_data.

    :param df: dataframe s udajmi
    :param fig_location: miesto kam sa graf ulozi
    :param show_figure: parameter na zobrazenie grafu pri spusteni
    """
    dictionary = {1: "ve dne - nezhorsena", 2: "ve dne - zhorsena", 3: "ve dne - zhorsena",
                  4: "v noci - nezhorsena", 5: "v noci - zhorsena", 6: "v noci - nezhorsena", 7: "v noci - zhorsena"}

    sns.set_style("darkgrid")

    data = df[["region", "p19", "p1"]].copy()
    data["p19"] = data["p19"].map(dictionary)
    data = data.groupby(["region", "p19"]).agg({"p1": "count"}).reset_index()

    data = data[data["region"].isin(["PHA", "STC", "JHC", "PLK"])]

    g = sns.catplot(data=data, x="region", y="p1", col_wrap=2, col="p19", sharey=False, kind="bar")

    g.set_titles("Viditelnost: {col_name}")
    g.set_axis_labels("Kraj", "Pocet nehod")
    g.fig.suptitle("Pocet nehod dle viditelnosti")

    plt.tight_layout()

    if fig_location:
        plt.savefig(fig_location)

    if show_figure:
        plt.show()

    plt.close()


# Ukol4: druh sr�ky jedouc�ch vozidel
def plot_direction(df: pd.DataFrame, fig_location: str = None,
                   show_figure: bool = False):
    """
    Funkcia k úlohe 4. Vytvára graf k druhom zrážok vozidiel z dataframe, ktorý vráti funkcia parse_data.

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


# Ukol 5: N�sledky v �ase
def plot_consequences(df: pd.DataFrame, fig_location: str = None,
                      show_figure: bool = False):
    """
    Funkcia k úlohe 5. Vytvára graf počtu nehôd v jednotlivých regiónoch zobrazujúci následky zrážky v čase
    z dataframe, ktorý vráti funkcia parse_data.

    :param df: dataframe s udajmi
    :param fig_location: miesto kam sa graf ulozi
    :param show_figure: parameter na zobrazenie grafu pri spusteni
    """
    sns.set(rc={"axes.facecolor": "#eaeaf2"})

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    data = df[['region', 'date', 'p13a', 'p13b', 'p13c']].copy()
    data.set_index('region', inplace=True)
    data = data.loc[['JHM', 'HKK', 'PLK', 'ZLK']]

    data['p13a'] = data['p13a'].astype(int)
    data['p13b'] = data['p13b'].astype(int)
    data['p13c'] = data['p13c'].astype(int)

    values = list()

    for i in range(0, len(data)):
        if df.iloc[i, 13] == 0:  # p13a
            if df.iloc[i, 14] == 0:  # p13b
                values.append("lahke zraneni")  # p13c
            else:
                values.append("tazke zdraneni")
        else:
            values.append("smrt")

    data["nasledky"] = values

    if fig_location:
        plt.savefig(fig_location)

    if show_figure:
        plt.show()

    plt.close(fig)


if __name__ == "__main__":
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni 
    # funkce.
    df = load_data("data/data.zip")
    df2 = parse_data(df, False)

    plot_visibility(df2, "01_visibility.png")
    plot_direction(df2, "02_direction.png", True)
    plot_consequences(df2, "03_consequences.png")

# Poznamka:
# pro to, abyste se vyhnuli castemu nacitani muzete vyuzit napr
# VS Code a oznaceni jako bunky (radek #%%% )
# Pak muzete data jednou nacist a dale ladit jednotlive funkce
# Pripadne si muzete vysledny dataframe ulozit nekam na disk (pro ladici
# ucely) a nacitat jej naparsovany z disku
