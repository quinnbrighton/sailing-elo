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

#df1 = load_csv('./data/crews.csv')
df2 = load_csv('./data/skippers.csv')
df3 = load_csv('./data/sailors_roster.csv')

#df3.columns = ['name'] + list(df3.columns[1:])


df4 = merge_dataframes(df2,df3,on='name', how='inner')
#df5 = merge_dataframes(df1,df3,on='name', how='inner')

#df4 = load_csv('./data/skippers.csv')

#df5 = merge_dataframes(df3,df4,on='id', how='inner')

df_sorted_desc = df4.sort_values(by="Adjusted Estimate", ascending=False)

print(df_sorted_desc)

df_sorted_desc.to_csv("data/skipperranks.csv", index=False)


#df_sorted_desc = df5.sort_values(by="Estimate", ascending=False)

#print(df_sorted_desc)

#df_sorted_desc.to_csv("data/crewranks.csv", index=False)

