# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 10:25:39 2020

@author: orlyk
"""

import pyodbc
import pandas as pd
import os
from datetime import timedelta
import numpy as np

# global parameters
global global_data_folder_path
global_data_folder_path = "O:/OrlI/readmissions/"



global global_path_dwh_VS_namer
global_path_dwh_VS_namer = global_data_folder_path + "dwh/df_vital_signs_namer.pkl" #orli

global global_path_processes_file_pop_csv
#global_path_processes_file_pop_csv = global_data_folder_path +  "preprocessed/vital_signs/df_vital_signs_pop_namer_csv.csv"
global_path_processes_file_pop_csv = global_data_folder_path +  "preprocessed/vital_signs/df_vital_signs_pop_namer_csv.csv"

global global_path_processes_file_pop
#global_path_processes_file_pop = global_data_folder_path  + "preprocessed/vital_signs/df_vital_signs_pop_namer.pkl"
global_path_processes_file_pop = global_data_folder_path  + "preprocessed/vital_signs/df_vital_signs_pop_namer.pkl"




#global global_pyshiological_blood_pressure_upper_limit
#global_pyshiological_blood_pressure_upper_limit = 300
#
#global global_pyshiological_blood_pressure_lower_limit
#global_pyshiological_blood_pressure_lower_limit = 10
#
#global global_physiological_hr_upper_limit
#global_physiological_hr_upper_limit = 500
#
#global global_physiological_hr_lower_limit#orli
#global_physiological_hr_lower_limit = 25
#
#
#global global_physiological_tmp_lower_limit#orli
#global_physiological_tmp_lower_limit = 30
#
#global global_pyshiological_temperature_upper_limit
#global_pyshiological_temperature_upper_limit = 45
#
#global global_pyshiological_saturation_lower_limit
#global_pyshiological_saturation_lower_limit = 40



def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn


#OR [Parameter_Name]='BLOODPRES' OR [Parameter_Name]='PULS'
#    OR [Parameter_Name]='TMP_PR'  OR [Parameter_Name]='TMP_PO

def f_get_CLN_vitals_namer():
    #if os.path.isfile(global_path_dwh_VS_namer):
     #   df = pd.read_pickle(global_path_dwh_VS_namer)
      #  return df
    s_columns = 'CaseNum,Parameter_Name,Monitor_Date,Parameter_FixedValue'
    s_table = '[CLN_Vital_Signals_Namer]'
    s_condition="""where [Parameter_Name]='SATUR'OR [Parameter_Name]='BLOODPRES' OR [Parameter_Name]='PULS'
    OR [Parameter_Name]='TMP_PR'  OR [Parameter_Name]='TMP_PO'"""
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table + s_condition
    cnxn = f_get_connection('BI_Dev')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_VS_namer)
    return df


def f_get_vitals_namer():
    df=f_get_CLN_vitals_namer()
        
    df.rename(
        columns={ "Parameter_FixedValue": "Result", "Monitor_Date": "date_time","Parameter_Name":"eng_param_name"},
        inplace=True)
    
   
    #BP
    df_bloodprs = df[df["eng_param_name"]=="BLOODPRES"]
    df_bloodprs_split = df_bloodprs['Result'].str.split('/', 1, expand=True)
    df_bloodprs = pd.concat([df_bloodprs, df_bloodprs_split], axis=1)
    df_bloodprs.rename(
        columns={0: "sbp", 1: "dbp"},
        inplace=True)
    df_bloodprs["sbp"]=df_bloodprs["sbp"].astype('int64')
    df_bloodprs["dbp"]=df_bloodprs["dbp"].astype('int64')
#    df_bloodprs = df_bloodprs[
#            (df_bloodprs['sbp'] >= global_pyshiological_blood_pressure_lower_limit) \
#            & (df_bloodprs['sbp'] <= global_pyshiological_blood_pressure_upper_limit)]
#    df_bloodprs = df_bloodprs[
#            (df_bloodprs['dbp'] >= global_pyshiological_blood_pressure_lower_limit) \
#            & (df_bloodprs['dbp'] <= global_pyshiological_blood_pressure_upper_limit)]
    
    
    df_bloodprs_sbp=df_bloodprs[['CaseNum', 'eng_param_name', 'date_time','sbp']]
    df_bloodprs_sbp.rename(
        columns={ "sbp": "Result"},
        inplace=True)
    df_bloodprs_sbp["eng_param_name"]="sbp"
    df_bloodprs_dbp=df_bloodprs[['CaseNum', 'eng_param_name', 'date_time','dbp']]
    df_bloodprs_dbp.rename(
        columns={ "dbp": "Result"},
        inplace=True)
    df_bloodprs_dbp["eng_param_name"]="dbp"
    
    #pulse
    df_pulse= df[df["eng_param_name"]=="PULS"]
    df_pulse["Result"]=df_pulse["Result"].astype('int64')
#    df_pulse = df_pulse[
#            (df_pulse['Result'] >= global_physiological_hr_lower_limit) \
#            & (df_pulse['Result'] <= global_physiological_hr_upper_limit)]
    df_pulse["eng_param_name"]="hr"
    
    
    df_satur= df[df["eng_param_name"]=="SATUR"]
    df_satur["Result"]=df_satur["Result"].astype('int64')
#    df_satur = df_satur[
#            (df_satur['Result'] >= global_pyshiological_saturation_lower_limit)]
    
          
    df_satur["eng_param_name"]="spo2"
    
    
    
    
    df_tmp= pd.concat([df[df["eng_param_name"]=="TMP_PO"],df[df["eng_param_name"]=="TMP_PR"]])
    df_tmp["Result"]=df_tmp["Result"].astype('float')
#    df_tmp = df_tmp[
#            (df_tmp['Result'] >= global_physiological_tmp_lower_limit) \
#            & (df_tmp['Result'] <= global_pyshiological_temperature_upper_limit)]
    df_tmp["eng_param_name"]="temp"
    
    df_all=pd.concat([df_bloodprs_sbp,df_bloodprs_dbp,df_pulse,df_satur,df_tmp])
    
    df_all["Result"]=df_all["Result"].astype('float')

    return df_all


def f_get_vital_signs_pop_namer(l_casenum=[]):
    
#    if os.path.isfile(global_path_processes_file_pop):
#        df = pd.read_pickle(global_path_processes_file_pop)
#        return df
    df = f_get_vitals_namer()
    if len(l_casenum) > 0:
        df = df[df['CaseNum'].isin(l_casenum)]
        df["source"]="namer"
        df.to_pickle(global_path_processes_file_pop)
        #df.to_pickle(global_path_processes_file_pop_csv)

    return df


