# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 11:28:50 2020

@author: orlyk
"""



import pyodbc
import pandas as pd
import os

# global parameters
#global global_path_dwh_table
#global_path_dwh_table = r"C:\Users\orlyk\readmissions\project\dwh\df_dwh_CCI.pkl"
#
#global global_path_processed_file
#global_path_processed_file = r"C:\Users\orlyk\readmissions\project\preprocessed\CCI\df_CCI_full.pkl"

global global_path_processes_file_pop
global_path_processes_file_pop = r"O:\OrlI\readmissions\preprocessed\CCI\df_CCI_pop.pkl"


#global global_path_processes_file_pop_csv
#global_path_processes_file_pop_csv = r"C:\Users\orlyk\readmissions\project\preprocessed\CCI\CCI_pop_csv.csv"

# Helper functions
def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn

def f_get_CCI_full():
    s_columns = '''CaseNum,CharlsDiseases,CharlsScore,SPMyocardialinfarction,
     CongestiveHeartFailure,Peripheralvasculardisea,SPCerebrovasculardisea,
     Connectivetissuedisease,Dementia,Chronicpulmonarydisease,Ulcerdisease,
     liverdisease,Diabetes,Hemiplegia,renaldisease,Tumor,Leukemia,Lymphoma'''
    
    
    
    
    s_table = 'CLN_Charlson'
    s_dwh = 'BI_Dev'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection(s_dwh)
    df = pd.read_sql(s_query, cnxn)
    return df
    
    #df_cases.to_pickle(global_path_dwh_table)


#def f_create_CCI_full():
#    df = pd.read_pickle(global_path_dwh_table)
    # Turning SexCode to one-hot encoding
    #df.to_pickle(global_path_processed_file)



def f_get_CCI_pop(l_casenum=[]):
#    
    df = f_get_CCI_full()


    if len(l_casenum) > 0:
       # df = pd.read_pickle(global_path_processed_file)
        df = df[df['CaseNum'].isin(l_casenum)]
        df.to_pickle(global_path_processes_file_pop)
       # df.to_csv(global_path_processes_file_pop_csv)





