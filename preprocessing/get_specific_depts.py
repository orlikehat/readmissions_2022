# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 13:35:11 2021

@author: orlyk
"""

import pandas as pd
import numpy as np

def get_specific_depts(df_all):
    df=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\population\df_readmin_with_labels_base.pkl")
    
    df_neuro=df[df["MedOrgTreeDisch"]==137]
    df_cardio=df[df["MedOrgTreeDisch"]==316]
    df_dermo=df[df["MedOrgTreeDisch"]==139]
    df_uro=df[df["MedOrgTreeDisch"]==164]
    
    df_neuro=df_neuro["CaseNum"]
    df_cardio=df_cardio["CaseNum"]
    df_dermo=df_dermo["CaseNum"]
    df_uro=df_uro["CaseNum"]
    
    df_neuro=pd.merge(df_neuro,df_all, how="left",on="CaseNum")
    df_cardio=pd.merge(df_cardio,df_all, how="left",on="CaseNum")
    df_dermo=pd.merge(df_dermo,df_all, how="left",on="CaseNum")
    df_uro=pd.merge(df_uro,df_all, how="left",on="CaseNum")

    
    return df_neuro,df_cardio,df_dermo,df_uro

