# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 11:28:50 2020

@author: orlyk
"""



import pyodbc
import pandas as pd
import os

# global parameters
global global_path_dwh_table
global_path_dwh_table = r"O:\OrlI\readmissions\project\dwh\df_dwh_norton.pkl"

global global_path_processed_file
global_path_processed_file = r"O:\OrlI\readmissions\preprocessed\norton\df_norton.pkl"

global global_path_processes_file_pop
global_path_processes_file_pop = r"O:\OrlI\readmissions\preprocessed\norton\df_norton_pop.pkl"


#global global_path_processes_file_pop_csv
#global_path_processes_file_pop_csv = r"C:\Users\orlyk\readmissions\project\preprocessed\norton\norton_csv.csv"

# Helper functions
def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn

def f_create_norton_cases():
    s_columns = '''CaseNum, NRTN_Mental_State
      ,NRTN_Physical_state
      ,NRTN_Activity
      ,NRTN_Mobility
      ,NRTN_Feces_control
      ,NRTN_Score
      ,NRTN_Score_wo_Comorbidity'''
    
    
    
    
    s_table = 'CLN_Norton'
    s_dwh = 'BI_Dev'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection(s_dwh)
    df_cases = pd.read_sql(s_query, cnxn)
    #df_cases.to_pickle(global_path_dwh_table)
    return df_cases

#def f_create_norton_full():
#    #df = pd.read_pickle(global_path_dwh_table)
#    # Turning SexCode to one-hot encoding
#    df.to_pickle(global_path_processed_file)



def f_get_norton(l_casenum=[]):
    #if os.path.isfile(global_path_processes_file_pop):
   #     return

    #if not os.path.isfile(global_path_dwh_table):
     #   df = f_create_norton_cases()

    #if not os.path.isfile(global_path_processed_file):
    df=f_create_norton_cases()

    if len(l_casenum) > 0:
        #df = pd.read_pickle(global_path_processed_file)
        df = df[df['CaseNum'].isin(l_casenum)]
        df.to_pickle(global_path_processes_file_pop)
        #df.to_csv(global_path_processes_file_pop_csv)





