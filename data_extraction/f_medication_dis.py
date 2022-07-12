# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 16:27:13 2021

@author: orlyk
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 14:51:27 2021

@author: orlyk
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 14:16:10 2021

@author: orlyk
"""

#count the number of medicarions given during hospitalization
# notice! there is some preprocessing here - only first administartion per casenum per drug

import pandas as pd
import numpy as np
#from get_connection import f_get_connection
from pathlib import Path
import pyodbc

global global_path_processes_file_pop
global_path_processes_file_pop=r"O:\OrlI\readmissions\preprocessed\medications\df_meds_dis_pop.pkl"

# Helper functions
def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn

def f_get_meds_dis_full():
    s_query = '''SELECT [CaseNum]
      
      ,[DrugCode]
      ,[DrugName]
     
      ,[DrugType_Code]
     
  FROM [BI_Dev].[dbo].[CLN_FACT_Medicines]
  where DrugType_Code='15' and DrugCode <> '-1'
  
  '''
    
    s_dwh = 'BI_Dev'
    
    cnxn = f_get_connection(s_dwh)
    df = pd.read_sql(s_query, cnxn)
    
    #df=df.sort_values(by='ExecutionDtTm')###orli
    #df=df.drop_duplicates(subset="CaseNum")###orli
    
    
    
    
    return df

#temp
#df_pop=pd.read_pickle("C:/Users/orlyk/redisissions/project/preprocessed/population/population_for_model/df_basic_data_short.pkl")
#l_casenum=df_pop.CaseNum.unique()

def f_get_meds_dis_pop(l_casenum=[]):
    df = f_get_meds_dis_full()

    if len(l_casenum) > 0:
        df = df[df['CaseNum'].isin(l_casenum)]
        df.to_pickle(global_path_processes_file_pop)
    return df
