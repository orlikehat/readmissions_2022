# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 15:00:03 2021

@author: orlyk
"""

import pyodbc
import pandas as pd
import os



global global_path_processes_file_pop
global_path_processes_file_pop = r"O:\OrlI\readmissions\preprocessed\procedures_specs\df_procedures_specs_pop.pkl"


#global global_path_processes_file_pop_csv
#global_path_processes_file_pop_csv = r"C:\Users\orlyk\readmissions\project\preprocessed\procedures_specs\df_procedures_specs_pop.csv"



def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn

def f_get_procedures_specs_full():
    s_fact_query='''SELECT  [ServSqNum]
  ,[CaseNum]
  ,[MvSqNum]
 
  FROM [Surgery DM].[dbo].[FACT_Surgeries]
  '''

    s_factless_query='''SELECT [ServSqNum]
      ,[ProcedureCode]
      ,[NamerProcedureCode]
    
  FROM [Surgery DM].[dbo].[FACTLESS_Procedures_In_Surgery]'''

    cnxn = f_get_connection('DWH_PRD')
    df_fact = pd.read_sql(s_fact_query, cnxn)
    df_factless=pd.read_sql(s_factless_query, cnxn)
    #df_dim=pd.read_sql(s_dim_query, cnxn)
    
    df_fact=pd.merge(df_fact,df_factless,on="ServSqNum", how="left")
    
    #drop procedure code=-99999
    df_fact=df_fact[df_fact["ProcedureCode"]>0]
    df_fact=df_fact[["CaseNum","ProcedureCode"]]
        
    return df_fact

def f_get_procedures_specs_pop(l_casenum=[]):
    df=f_get_procedures_specs_full()
    if len(l_casenum) > 0:
        df = df[df['CaseNum'].isin(l_casenum)]
        df.to_pickle(global_path_processes_file_pop)
        #df.to_csv(global_path_processes_file_pop_csv)





















