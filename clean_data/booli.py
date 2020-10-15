import glob
import pandas as pd
import numpy as np
import sys

# the centre of stockholm
clat, clon = 59.329444, 18.068611


def merge_csvs(filename_glob):
    dfs = [pd.read_csv(f) for f in glob.glob(filename_glob)]
    return pd.concat(dfs, ignore_index=True)


def clean_csvs(filename_glob):
    for f in glob.glob(filename_glob):
        df = pd.read_csv(f)
        cf = clean_data(df)
        cf.to_csv(f"clean_{f}")


def clean_data(df, drop_list_price=False):
    cols_to_keep = [
        "daysActive_raw",
        "descriptiveAreaName",
        "floor_raw",
        "isNewConstruction",
        "latitude",
        "listPrice_raw",
        "livingArea_raw",
        "longitude",
        "primaryArea_name",
        "rooms_raw",
        "soldDate_raw",
        "soldPrice_raw",
        "soldSqmPrice_raw",
        "source_name",
        "streetAddress",
    ]
    cols_to_drop = set(df.columns) - set(cols_to_keep)
    df = df.drop(columns=cols_to_drop).rename(columns=lambda c: c.replace("_raw", ""))

    if drop_list_price:
        df.drop(columns="listPrice")
    else:
        df.listPrice = df.listPrice.fillna(df.soldPrice)
        df["bid_factor"] = df.listPrice / df.soldPrice

    df.soldDate = pd.to_datetime(df.soldDate)
    df["dist_from_centre"] = np.sqrt(
        np.square(clat - df.latitude) + np.square(clon - df.longitude)
    )

    return df.dropna()
