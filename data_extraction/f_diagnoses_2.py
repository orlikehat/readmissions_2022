import os
import pandas as pd
import pyodbc
from datetime import datetime, timedelta
# global parameters
global global_data_folder_path
global_data_folder_path = r"O:\OrlI\readmissions"


global global_secondary_folder_path # retrospective / prospective
global_secondary_folder_path = r'\preprocessed\diagnoses'#orli

global global_path_dwh_diagnoses
global_path_dwh_diagnoses = global_data_folder_path + "/dwh/df_dwh_prd_prd_fact_diagnosis.pkl"

global global_path_dwh_dim_diagnosis_icd9
global_path_dwh_dim_diagnosis_icd9 = global_data_folder_path + "/dwh/df_bi_dev_cln_dim_diagnosis_icd9.pkl"

global global_path_mdclone_file
global_path_mdclone_file = global_data_folder_path+"/code/support_files/Diagnosis_codes_MDClone.xlsx"

global global_path_dwh_movements
global_path_dwh_movements = global_data_folder_path + "/dwh/df_dwh_prd_chameleon_fact_movements_patient.pkl"

global global_l_ret_years
global_l_ret_years = list(range(2011,2021))

global global_use_mdclone_diagnoses
global_use_mdclone_diagnoses = True

global global_path_processes_file_full
global global_path_processes_file_pop
global_path_processes_file_pop="O:/OrlI/readmissions/preprocessed/diagnoses/"
# functions
# functions

def f_update_global_parameters():
    global global_path_processes_file_full
    global_path_processes_file_full = global_data_folder_path + global_secondary_folder_path + "/df_diagnoses_full.pkl"

    global global_path_processes_file_pop
    global_path_processes_file_pop = global_data_folder_path + global_secondary_folder_path + "/df_diagnoses_pop.pkl"

    if global_secondary_folder_path  ==  'prospective':
        global global_l_ret_years
        global_l_ret_years = list(range(2019, 2021))

def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn

def f_get_bi_dev_cln_ishpuzim_indicators():
    if os.path.isfile(global_data_folder_path + "/dwh/df_bi_dev_cln_ishpuzim_indicators_slim.pkl"):
        df = pd.read_pickle(global_data_folder_path + "/dwh/df_bi_dev_cln_ishpuzim_indicators_slim.pkl")
        return df
    s_columns = '*'
    s_table = 'CLN_Ishpuzim_Indicators'
    cnxn = f_get_connection('BI_Dev')
    df_full = pd.DataFrame()
    for i_year in global_l_ret_years:
        s_year = str(i_year)
        #if not os.path.isfile(global_data_folder_path  + "/dwh/df_bi_dev_cln_ishpuzim_indicators_" + s_year + ".pkl"):
        s_cond = "year(EnterDate) = " + s_year + " AND ExitYearKey != 'Still Hosp.' AND Age < 9999"
        s_query = 'SELECT ' + s_columns + ' FROM ' + s_table + ' WHERE ' + s_cond
        df = pd.read_sql(s_query, cnxn)
            #df.to_pickle(global_data_folder_path + "/dwh/df_bi_dev_cln_ishpuzim_indicators_" + s_year + ".pkl")
        #df = pd.read_pickle(global_data_folder_path  + "/dwh/df_bi_dev_cln_ishpuzim_indicators_" + s_year + ".pkl")
        df['year'] = df['ExitDate'].astype(str).str.slice(0,4,1)
        df = df[df['year'] != '9999']
        df = df[['CaseNum', 'CaseTypeCode', 'PatNum', 'PatID', 'EnterDate', 'ExitDate']]

        df_full = df_full.append(df).dropna(subset=['CaseNum'])
    #df_full.to_pickle(global_data_folder_path + "/dwh/df_bi_dev_cln_ishpuzim_indicators_slim.pkl")
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


def f_get_bi_dev_cln_dim_diagnosis_icd9():
    if os.path.isfile(global_path_dwh_dim_diagnosis_icd9):
        df = pd.read_pickle(global_path_dwh_dim_diagnosis_icd9)
        return df
    s_columns = 'DiagnosisCode,DiagnosisDesc'
    s_table = 'CLN_DIM_Diagnosis_ICD9'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('BI_Dev')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_dim_diagnosis_icd9)
    return df


def f_get_dwh_prd_prd_fact_diagnosis():
    if os.path.isfile(global_path_dwh_diagnoses):
        df = pd.read_pickle(global_path_dwh_diagnoses)
        return df
    s_columns = 'CaseNum,DiagCode_ICD9,Beginning_Date,Original_Date_Entry,Diag_Type_Code,SP,Delete_Date,Diag_Free_Text'
    s_table = 'PRD_FACT_Diagnosis'
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table
    cnxn = f_get_connection('DWH_PRD')
    df = pd.read_sql(s_query, cnxn)
    #df.to_pickle(global_path_dwh_diagnoses)
    return df


def f_get_diagnoses_full():
#    if os.path.isfile(global_path_processes_file_full):
#        df = pd.read_pickle(global_path_processes_file_full)
#        return df
    df_ishpuzim = f_get_bi_dev_cln_ishpuzim_indicators()


    df_movements = f_get_dwh_prd_chameleon_fact_movements_patient()
    df_movements['year'] = df_movements['MvEndDateTime'].astype(str).str.slice(0, 4, 1)
    df_movements_end_rest = df_movements[df_movements['year'] != '9999']
    df_movements_end_rest = df_movements_end_rest.sort_values(by=['CaseNum', 'MvEndDateTime'])
    df_movements_end_rest = df_movements_end_rest.drop_duplicates(subset=['CaseNum'], keep='last')
    df_movements_end_rest = df_movements_end_rest[['CaseNum', 'MvEndDateTime']]
    df_ishpuzim_end = df_ishpuzim[['CaseNum', 'ExitDate']]
    df_ishpuzim_end = df_ishpuzim_end.merge(df_movements_end_rest, how='left', on='CaseNum')
    df_ishpuzim_end = df_ishpuzim_end.fillna('1800-01-01 00:00:00')
    df_ishpuzim_end['ExitDate'] = pd.to_datetime(df_ishpuzim_end['ExitDate'])
    df_ishpuzim_end['MvEndDateTime'] = pd.to_datetime(df_ishpuzim_end['MvEndDateTime'])
    df_ishpuzim_end['diff'] = df_ishpuzim_end.ExitDate - df_ishpuzim_end.MvEndDateTime
    # when diff < 0 (ExitDate is earlier than MvEndDateTime) - taking MvEndDateTime
    df_ishpuzim_end_neg = df_ishpuzim_end[df_ishpuzim_end['diff'] < timedelta(hours=0)]
    df_ishpuzim_end_neg['ExitDate'] = df_ishpuzim_end_neg['MvEndDateTime']
    df_ishpuzim_end_pos = df_ishpuzim_end[df_ishpuzim_end['diff'] >= timedelta(hours=0)]
    df_ishpuzim_end = df_ishpuzim_end_pos.append(df_ishpuzim_end_neg)
    df_ishpuzim = df_ishpuzim.drop(columns=['ExitDate'])
    df_ishpuzim_end = df_ishpuzim_end[['CaseNum', 'ExitDate']]
    df_ishpuzim = df_ishpuzim.merge(df_ishpuzim_end, how='left', on='CaseNum')
    del df_movements, df_movements_end_rest, df_ishpuzim_end, df_ishpuzim_end_neg, df_ishpuzim_end_pos

    df = f_get_dwh_prd_prd_fact_diagnosis()
    df = df.merge(df_ishpuzim, how='left',on='CaseNum').drop(columns=['PatID'])

    # Removing deleted diagnoses
    df_deleted = df.dropna(subset=['Delete_Date'])
    df = df.drop(index=df_deleted.index)
    df = df.drop(columns=['Delete_Date'])

    # Replacing nan values
    df['DiagCode_ICD9'] = df['DiagCode_ICD9'].astype(str)
    df['Diag_Free_Text'] = df['Diag_Free_Text'].astype(str)
    df[['DiagCode_ICD9', 'Diag_Free_Text']] = df[
        ['DiagCode_ICD9', 'Diag_Free_Text']].replace(' ', '')
    df[['DiagCode_ICD9', 'Diag_Free_Text']] = df[
        ['DiagCode_ICD9', 'Diag_Free_Text']].replace('nan', '')

    # Removing rows with status post = 1
    df = df[df['SP'] != 1].drop(columns=['SP'])

    # Removing family diagnoses
    df = df[df['Diag_Type_Code'] != 9]


    # If the diagnosis has a beginning date that is from a different date than the one it was entered at - using the begging date
    df_beginning_date_full = df.dropna(subset=['Beginning_Date'])
    df_beginning_date_full['Original_Date_Entry'] = pd.to_datetime(df_beginning_date_full['Original_Date_Entry'])
    df_beginning_date_full['Beginning_Date'] = pd.to_datetime(df_beginning_date_full['Beginning_Date'])
    df_beginning_date_full['diff'] = df_beginning_date_full['Original_Date_Entry'].dt.date - df_beginning_date_full['Beginning_Date'].dt.date
    df_beginning_date_full = df_beginning_date_full[df_beginning_date_full['diff'] > timedelta(days=0)]
    df = df.drop(index=df_beginning_date_full.index)
    df_beginning_date_full = df_beginning_date_full.rename(index=str, columns={"Beginning_Date": "date_time"}).drop(
        columns=['Original_Date_Entry'])
    # When the diagnosis is death (EX)
    df_dead = df_beginning_date_full[df_beginning_date_full['DiagCode_ICD9'] == 'EX']
    df_beginning_date_full = df_beginning_date_full.drop(index=list(df_dead.index))
    df_dead['date_time'] = df_dead['ExitDate']
    df_beginning_date_full = df_beginning_date_full.append(df_dead)

    df = df.rename(index=str, columns={"Original_Date_Entry": "date_time"})
    df = df.append(df_beginning_date_full)
    del df_beginning_date_full, df_dead

    # Removing rows where both code & description are missing
    df = df[(df['DiagCode_ICD9'] != '') | (df['Diag_Free_Text'] != '')]

    # Handling data without a text (Diag_Free_Text==''), filling missing data from the table cln_dim_diagnosis_icd9
    df_no_text = df[df['Diag_Free_Text'] == ''].drop(columns=['Diag_Free_Text'])
    df = df.drop(index=list(df_no_text.index))
    df_codes = f_get_bi_dev_cln_dim_diagnosis_icd9()
    df_codes = df_codes.rename(index=str, columns={"DiagnosisCode": "DiagCode_ICD9"})
    df_no_text = df_no_text.merge(df_codes, how='left', on='DiagCode_ICD9').rename(index=str, columns={
        "DiagnosisDesc": "Diag_Free_Text"})

    if global_use_mdclone_diagnoses:
        # Using MDCLONE data
        df_mdclone = pd.read_excel(global_path_mdclone_file)
        df_mdclone = df_mdclone.rename(index=str, columns={"Diagnosis": "Diag_Free_Text"})
        # Changing to uppercase in both dfs
        df['Diag_Free_Text'] = df['Diag_Free_Text'].str.upper()
        df_mdclone['Diag_Free_Text'] = df_mdclone['Diag_Free_Text'].str.upper()
        df = df.merge(df_mdclone, how='left', on='Diag_Free_Text')
        df = df.fillna('')

        df['icd9_final'] = ''
        df[['DiagCode_ICD9', 'ICD9 code']] = df[['DiagCode_ICD9', 'ICD9 code']].astype(str)

        # Removing diagnoses without an icd9 code
        df[['DiagCode_ICD9', 'ICD9 code']] = df[['DiagCode_ICD9', 'ICD9 code']].replace(' ', '')
        df[['DiagCode_ICD9', 'ICD9 code']] = df[['DiagCode_ICD9', 'ICD9 code']].replace('UNSPECIFIED', '')
        df = df[(df['DiagCode_ICD9'] != '') & (df['ICD9 code'] != '')]

        # Handling rows with same code in both fields
        df_same_icd9 = df[df['DiagCode_ICD9'] == df['ICD9 code']]
        l_same_icd9_index = list(df_same_icd9.index)
        df.at[l_same_icd9_index, 'icd9_final'] = df['DiagCode_ICD9'][l_same_icd9_index]
        del df_same_icd9

        # Handling differences between "DiagCode_ICD9" (original code) and "ICD9 code" (mdclone match) columns

        # When only one field is not empty
        df_diff_icd9 = df[df['DiagCode_ICD9'] != df['ICD9 code']]
        df_only_one_code1 = df_diff_icd9[(df_diff_icd9['DiagCode_ICD9'] == '') & (df_diff_icd9['ICD9 code'] != '')]
        df_only_one_code2 = df_diff_icd9[(df_diff_icd9['DiagCode_ICD9'] != '') & (df_diff_icd9['ICD9 code'] == '')]
        l_only_one_code1 = list(df_only_one_code1.index)
        l_only_one_code2 = list(df_only_one_code2.index)
        df.at[l_only_one_code1, 'icd9_final'] = df['ICD9 code'][l_only_one_code1]
        df.at[l_only_one_code2, 'icd9_final'] = df['DiagCode_ICD9'][l_only_one_code2]
        df_diff_icd9 = df_diff_icd9.drop(index=l_only_one_code1)
        df_diff_icd9 = df_diff_icd9.drop(index=l_only_one_code2)
        # When both fields are full and different - taking MDCLONE
        l_diff_icd9 = list(df_diff_icd9.index)
        df.at[l_diff_icd9, 'icd9_final'] = df['ICD9 code'][l_diff_icd9]
        df_no_text = df_no_text.rename(index=str, columns={"DiagCode_ICD9": "icd9_final"})

    # Adding the data df_no_text
    df = df.append(df_no_text)
    if not global_use_mdclone_diagnoses:
        df['icd9_final'] = df['DiagCode_ICD9']
    df.date_time = pd.to_datetime(df.date_time)
    df = df.drop(columns=['Beginning_Date','CaseTypeCode','DiagCode_ICD9','ICD9 code','diff','Mapped ICD10 code','Mapped ICD10 description'])

    #df = df.drop(columns=['Beginning_Date','CaseTypeCode','DiagCode_ICD9','ICD9 code','PatNum','diff','Mapped ICD10 code','Mapped ICD10 description'])
    df = df.rename(index=str, columns={"EnterDate": "hospitalization_date_time", "ExitDate": "release_date_time"})

    #df.to_pickle(global_path_processes_file_full)
    return df


def f_get_diagnoses_pop(l_casenum=[], s_secondary_folder_path=[]):
    # updating global parameters
#    if len(s_secondary_folder_path) > 0:
#        global global_secondary_folder_path
#        global_secondary_folder_path = s_secondary_folder_path
#    f_update_global_parameters()
#
#    if os.path.isfile(global_path_processes_file_pop):
#        df = pd.read_pickle(global_path_processes_file_pop)
#        return df
    df = f_get_diagnoses_full()

    if len(l_casenum) > 0:
        df = df[df['CaseNum'].isin(l_casenum)]
        df.to_pickle(global_path_processes_file_pop+"df_diagnoses_pop.pkl")
    return df

