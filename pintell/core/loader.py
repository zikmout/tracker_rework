import os
import pandas as pd

def get_df_from_excel(filename):
    return pd.read_excel(filename)
