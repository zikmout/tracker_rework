import os
import pandas as pd

def get_df_from_excel(filename):
    # TODO: Add !! , index_col=[0]) 
    # to get rid of dirty unnamed0 in excel file
	return pd.read_excel(filename) 