# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 13:36:36 2020

@author: orlyk
"""

#todo clean up this script

## imports
import pyodbc
import pandas as pd
import os
from datetime import timedelta
import numpy as np

# global parameters
global global_data_folder_path
global_data_folder_path = "O:/OrlI/readmissions/"

global global_secondary_folder_path # retrospective / prospective###orli
global_secondary_folder_path = ''

global global_path_dwh_medical_records
global_path_dwh_medical_records = global_data_folder_path + "dwh/df_dwh_prd_chameleon_fact_medicalrecords.pkl"

global global_path_dwh_monitoring_parameters
global_path_dwh_monitoring_parameters = global_data_folder_path + "dwh/df_chameleon_mrr_chameleon_mrr_monitoringparameters.pkl"

global global_path_dwh_v_execution
global_path_dwh_v_execution = global_data_folder_path + "dwh/df_chameleon_mrr_chameleon_mrr_v_execution.pkl"

global global_path_dwh_device_monitor
global_path_dwh_device_monitor = global_data_folder_path + "dwh/df_chameleon_mrr_chameleon_mrr_devicemonitor.pkl"

global global_path_dwh_device_monitor_arch
global_path_dwh_device_monitor_arch = global_data_folder_path + "dwh/df_chameleon_mrr_chameleon_mrr_devicemonitorarch.pkl"

global global_path_dwh_mrr_monitor
global_path_dwh_mrr_monitor = global_data_folder_path + "dwh/df_chameleon_mrr_chameleon_mrr_monitor.pkl"

global global_path_dwh_mrr_monitor_arch
global_path_dwh_mrr_monitor_arch = global_data_folder_path + "dwh/df_chameleon_mrr_chameleon_mrr_monitorarch.pkl"

global global_path_dwh_movements
global_path_dwh_movements = global_data_folder_path + "dwh/df_dwh_prd_chameleon_fact_movements_patient.pkl"

global global_path_processed_file_full
global global_path_processes_file_pop
global_path_processes_file_pop="O:/OrlI/readmissions/preprocessed/vital_signs/"


global global_l_ret_years
global_l_ret_years = list(range(2013,2020))

global global_l_param_hr
global_l_param_hr = ['דופק']
global global_l_param_spo2
global_l_param_spo2 = ['סטורציה', 'סטורציה עם חמצן', 'סטורציה באויר חדר']
global global_l_param_rr
global_l_param_rr = ['מספר נשימות', 'מס נשימות למכשיר', 'נשימות', 'קצב נשימה', 'נשימות.', 'קצב נשימות',
                  'קצב נשימה.', 'קצב נשימה,', 'נשימה - קצב לדקה', 'נשימות לדקה', 'מספר נשימות.']
global global_l_param_bp
global_l_param_bp = ['לחץ דם', 'לחץ סיסטולי', 'לחץ דיאסטולי', 'לחץ דם.', 'לחץ דם,']
global global_l_param_temp
global_l_param_temp = ['חום']

#global global_physiological_hr_upper_limit
#global_physiological_hr_upper_limit = 500
#
#global global_physiological_hr_lower_limit#orli
#global_physiological_hr_lower_limit = 25
#
#global global_pyshiological_temperature_upper_limit
#global_pyshiological_temperature_upper_limit = 45
#
#global global_pyshiological_temperature_lower_limit
#global_pyshiological_temperature_lower_limit = 30
#
#global global_pyshiological_blood_pressure_upper_limit
#global_pyshiological_blood_pressure_upper_limit = 300
#
#global global_pyshiological_blood_pressure_lower_limit
#global_pyshiological_blood_pressure_lower_limit = 10

# functions

def f_update_global_parameters():
    global global_path_processed_file_full
   # global_path_processed_file_full = global_data_folder_path + global_secondary_folder_path + "preprocessed/vital_signs/df_vital_signs_full.pkl"
    global_path_processed_file_full = global_data_folder_path + global_secondary_folder_path + "preprocessed/vital_signs/df_vital_signs_full.pkl"

    global global_path_processes_file_pop
    global_path_processes_file_pop="O:/OrlI/readmissions/preprocessed/vital_signs"
    global global_path_processes_file_pop_csv
    global_path_processes_file_pop_csv = global_data_folder_path + global_secondary_folder_path + "preprocessed/vital_signs/df_vital_signs_pop_csv.csv"

    if global_secondary_folder_path == 'prospective':
        global global_l_ret_years
        global_l_ret_years = list(range(2019, 2021))


def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn

def f_get_dwh_prd_chameleon_fact_medicalrecords():
    if os.path.isfile(global_path_dwh_medical_records):
        df = pd.read_pickle(global_path_dwh_medical_records)
        return df
    s_columns = 'CaseNum,Medical_Record'
    s_table = 'Chameleon_Fact_MedicalRecords'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('DWH_PRD')
    df = pd.read_sql(s_query, cnxn)
   # df.to_pickle(global_path_dwh_medical_records)
    return df

def f_get_chameleon_mrr_chameleon_mrr_monitoringparameters():
    if os.path.isfile(global_path_dwh_monitoring_parameters):
        df = pd.read_pickle(global_path_dwh_monitoring_parameters)
        return df
    s_columns = 'Row_ID,Parameter_Name'
    s_table = 'Chameleon_MRR_MonitoringParameters'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('Chameleon_MRR')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_monitoring_parameters)
    return df

def f_get_chameleon_mrr_chameleon_mrr_v_execution():
    if os.path.isfile(global_path_dwh_v_execution):
        df = pd.read_pickle(global_path_dwh_v_execution)
        return df
    s_columns = 'Medical_Record,Parameter,Entry_Date,Result,Delete_Date'
    s_table = 'Chameleon_MRR_V_Execution'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('Chameleon_MRR')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_v_execution)
    return df

def f_get_chameleon_mrr_chameleon_mrr_devicemonitor():
    if os.path.isfile(global_path_dwh_device_monitor):
        df = pd.read_pickle(global_path_dwh_device_monitor)
        return df
    s_columns = 'Medical_Record,Parameter,Entry_Date,Result,Delete_Date'
    s_table = 'Chameleon_MRR_DeviceMonitor'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('Chameleon_MRR')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_device_monitor)
    return df

def f_get_chameleon_mrr_chameleon_mrr_devicemonitorarch():
    if os.path.isfile(global_path_dwh_device_monitor_arch):
        df = pd.read_pickle(global_path_dwh_device_monitor_arch)
        return df
    s_columns = 'Medical_Record,Parameter,Entry_Date,Result,Delete_Date'
    s_table = 'Chameleon_MRR_DeviceMonitorArch'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('Chameleon_MRR')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_device_monitor_arch)
    return df


def f_get_chameleon_mrr_chameleon_mrr_monitor():
    if os.path.isfile(global_path_dwh_mrr_monitor):
        df = pd.read_pickle(global_path_dwh_mrr_monitor)
        return df
    s_columns = 'Medical_Record,Parameter,Entry_Date,Result,Delete_Date'
    s_table = 'Chameleon_MRR_Monitor'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('Chameleon_MRR')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_mrr_monitor)
    return df


def f_get_chameleon_mrr_chameleon_mrr_monitorarch():
    if os.path.isfile(global_path_dwh_mrr_monitor_arch):
        df = pd.read_pickle(global_path_dwh_mrr_monitor_arch)
        return df
    s_columns = 'Medical_Record,Parameter,Entry_Date,Result,Delete_Date'
    s_table = 'Chameleon_MRR_MonitorArch'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('Chameleon_MRR')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_mrr_monitor_arch)
    return df

def f_get_bi_dev_cln_ishpuzim_indicators():
    if os.path.isfile(global_data_folder_path + "dwh/df_bi_dev_cln_ishpuzim_indicators_slim.pkl"):
        df = pd.read_pickle(global_data_folder_path + "dwh/df_bi_dev_cln_ishpuzim_indicators_slim.pkl")
        return df
    s_columns = '*'
    s_table = 'CLN_Ishpuzim_Indicators'
    cnxn = f_get_connection('BI_Dev')
    df_full = pd.DataFrame()
    for i_year in global_l_ret_years:
        s_year = str(i_year)
        if not os.path.isfile(global_data_folder_path  + "dwh/df_bi_dev_cln_ishpuzim_indicators_" + s_year + ".pkl"):
            s_cond = "year(EnterDate) = " + s_year + " AND ExitYearKey != 'Still Hosp.' AND Age < 9999"
            s_query = 'SELECT ' + s_columns + ' FROM ' + s_table + ' WHERE ' + s_cond
            df = pd.read_sql(s_query, cnxn)
            #df.to_pickle(global_data_folder_path + "dwh/df_bi_dev_cln_ishpuzim_indicators_" + s_year + ".pkl")
        df = pd.read_pickle(global_data_folder_path  + "dwh/df_bi_dev_cln_ishpuzim_indicators_" + s_year + ".pkl")
        df['year'] = df['ExitDate'].astype(str).str.slice(0,4,1)
        df = df[df['year'] != '9999']
        df = df[['CaseNum', 'CaseTypeCode', 'PatNum', 'PatID', 'EnterDate', 'ExitDate']]

        df_full = df_full.append(df).dropna(subset=['CaseNum'])
   # df_full.to_pickle(global_data_folder_path + "dwh/df_bi_dev_cln_ishpuzim_indicators_slim.pkl")
    return df_full

def f_get_dwh_prd_chameleon_fact_movements_patient():
    if os.path.isfile(global_path_dwh_movements):
        df = pd.read_pickle(global_path_dwh_movements)
        return df
    s_columns = 'CaseNum,Unit,MvBgDateTime,MvEndDateTime'
    s_table = 'Chameleon_Fact_Movements_Patient'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('DWH_PRD')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_movements)
    return df


def f_get_vital_signs_full():
#    if os.path.isfile(global_path_processed_file_full):
#        df = pd.read_pickle(global_path_processed_file_full)
#        return df

    l_l_params = [global_l_param_hr, global_l_param_spo2, global_l_param_rr, global_l_param_bp, global_l_param_temp]
    l_param_hebrew = []
    for l in l_l_params:
        for s_param in l:
            l_param_hebrew.append(s_param)
    df_param_codes = f_get_chameleon_mrr_chameleon_mrr_monitoringparameters()
    df_param_codes = df_param_codes[df_param_codes['Parameter_Name'].isin(l_param_hebrew)]
    df_param_codes = df_param_codes.rename(index=str, columns={"Row_ID": "Parameter"})

    df_vex = f_get_chameleon_mrr_chameleon_mrr_v_execution()
    df_dm = f_get_chameleon_mrr_chameleon_mrr_devicemonitor()
    df_dma = f_get_chameleon_mrr_chameleon_mrr_devicemonitorarch()
    df_m = f_get_chameleon_mrr_chameleon_mrr_monitor()
    df_ma = f_get_chameleon_mrr_chameleon_mrr_monitorarch()

    df_records = pd.DataFrame()
    l_df = [df_vex, df_dm, df_dma, df_m, df_ma]
    for df in l_df:
        if len(df) > 0:
            df = df[df['Parameter'].isin(df_param_codes.Parameter.unique())]
            df_records = df_records.append(df)

    df_records['Entry_Date'] = df_records['Entry_Date'].astype('datetime64[s]')
    df_records = df_records.drop_duplicates(keep='first')


    # Keeping records without a delete date
    df_deleted_records = df_records.dropna(subset=['Delete_Date'])
    df_records = df_records.drop(index=df_deleted_records.index)
    df_records = df_records.drop(columns=['Delete_Date'])

    # Removing empty results
    df_records = df_records.dropna(subset=['Result'])
    df_records['Result'] = df_records['Result'].replace('NaN', '')
    df_records['Result'] = df_records['Result'].replace(' ', '')
    df_records = df_records[df_records['Result'] != '']

    # Keeping only numeric results
    df_records['Result'] = pd.to_numeric(df_records['Result'], errors='coerce')
    df_records['Result'] = df_records['Result'].replace(np.nan, '-', regex=True)
    df_records = df_records[df_records['Result'] != '-']
    # Changing result from string to float
    df_records['Result'] = df_records['Result'].astype(float)

    # Calculating modolus
    df_records['modulus'] = df_records['Result'] % 1

    # Cleaning data
    # HR - pulse
    l_hr_codes = list(
        df_param_codes[df_param_codes['Parameter_Name'].isin(global_l_param_hr)]['Parameter'].unique())
    df_hr = df_records[df_records['Parameter'].isin(l_hr_codes)]
    df_hr = df_hr[df_hr['modulus'] == 0]
    df_hr['Result'] = df_hr['Result'].astype(int)
   # df_hr = df_hr[df_hr['Result'] <= global_physiological_hr_upper_limit]
    #df_hr = df_hr[df_hr['Result'] >= global_physiological_hr_lower_limit]#orli

    df_hr['eng_param_name'] = 'hr'

    # Saturation
    l_spo2_codes = list(
        df_param_codes[df_param_codes['Parameter_Name'].isin(global_l_param_spo2)]['Parameter'].unique())
    df_spo2 = df_records[df_records['Parameter'].isin(l_spo2_codes)]
    df_spo2 = df_spo2[df_spo2['modulus'] == 0]
    df_spo2['Result'] = df_spo2['Result'].astype(int)
    #df_spo2 = df_spo2[(df_spo2['Result'] <= 100) & (df_spo2['Result'] >= 0)]
    df_spo2['eng_param_name'] = 'spo2'

    # Temperature
    l_temperature_codes = list(
        df_param_codes[df_param_codes['Parameter_Name'].isin(global_l_param_temp)]['Parameter'].unique())
    df_temperature = df_records[df_records['Parameter'].isin(l_temperature_codes)]
   # df_temperature = df_temperature[(df_temperature['Result'] >= global_pyshiological_temperature_lower_limit) \
    #                                & (df_temperature['Result'] <= global_pyshiological_temperature_upper_limit)]
    df_temperature['eng_param_name'] = 'temp'

    # Respiratory rate
    l_rr_codes = list(
        df_param_codes[df_param_codes['Parameter_Name'].isin(global_l_param_rr)]['Parameter'].unique())
    df_rr = df_records[df_records['Parameter'].isin(l_rr_codes)]
    df_rr['Result'] = df_rr['Result'].astype(int)
    df_rr['eng_param_name'] = 'rr'

    # Blood pressure
    l_bp_codes = list(df_param_codes[df_param_codes['Parameter_Name'].isin(global_l_param_bp)]['Parameter'].unique())
    df_blood_pressure = df_records[df_records['Parameter'].isin(l_bp_codes)]
    df_blood_pressure = df_blood_pressure[df_blood_pressure['modulus'] == 0].drop(columns=['modulus'])
    df_blood_pressure['Result'] = df_blood_pressure['Result'].astype(int)
   # df_blood_pressure = df_blood_pressure[
    #    (df_blood_pressure['Result'] >= global_pyshiological_blood_pressure_lower_limit) \
     #   & (df_blood_pressure['Result'] <= global_pyshiological_blood_pressure_upper_limit)]

    df_blood_pressure = df_blood_pressure.merge(df_param_codes, how='left', on='Parameter')
    df_general_bp = df_blood_pressure[df_blood_pressure['Parameter_Name'].str.contains('לחץ דם')]
    df_general_bp = df_general_bp.sort_values(by=['Result'], ascending=False)
    # Handling systolic blood pressure
    df_sbp = df_general_bp.drop_duplicates(['Medical_Record', 'Entry_Date'], keep='first')
    df_sbp = df_sbp.append(df_blood_pressure[df_blood_pressure['Parameter_Name'].str.contains('סיסטולי')])
    df_sbp = df_sbp.drop_duplicates(['Medical_Record', 'Entry_Date', 'Result'], keep='first')
    df_sbp['eng_param_name'] = 'sbp'
    df_sbp = df_sbp.drop(columns=['Parameter_Name'])

    # Handling diastolic blood pressure
    df_dbp = df_general_bp.drop_duplicates(['Medical_Record', 'Entry_Date'], keep='last')
    df_dbp = df_dbp.append(df_blood_pressure[df_blood_pressure['Parameter_Name'].str.contains('דיאסטולי')])
    df_dbp = df_dbp.drop_duplicates(['Medical_Record', 'Entry_Date', 'Result'], keep='first')
    df_dbp['eng_param_name'] = 'dbp'
    df_dbp = df_dbp.drop(columns=['Parameter_Name'])



    # Gathering all vital signs
    df_records = df_hr
    df_records = df_records.append(df_spo2)
    df_records = df_records.append(df_temperature)
    df_records = df_records.append(df_sbp)
    df_records = df_records.append(df_dbp)
    df_records = df_records.append(df_rr)
    del df_hr, df_spo2, df_temperature, df_rr, df_sbp, df_dbp

    df_records['Medical_Record'] = df_records['Medical_Record'].astype(int)
    df_records = df_records.drop(columns=['modulus'])

    df_pop = f_get_dwh_prd_chameleon_fact_medicalrecords()
    df_records = df_records.merge(df_pop, how='inner', on='Medical_Record')
    df_param_codes = f_get_chameleon_mrr_chameleon_mrr_monitoringparameters()
    df_param_codes = df_param_codes.rename(index=str, columns={"Row_ID": "Parameter"})

    df_records = df_records.merge(df_param_codes, how='left', on='Parameter')

    #df_ishpuzim = f_get_bi_dev_cln_ishpuzim_indicators()
    #df_movements = f_get_dwh_prd_chameleon_fact_movements_patient()
    #df_movements['year'] = df_movements['MvEndDateTime'].astype(str).str.slice(0, 4, 1)
    #df_movements_end_rest = df_movements[df_movements['year'] != '9999']
    #df_movements_end_rest = df_movements_end_rest.sort_values(by=['CaseNum', 'MvEndDateTime'])
    #df_movements_end_rest = df_movements_end_rest.drop_duplicates(subset=['CaseNum'], keep='last')
    #df_movements_end_rest = df_movements_end_rest[['CaseNum', 'MvEndDateTime']]
    #df_ishpuzim_end = df_ishpuzim[['CaseNum', 'ExitDate']]
    #df_ishpuzim_end = df_ishpuzim_end.merge(df_movements_end_rest, how='left', on='CaseNum')
    #df_ishpuzim_end = df_ishpuzim_end.fillna('1800-01-01 00:00:00')
    #df_ishpuzim_end['ExitDate'] = pd.to_datetime(df_ishpuzim_end['ExitDate'])
    #df_ishpuzim_end['MvEndDateTime'] = pd.to_datetime(df_ishpuzim_end['MvEndDateTime'])
    #df_ishpuzim_end['diff'] = df_ishpuzim_end.ExitDate - df_ishpuzim_end.MvEndDateTime
    # when diff < 0 (ExitDate is earlier than MvEndDateTime) - taking MvEndDateTime
    #df_ishpuzim_end_neg = df_ishpuzim_end[df_ishpuzim_end['diff'] < timedelta(hours=0)]
    #df_ishpuzim_end_neg['ExitDate'] = df_ishpuzim_end_neg['MvEndDateTime']
    #df_ishpuzim_end_pos = df_ishpuzim_end[df_ishpuzim_end['diff'] >= timedelta(hours=0)]
    #df_ishpuzim_end = df_ishpuzim_end_pos.append(df_ishpuzim_end_neg)
    #df_ishpuzim = df_ishpuzim.drop(columns=['ExitDate'])
    #df_ishpuzim_end = df_ishpuzim_end[['CaseNum', 'ExitDate']]
    #df_ishpuzim = df_ishpuzim.merge(df_ishpuzim_end, how='left', on='CaseNum')
    #del df_movements, df_movements_end_rest, df_ishpuzim_end, df_ishpuzim_end_neg, df_ishpuzim_end_pos

    #df_records = df_records.merge(df_ishpuzim, how='left', on='CaseNum')
    #df_records = df_records.drop(columns=['Medical_Record','CaseTypeCode','PatNum','PatID'])
    #df_records = df_records.rename(index=str,columns={"Entry_Date": "date_time", "EnterDate": "hospitalization_date_time", "ExitDate": "release_date_time"})
    #df_records.to_pickle(global_path_processed_file_full)
    
    df_records=df_records.rename(index=str,columns={"Entry_Date": "date_time"})
    return df_records


def f_get_vital_signs_pop(l_casenum=[], s_secondary_folder_path=[]):
    # updating global parameters
#    if len(s_secondary_folder_path) > 0:
#        global global_secondary_folder_path
#        global_secondary_folder_path = s_secondary_folder_path
#    f_update_global_parameters()
#
#    if os.path.isfile(global_path_processes_file_pop):
#        df = pd.read_pickle(global_path_processes_file_pop)
#        return df
    df = f_get_vital_signs_full()
    if len(l_casenum) > 0:
        df = df[df['CaseNum'].isin(l_casenum)]
        df["source"]="chameleon"
        df=df[["CaseNum","eng_param_name","date_time","Result","source"]]
        #df.to_pickle(global_path_processes_file_pop+"df_vital_signs_pop.pkl")

        df.to_pickle(global_path_processes_file_pop+"df_vital_signs_pop.pkl")
       # df.to_pickle(global_path_processes_file_pop_csv)

    return df
