# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 14:14:10 2021

@author: orlyk
"""

import pandas as pd

def get_age_interactions(df,feat_list):
    ageX_df = pd.DataFrame(columns = feat_list)
    for i in feat_list:
        temp=df[i]*df["age"]
        ageX_df[i]=temp
        
    ageX_df=ageX_df.add_suffix('_X_age')
    
    return ageX_df



def get_age_sq_interactions(df,feat_list):
    ageX_df = pd.DataFrame(columns = feat_list)
    for i in feat_list:
        temp=df[i]*df["age"]*df["age"]
        ageX_df[i]=temp
        
    ageX_df=ageX_df.add_suffix('_X_age_SQ')
    
    return ageX_df
    

def get_cci_interactions(df,feat_list):
    cciX_df = pd.DataFrame(columns = feat_list)
    for i in feat_list:
        temp=df[i]*df["CCI_CharlsDiseases"]
        cciX_df[i]=temp
        
    cciX_df=cciX_df.add_suffix('_X_CCI')
    
    return cciX_df
    