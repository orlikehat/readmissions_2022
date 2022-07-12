# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 13:19:54 2021

@author: orlyk
"""

def get_features(df):
    sex_cols=[col for col in df.columns if 'gender' in col]
    dept_cols=[col for col in df.columns if 'dept' in col]
    disch_cols=[col for col in df.columns if 'discharge_type' in col]
    entry_cols=[col for col in df.columns if 'entry' in col]
    diag_cols=[col for col in df.columns if 'DIAG' in col]
    vent_cols=[col for col in df.columns if 'VENT' in col]
    cci_cols=[col for col in df.columns if 'CCI_Charls' in col]
    cci_bg_cols=[col for col in df.columns if 'CCI_bg' in col]

    med=[col for col in df.columns if 'MEDS_' in col]
    family_stat=[col for col in df.columns if 'family_stat' in col]
    quarter_cols=[col for col in df.columns if 'Quarter' in col]
    week_cols=[col for col in df.columns if 'Week' in col]
    ishpuz_cols=[col for col in df.columns if 'ISHP' in col]
    lab_cols=[col for col in df.columns if 'LABS_' in col]
    vs_cols=[col for col in df.columns if 'VS_' in col]
    norton_cols=[col for col in df.columns if 'NORT' in col]
    prev_cols=[col for col in df.columns if 'PREV_' in col]
    
       
    feat_list=(sex_cols+dept_cols+disch_cols+ entry_cols+diag_cols+
               vent_cols+cci_cols+cci_bg_cols+med+family_stat+quarter_cols+
               ishpuz_cols+lab_cols+vs_cols+norton_cols+prev_cols)
    
    cont_list=(lab_cols+vs_cols+norton_cols+cci_cols)
    lab_vs_list=(lab_cols+vs_cols)
    
    cat_list= (sex_cols+dept_cols+disch_cols+ entry_cols+diag_cols+
               vent_cols+cci_bg_cols+med+family_stat+quarter_cols+week_cols+
               ishpuz_cols)
    
    return feat_list,cont_list,cat_list,lab_vs_list
    
    
    
    
    