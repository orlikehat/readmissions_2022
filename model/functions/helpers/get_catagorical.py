# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 13:34:11 2021

@author: orlyk
"""
import pandas as pd


def get_categorical(df):
    month_cols = [col for col in df.columns if 'month' in col]
    #year_cols=[col for col in df.columns if 'year' in col]
    sex_cols=[col for col in df.columns if 'sex ' in col]
    dept_cols=[col for col in df.columns if 'dept' in col]
    disch_cols=[col for col in df.columns if 'discharge_type' in col]
    entry_cols=[col for col in df.columns if 'entry' in col]
    diag_cols=[col for col in df.columns if 'DIAG' in col]
    vent_cols=[col for col in df.columns if 'VENT' in col]
    cci_cols=[col for col in df.columns if 'CCI_bg' in col]
    med=[col for col in df.columns if 'MEDS_' in col]
    family_stat=[col for col in df.columns if 'family_stat' in col]
    quarter_cols=[col for col in df.columns if 'Quarter' in col]
    week_cols=[col for col in df.columns if 'Week' in col]
    continent_cols=[col for col in df.columns if 'ISHP_ContinentID' in col]
    kupa_cols=[col for col in df.columns if 'ISHP_KupaCode' in col]
    cat_list=disch_cols+month_cols+dept_cols+ entry_cols+diag_cols+vent_cols+sex_cols+cci_cols+family_stat+med+quarter_cols+week_cols+continent_cols+kupa_cols
    
    return cat_list

  
