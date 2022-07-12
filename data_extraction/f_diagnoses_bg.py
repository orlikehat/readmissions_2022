# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 15:54:53 2021

@author: orlyk
"""

import pandas as pd
import numpy as np
#from get_connection import f_get_connection
from pathlib import Path
import pyodbc

global global_path_processes_file_pop
global_path_processes_file_pop=r"O:\OrlI\readmissions\preprocessed\diagnoses\df_diagnoses_bg_pop.pkl"


def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn



def f_get_bi_dev_cln_dim_diagnosis_icd9():
    s_columns = 'DiagnosisCode,DiagnosisDesc'
    s_table = 'CLN_DIM_Diagnosis_ICD9'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('BI_Dev')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_dim_diagnosis_icd9)
    return df


def f_get_diagnoses_bg_full():
    s_query='''select distinct CaseNum,PatNum,DiagCode_ICD9,Diag_Free_Text,Diag_Type_Code
    from [BI_Dev].[dbo].[v_CLN_Diagnosis_FULL]
    where Diag_Type_Code in (1,99) '''
    cnxn_dwh_prd=f_get_connection('DWH_PRD')
    df=pd.read_sql(s_query, cnxn_dwh_prd)
    
    
     # Replacing nan values  
    df['DiagCode_ICD9'] = df['DiagCode_ICD9'].astype(str)
    df['Diag_Free_Text'] = df['Diag_Free_Text'].astype(str)
    df[['DiagCode_ICD9', 'Diag_Free_Text']] = df[
    ['DiagCode_ICD9', 'Diag_Free_Text']].replace(' ', '')
    df[['DiagCode_ICD9', 'Diag_Free_Text']] = df[
    ['DiagCode_ICD9', 'Diag_Free_Text']].replace('nan', '')
    
    # Removing rows where both code & description are missing
    df = df[(df['DiagCode_ICD9'] != '') | (df['Diag_Free_Text'] != '')]
    
    
     # Handling data without a text (Diag_Free_Text==''), filling missing data from the table cln_dim_diagnosis_icd9
    df_no_text = df[df['Diag_Free_Text'] == ''].drop(columns=['Diag_Free_Text'])
    df = df.drop(index=list(df_no_text.index))
    df_codes = f_get_bi_dev_cln_dim_diagnosis_icd9()
    df_codes = df_codes.rename(index=str, columns={"DiagnosisCode": "DiagCode_ICD9"})
    df_no_text = df_no_text.merge(df_codes, how='left', on='DiagCode_ICD9').rename(index=str, columns={
        "DiagnosisDesc": "Diag_Free_Text"})
        
    #concat df and df_no_text
    df=pd.concat([df,df_no_text])    
    
 #   #import mdclone categories
  #  df_mdclone = pd.read_excel(r'C:\Users\orlyk\readmissions\project\code\support_files\Diagnosis_codes_MDClone_2021.xlsx')
  #  df_mdclone = df_mdclone.rename(index=str, columns={"Code": "Diag_Free_Text"})    
    
  #  df_mdclone=df_mdclone[(df_mdclone['Chapter'] != 'UNSPECIFIED')]
  #  df_mdclone=df_mdclone[(df_mdclone['Chapter'] != 'Not specified')]
    
    
   # # Changing to uppercase in df
   # df['Diag_Free_Text'] = df['Diag_Free_Text'].str.upper()
#    df = df.merge(df_mdclone, how='left', on='Diag_Free_Text')
    return df

def f_get_diagnoses_bg_pop(l_casenum=[]):
    df = f_get_diagnoses_bg_full()

    if len(l_casenum) > 0:
        df = df[df['CaseNum'].isin(l_casenum)]
        df.to_pickle(global_path_processes_file_pop)
    return df







