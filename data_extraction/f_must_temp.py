# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 12:36:25 2021

@author: orlyk
"""


import pyodbc
import pandas as pd
import os

# global parameters
global global_path_dwh_table
global_path_dwh_table = r"C:\Users\orlyk\readmissions\project\dwh\df_dwh_prd_prd_dim_cases.pkl"

global global_path_processed_file
global_path_processed_file = r"C:\Users\orlyk\readmissions\project\preprocessed\demographics\df_demographics_full.pkl"

global global_path_processes_file_pop
global_path_processes_file_pop = r"C:\Users\orlyk\readmissions\project\preprocessed\must\df_must_pop.pkl"


global global_path_processes_file_pop_csv
global_path_processes_file_pop_csv = r"C:\Users\orlyk\readmissions\project\preprocessed\demographics\demographics_pop_csv.csv"

def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn

def f_create_must_full():
#    s_columns = 'CaseNum,age,SexCode'
#    s_table = 'PRD_DIM_CASES'
#    s_dwh = 'DWH_PRD'
#    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    
    s_query='''SELECT 
     
      [CaseNum]
     
      ,[Test_ID]
      ,[Test_Name]
      ,[Result]
      ,[Answer_Result]
   
      ,[Execution_Time]
     
     
    
  FROM [DWH_PRD].[dbo].[Chameleon_Fact_MedicalCheckup]
  where Test_ID='11434' OR Test_ID='11426' OR Test_ID='11428' OR Test_ID='11436'
  '''
    
    
    
    
    
    cnxn = f_get_connection('DWH_PRD')
    df = pd.read_sql(s_query, cnxn)
    return df
   # df_cases.to_pickle(global_path_dwh_table)



    



def f_get_must_pop(l_casenum=[]):
    df=f_create_must_full()
    

    if len(l_casenum) > 0:
        df = df[df['CaseNum'].isin(l_casenum)]
        df.to_pickle(global_path_processes_file_pop)



















