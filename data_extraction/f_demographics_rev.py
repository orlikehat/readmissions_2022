# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 11:44:24 2021

@author: orlyk
"""

import pandas as pd
import numpy as np
#from get_connection import f_get_connection
from pathlib import Path
import pyodbc



global global_path_processes_file_pop
#global_path_processes_file_pop = "O:/OrlI/readmissions/preprocessed/demographics/df_demographics_pop.pkl"
global_path_processes_file_pop = "O:/OrlI/readmissions/preprocessed/demographics/df_demographics_pop.pkl"
    

def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn

def f_get_demo_full():
    s_query='''select PatNum,gender
      
      ,family_stat
     
      
      ,HolocaustSurvivor_flg
      ,ChildrenNum
       FROM [DWH_PRD].[dbo].[PRD_DIM_PATIENTS]'''
    cnxn_dwh_prd=f_get_connection('DWH_PRD')
    df=pd.read_sql(s_query, cnxn_dwh_prd)
    return df
#df = df[~df.Result.str.contains("Cancelled")]

def f_get_demo_pop(l_pat=[]):    
    df = f_get_demo_full()

    if len(l_pat) > 0:
        df = df[df['PatNum'].isin(l_pat)]
        df.to_pickle(global_path_processes_file_pop)
    