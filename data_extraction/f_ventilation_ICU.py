# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 16:18:55 2020

@author: orlyk
"""

#first occurance of ventilation in ICU
#mechnical ventilation or oxygen support (2 entries per casenum can appear)
#type of ventilation (available for most but not all)



import pyodbc
import pandas as pd
import os
from datetime import timedelta
import numpy as np

# global parameters
global global_data_folder_path
global_data_folder_path = r"O:/OrlI/readmissions/"

global global_path_dwh_mv_param_id
global_path_dwh_mv_param_id = global_data_folder_path + "dwh/df_dwh_mv_icu_src_parameters_id.pkl"


global global_path_dwh_mv_param_text
global_path_dwh_mv_param_text = global_data_folder_path + "dwh/df_dwh_mv_icu_src_parameters_text.pkl"


global global_path_dwh_mv_text_signals
global_path_dwh_mv_text_signals = global_data_folder_path + "dwh/df_dwh_mv_icu_src_text_signals.pkl"

global global_path_dwh_mv_icu_units
global_path_dwh_mv_icu_units = global_data_folder_path + "dwh/df_dwh_mv_icu_src_units.pkl"


global global_path_dwh_mv_icu_nonsequential
global_path_dwh_mv_icu_nonsequential = global_data_folder_path + "dwh/df_dwh_mv_icu_src_nonsequential.pkl"

global global_path_dwh_mv_icu_admissions
global_path_dwh_mv_icu_admissions = global_data_folder_path + "dwh/df_dwh_mv_icu_fact_admissions.pkl"

global global_vent_list
global_vent_list = global_data_folder_path + "code/support_files/vent_list.csv"


global global_path_processed_file_full
global_path_processed_file_full = global_data_folder_path + "processed/df_ventilation_full.pkl"

global global_path_processes_file_pop
global_path_processes_file_pop = global_data_folder_path + "preprocessed/ventilation/ICU/df_ventilation_pop.pkl"

global global_path_processes_file_pop_csv
global_path_processes_file_pop_csv = global_data_folder_path + "preprocessed/ventilation/ICU/df_ventilation_pop.csv"


def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn

def f_get_admissions():
    if os.path.isfile(global_path_dwh_mv_icu_admissions):
        df = pd.read_pickle(global_path_dwh_mv_icu_admissions)
        return df
    s_columns = 'Admission_id,CaseNum'
    s_table = 'ICU_FACT_Admissions'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('DWH_PRD')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_mv_icu_admissions)
    return df



def f_get_text_signals():
    if os.path.isfile(global_path_dwh_mv_text_signals):
        df = pd.read_pickle(global_path_dwh_mv_text_signals)
        return df
    s_columns = 'PatientID,Time,ParameterID,TextID'
    s_table = 'ICU_SRC_TextSignals'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('DWH_SRC')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_mv_text_signals)
    return df

def f_get_icu_params():
    if os.path.isfile(global_path_dwh_mv_param_id):
        df = pd.read_pickle(global_path_dwh_mv_param_id)
        return df
    s_columns = 'ParameterID,ParameterName'
    s_table = 'ICU_SRC_Parameters'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('DWH_SRC')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_mv_param_id)
    return df



def f_get_icu_params_text():
    if os.path.isfile(global_path_dwh_mv_param_text):
        df = pd.read_pickle(global_path_dwh_mv_param_text)
        return df
    s_columns = 'ParameterID,TextID,Text'
    s_table = 'ICU_SRC_ParametersText'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('DWH_SRC')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_mv_param_text)
    return df



def f_get_icu_nonsequential():
     if os.path.isfile(global_path_dwh_mv_icu_nonsequential):
        df = pd.read_pickle(global_path_dwh_mv_icu_nonsequential)
        return df
     s_columns = 'PatientID,ParameterID,Time,Value'
     s_table = 'ICU_SRC_Signals_NonSequential'
     s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
     cnxn = f_get_connection('DWH_SRC')
     df = pd.read_sql(s_query, cnxn)
     #df.to_pickle(global_path_dwh_mv_icu_nonsequential)
     return df
    
    
#def f_get_icu_units():
#      if os.path.isfile(global_path_dwh_mv_icu_units):
#        df = pd.read_pickle(global_path_dwh_mv_icu_units)
#        return df
#      s_columns = 'UnitID,UnitName'
#      s_table = 'ICU_SRC_Units'
#      s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
#      cnxn = f_get_connection('DWH_SRC')
#      df = pd.read_sql(s_query, cnxn)
#      df.to_pickle(global_path_dwh_mv_icu_units)
#      return df
#    
     
    

def f_get_ventilation_full():
    if os.path.isfile(global_path_processed_file_full):
        df = pd.read_pickle(global_path_processed_file_full)
        return df

   
    df_text_signals=f_get_text_signals()
    key_patient=f_get_admissions()
    key_params=f_get_icu_params()
    key_text=f_get_icu_params_text()
    df_non_sequential=f_get_icu_nonsequential()
    #key_units=f_get_icu_units()
    vent_list=pd.read_csv(global_vent_list)
    
         
    #filter for params associated with ventilation 
    
    param_id_vent=['4612','4623','5487','5841','6891','6916','7289','7290','7291','7295','7328','10472','11071','11716']
    key_params["ParameterID"]=key_params["ParameterID"].astype('str')
    mask = key_params.ParameterID.apply(lambda x: any(item for item in param_id_vent if item in x))
    key_params = key_params[mask]
    
    
    text_id_vent=['7290','7291']
    key_text["ParameterID"]=key_text["ParameterID"].astype('str')
    mask = key_text.ParameterID.apply(lambda x: any(item for item in text_id_vent if item in x))
    key_text=key_text[mask]
    
    df_text_signals["ParameterID"]=df_text_signals["ParameterID"].astype('str')
    mask = df_text_signals.ParameterID.apply(lambda x: any(item for item in text_id_vent if item in x))
    df_text_signals=df_text_signals[mask]
         
    param_id_nonseq_vent=['5841','7328']
    df_non_sequential["ParameterID"]=df_non_sequential["ParameterID"].astype('str')
    mask = df_non_sequential.ParameterID.apply(lambda x: any(item for item in param_id_nonseq_vent if item in x))
    df_non_sequential=df_non_sequential[mask]    
        
    #
    #non-sequential table___________________________________________________________
    key_patient=key_patient.drop_duplicates(subset=['Admission_id'])        
    df_non_sequential=pd.merge(df_non_sequential,key_patient, how="left",left_on="PatientID",right_on="Admission_id")
    
    df_non_sequential.dropna(subset=['CaseNum'], inplace=True)
    #keep only first occurance
    df_non_sequential.sort_values(by='Time',ascending=True, inplace=True)
    df_non_sequential=df_non_sequential.drop_duplicates(subset='CaseNum', keep='first')
    
    df_non_sequential=pd.merge(df_non_sequential,key_params, how="left",on="ParameterID")
    df_non_sequential.sort_values(by='Time',ascending=True, inplace=True)
    df_non_sequential=df_non_sequential.drop_duplicates(subset='PatientID', keep='first', inplace=False)
    df_non_sequential["type"]=""  
    df_non_sequential["source"]="NonSequential_MV"
    df_non_sequential["class"]="mech_ventilation"
    df_non_sequential=df_non_sequential[["CaseNum","Admission_id","Time","type","class","source"]]
    
     
    #text signal table__________________________________________________________________
    df_text_signals=pd.merge(df_text_signals,key_patient, how="left",left_on="PatientID",right_on="Admission_id")
    df_text_signals.dropna(subset=['CaseNum'], inplace=True)
    
    df_text_signals=pd.merge(df_text_signals,key_params, how="left",on="ParameterID")
    df_text_signals['ParameterName'] = df_text_signals['ParameterName'].map({'Non _Invesive Device_': "non_invasive", 'Ventilation Mode': "vent_mode","קצב":"rate",'Vent Type':"vent_type"})
    
    #merge with text 
    df_text_signals["param_text"]=df_text_signals["ParameterID"].astype(str)+"_"+df_text_signals["TextID"].astype(str)
    key_text["param_text"]=key_text["ParameterID"].astype(str)+"_"+key_text["TextID"].astype(str)
    df_text_signals=pd.merge(df_text_signals,key_text, how="left",on="param_text")
    df_text_signals["source"]="TextSignals_MV"
    
    #merge with ecxel for better descripption of ventialtion vs support
    df_text_signals=pd.merge(df_text_signals,vent_list, how="left",on="Text")
    df_text_signals.rename(columns={"Text": "type"}, inplace=True)
    
    #mechnical ventilation
    df_text_signals_mech=df_text_signals[df_text_signals["class"]=="mech_ventilation"]
    #first occurance only
    df_text_signals_mech.sort_values(by='Time',ascending=True, inplace=True)
    df_text_signals_mech=df_text_signals_mech.drop_duplicates(subset='CaseNum', keep='first', inplace=False)
    
    
    
    
    #oxygen support
    df_text_signals_support=df_text_signals[df_text_signals["class"]=="support"]
    df_text_signals_support.sort_values(by='Time',ascending=True, inplace=True)
    df_text_signals_support=df_text_signals_support.drop_duplicates(subset='CaseNum', keep='first', inplace=False)
    
    df_text_signals_mech=df_text_signals_mech[["CaseNum","Admission_id","Time","type","class","source"]]
    df_text_signals_support=df_text_signals_support[["CaseNum","Admission_id","Time","type","class","source"]]
    df_text_signals_support["is_ICU"]="ICU"
    #join textsignal mechnical support and non sequential
    df_invasive=pd.concat([df_non_sequential,df_text_signals_mech])
    #keep only one
    df_invasive.sort_values(by='source',ascending=False, inplace=True)
    df_invasive=df_invasive.drop_duplicates(subset='CaseNum', keep='first', inplace=False)
    df_invasive["is_ICU"]="ICU"
    
    #join invasive with non-invasive
    
    df_fin=pd.concat([df_invasive,df_text_signals_support])
    
    #df_fin.to_csv(r"C:\Users\orlyk\readmissions\project\dwh\full_ventilation_ICU.csv")
    return df_fin



def f_get_ventilation_ICU(l_casenum=[]):
   # if os.path.isfile(global_path_processes_file_pop):
   #     df = pd.read_pickle(global_path_processes_file_pop)
    #    return df
    df = f_get_ventilation_full()
    if len(l_casenum) > 0:
        df = df[df['CaseNum'].isin(l_casenum)]
        df.to_pickle(global_path_processes_file_pop)
       # df.to_csv(global_path_processes_file_pop_csv)
       
    return df




#df_pop=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\preprocessed\population\population_for_model\df_basic_data_short.pkl")
##df_pop=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\preprocessed\population\df_readmin_with_labels_base.pkl")#orli
#
#l_casenum=df_pop["CaseNum"]
#
#f_get_ventilation_ICU(l_casenum)
#



