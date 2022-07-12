# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 15:00:45 2021

@author: orlyk
"""

import pandas as pd
import numpy as np

def cont_to_cat(df,feat_list):
    df_upper=pd.DataFrame(columns = feat_list)
    df_lower=pd.DataFrame(columns = feat_list)
    for col in feat_list:
        df_upper[col]=np.where(df[col]>df[col].quantile(q=0.85),1,0)
        df_lower[col]=np.where(df[col]>df[col].quantile(q=0.15),1,0)
        
    df_upper=df_upper.add_suffix('_CAT_UPPER')
    df_lower=df_lower.add_suffix('_CAT_LOWER')
    
    return df_upper,df_lower

