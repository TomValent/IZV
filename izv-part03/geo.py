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
    """ Konvertovani dataframe do geopandas.GeoDataFrame se spravnym kodovani"""

    df.dropna(subset=["d"], inplace=True)
    df.dropna(subset=["e"], inplace=True)
    df.reindex()

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
    """ Vykresleni grafu s nehodami s alkoholem pro roky 2018-2021 """
    
    gdf_new = gdf.set_geometry(gdf.centroid).to_crs("EPSG:3857")
    gdf_new = gdf_new[gdf_new["p11"] >= 3]
    gdf_new["p2a"] = pd.to_datetime(gdf_new["p2a"], cache=True)
    regi = "PHA"


    gdf1 = gdf_new
    gdf2 = gdf_new
    gdf3 = gdf_new
    gdf4 = gdf_new

    gdfs = [gdf1, gdf2, gdf3, gdf4]
    years = [2018, 2019, 2020, 2021]
    fig, axes = plt.subplots(2, 2, figsize=(16, 9))

    for year, ax, gdf in zip(years, axes.flat, gdfs):
        ax = gdf[(gdf_new["p2a"].dt.year == year) & (gdf_new["region"] == regi)].centroid.plot(ax=ax, markersize=4, color="red", alpha=0.8)
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
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """
    pass

if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf, "geo1.png", True)
    plot_cluster(gdf, "geo2.png", True)
