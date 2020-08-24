import numpy as np
import pandas as pd

def find_most_correlated(df):
    corr      = df.corr()
    upper_tri = corr.where(~np.tril(np.ones(corr.shape)).astype(np.bool))
    cs        = corr_triu.stack()
    return np.abs(cs).sort_values(ascending=False)
