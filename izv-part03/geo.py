#!/usr/bin/python3.10
# coding=utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
import sklearn.cluster
import numpy as np
# muzete pridat vlastni knihovny


def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """
    Funkcia k ulohe 1. Funkcia konvertuje pandas dataframe do geopandas geodataframe.
    
    :param df: dataframe, ktory sa konvertuje
    
    :return: vysledny geodataframe
    """

    df.dropna(subset=["d"], inplace=True)
    df.dropna(subset=["e"], inplace=True)
    df.reindex()
    gdf = None

    try:
        gdf = geopandas.GeoDataFrame(df,
            geometry=geopandas.points_from_xy(df["d"], df["e"]),
            crs="EPSG:5514")
    except:
        print("Error in converting dataframe.\n")
        exit(1)
    
    return gdf
    
def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """
    Funkcia k ulohe 1. Funkcia vykresluje 4 grafy nehod pre 4 roky
    v danom regione zo zadaneho geodataframe
    
    :param gdf: geodataframe s udajmi
    :param fig_location: miesto kam sa graf ulozi
    :param show_figure: parameter na zobrazenie grafu pri spusteni
    """
    
    gdfNew = gdf.set_geometry(gdf.centroid).to_crs("EPSG:3857")
    gdfNew = gdfNew[gdfNew["p11"] >= 3]
    gdfNew["p2a"] = pd.to_datetime(gdfNew["p2a"], cache=True)
    regi = "PHA"


    gdf1 = gdfNew
    gdf2 = gdfNew
    gdf3 = gdfNew
    gdf4 = gdfNew

    gdfs = [gdf1, gdf2, gdf3, gdf4]
    years = [2018, 2019, 2020, 2021]
    fig, axes = plt.subplots(2, 2, figsize=(16, 9))

    for year, ax, gdf in zip(years, axes.flat, gdfs):
        ax = gdf[(gdfNew["p2a"].dt.year == year) & (gdfNew["region"] == regi)].centroid.plot(ax=ax, markersize=4, color="red", alpha=0.8)
        ctx.add_basemap(ax,crs=gdf.crs.to_string(), source=ctx.providers.Stamen.TonerLite)
        ax.set_title(regi + " kraj " + str(year))
        ax.axis("off")

    if fig_location:
        plt.savefig(fig_location)

    if show_figure:
        plt.show()

    plt.close()



def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """
    Funkcia k ulohe 1. Funkcia vykresluje graf nehod na cestach 1., 2. a 3.
    triedy, pomocou zhlukovacieho algoritmu zo zadaneho geodataframe.
    Zobrazuje kriticke miesta
    
    :param gdf: geodataframe s udajmi
    :param fig_location: miesto kam sa graf ulozi
    :param show_figure: parameter na zobrazenie grafu pri spusteni
    """

    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """
    
    regi = "JHC"

    gdf = gdf[(gdf["region"] == regi) & (gdf["p36"] >= 1) & (gdf["p36"] <= 3)].set_geometry(gdf.centroid).to_crs("EPSG:3857")
    coords = np.dstack([gdf.geometry.x, gdf.geometry.y]).reshape(-1, 2)

    # Pouzijem metodu K-means, metodu ucenia sa bez ucitela, pocet clusterov som zvolil 10 experimentalne
    # Vysledok je v atribute labels_
    model = sklearn.cluster.MiniBatchKMeans(n_clusters=10, n_init=3).fit(coords)

    gdfNew = gdf.copy()
    gdfNew["cluster"] = model.labels_
    gdfNew = gdfNew.dissolve(by="cluster", aggfunc={"region": "count"}).rename(columns={"region": "count"})

    gdf_coords = geopandas.GeoDataFrame(
    geometry=geopandas.points_from_xy(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1]))
    gdfMerged = gdfNew.merge(gdf_coords, left_on="cluster", right_index=True).set_geometry("geometry_y")

    plt.figure(figsize=(16, 9))
    ax = plt.gca()
    ax.axis("off")
    ax.set_title("Nehody v " + regi + " kraji na silnicich 1., 2. a 3. tridy")

    gdf.plot(ax=ax, color="tab:grey", alpha=0.5, markersize=1)
    gdfMerged.plot(ax=ax, markersize=gdfNew["count"] , column="count", legend=True, alpha=0.4)
    ctx.add_basemap(ax, crs="epsg:3857", source=ctx.providers.Stamen.TonerLite, alpha=0.6)

    if fig_location:
        plt.savefig(fig_location)

    if show_figure:
        plt.show()

    plt.close()


if __name__ == "__main__":  
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf, "geo1.png", True)
    plot_cluster(gdf, "geo2.png", True)
