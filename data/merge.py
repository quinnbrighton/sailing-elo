import pandas as pd
#from sklearn.preprocessing import StandardScaler
#from torch.utils.data import random_split
#import torch
#import numpy as np
#from sklearn.preprocessing import OneHotEncoder
import csv

def load_csv(file_path, drop_columns=None):
    """Load CSV and optionally drop specified columns."""
    df = pd.read_csv(file_path)
    if drop_columns:
        drop_columns_from_dataframe(df, drop_columns)
    return df


def merge_dataframes(base, *args, **kwargs):
    """Recursively merge dataframes."""
    if not args:
        return base
    return base.merge(merge_dataframes(*args), **kwargs)


df2 = load_csv('./data/skippers.csv')
df1 = load_csv('./data/coefsoutput2.csv')

df3 = merge_dataframes(df1,df2,on='id', how='inner')

#df4 = load_csv('./data/skippers.csv')

#df5 = merge_dataframes(df3,df4,on='id', how='inner')

df_sorted_desc = df3.sort_values(by="x", ascending=False)

print(df_sorted_desc)


with open("data/coefsoutput3.csv", 'w') as racefile:
    race_writer = csv.writer(racefile)
    race_writer.writerows(df_sorted_desc.values)