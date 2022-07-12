# imports
import pyodbc
import pandas as pd
import datetime as dt
import warnings
import os
from f_demographics_rev import *
from f_vital_signs import *
from f_diagnoses_2 import *
from f_HS import *
from vital_signs_namer import *
from f_blood_count import *
from f_blood_chem import *
from f_ventilation_ICU import *
from f_mech_vent_chameleon import *
from f_oxygen_chameleon import *
from f_CCI import *
from f_blood_coagulation import *
from f_microbiology import *
from f_surgery import *
from f_ishpuzim import *
from f_diagnoses_bg import *
from f_norton import *
#from f_must_temp import *
from f_procedures_specs import *
from f_medication_hosp import * 
from f_medication_adm import *
from f_medication_dis import *



IS_RUN_RESEARCH_POPULATION=False
IS_RUN_DEMOGRAPHICS=False
IS_RUN_VITALS=False
IS_RUN_VITALS_NAMER=False 
IS_RUN_DIAGNOSES=False
IS_RUN_BLOOD_COUNT=False
IS_RUN_BLOOD_CHEM=False
IS_RUN_VENTILATION_ICU=False
IS_RUN_MECH_VENTILATION_CHAMELEON=False
IS_RUN_OXYGEN_CHAMELEON=False
IS_RUN_CCI=False
IS_RUN_BLOOD_COAGULATION=False
IS_RUN_MICROBIOLOGY=False
IS_RUN_SURGERY=False
IS_RUN_ISHPUZIM=False 
IS_RUN_DIAGNOSES_BG=False
IS_RUN_NORTON=False
IS_RUN_PROCEDURES=False
IS_RUN_MEDS_HOSP=False
IS_RUN_MEDS_ADM=False
IS_RUN_MEDS_DIS=False
IS_RUN_HS=True


global output_path
output_path="O:/OrlI/readmissions/preprocessed/population/covid/"


def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn


def f_remove_rows_by_param_and_list(s_code_paramm, s_text_param, l_text, df):
    s_cond = ''
    for s_item in l_text:
        s_cond = s_cond + s_text_param + " like '%" + s_item + "%' OR "
    s_cond = s_cond[:-4]
    s_column = s_code_paramm
    s_table = 'CLN_Ishpuzim_Indicators'
    s_query = 'SELECT DISTINCT ' + s_column + ' FROM ' + s_table + ' WHERE ' + s_cond
    cnxn_bi_dev = f_get_connection('BI_Dev')
    tmp_df = pd.read_sql(s_query, cnxn_bi_dev)
    l_codes = tmp_df[s_code_paramm].values
    df = df[~df[s_code_paramm].isin(l_codes)]
    return df


def f_remove_canceled_cases(df):
    l_cancel_text = ['ביטול', 'בטול']
    df = f_remove_rows_by_param_and_list('ShihrurMvType', 'ShihrurMvTypeName', l_cancel_text, df)
    return df


def f_remove_departments(df):
    l_exclution_depmts = ['ילדים', 'ילודים', 'פסיכיאטריה', 'יולדות', 'מיילדותי', 'לידה', 'הריון', 'אונקולוגית',
                          'אונקולוגיה', 'אמבולטורי', 'השהיה - ליס', 'המרכז המשולב לאסתטיקה',
                          'אביבים',
  #orli - added departments
                          'שיקום - מחלקה',
                          'השתלת מח עצם - מחלקה',
                          'השתלת מח עצם ב - מחלקה']
   #orli - removed geriatry departments from list , 'גריאטריה', 'גריאטרית'
    df = f_remove_rows_by_param_and_list('MedOrgTreeAdm', 'OrgMedAdmTatYahidaDesc', l_exclution_depmts, df)
    df = f_remove_rows_by_param_and_list('MedOrgTreeDisch', 'OrgMedDischTatYahidaDesc', l_exclution_depmts, df)
    return df


def f_exclude_from_BASE_REF(s_code_param, s_text_param, l_text, flag_like_search, df, s_BASE_REF):
    s_cond = ''
    if flag_like_search == 1:
        for s_item in l_text:
            s_cond = s_cond + s_text_param + " like '%" + s_item + "%' OR "
    elif flag_like_search == 0:
        for s_item in l_text:
            s_cond = s_cond + s_text_param + " = '" + s_item + "' OR "
    s_cond = s_cond[:-4]
    s_column = s_code_param
    s_table = 'CLN_Ishpuzim_Indicators'
    s_query = 'SELECT DISTINCT ' + s_column + ' FROM ' + s_table + ' WHERE ' + s_cond
    cnxn_bi_dev = f_get_connection('BI_Dev')
    tmp_df = pd.read_sql(s_query, cnxn_bi_dev)
    l_codes = tmp_df[s_code_param].values
    df.loc[df[s_code_param].isin(l_codes), s_BASE_REF] = 0
    return df


def f_create_research_population():
    print("run f_create_research_population")
    #s_output_path = "O:/OrlI/readmissions/code/data_extraction/processed/df_readmin_pop.pkl"
    s_output_path = output_path+"df_readmin_pop.pkl"
  

    s_columns = 'CaseNum,\
                CaseType,\
                CaseTypeCode,\
                PatNum,\
                Age,\
                ShihrurMvType,\
                SugShihrurOrgMedFlg,\
                SugMevDesc,\
                MigrantWorkerFlg,\
                EnterDate,\
                ExitDate,\
                SugKnisaDesc,\
                SugKnisaOrgMedFlg,\
                SugShihrurDesc,\
                ShihrurMvTypeName,\
                DeathDate,\
                DeathInIshpuzFlg,\
                OrgMedAdmTatYahidaDesc,\
                MedOrgTreeAdm,\
                ReAdmPlan30DFlg,\
                ReAdm_Hosp_In30DFlg,\
                ReAdm_Hosp_In30D_CaseNum,\
                MedOrgTreeDisch,\
                OrgMedDischTatYahidaDesc,\
                Readm_Urgent_In30DFlg'

    s_table = 'CLN_Ishpuzim_Indicators'
    cnxn_bi_dev = f_get_connection('BI_Dev')
    s_cond = "("

    # Removing "מקרה אמבולטורי" from the data set
    s_cond = s_cond + "CaseTypeCode != 2) AND ("

    # Taking patients that where at least 18 at the admission, removing dummy patients
    s_cond = s_cond + "Age >=18 AND Age < 9999) AND ("

    # Keeping only Israeli citizen and foreign employees
    s_cond = s_cond + "SugMevDesc = 'ישראלי' OR (SugMevDesc = 'זרים' AND MigrantWorkerFlg = 1)) AND ("

    # Keeping data only until the end of July 2019
    #s_cond = s_cond + "year(EnterDate) < 2019 OR (year(EnterDate) = 2019 AND month(EnterDate) <= 7)"
    # s_cond = s_cond + "year(EnterDate) > 2018 AND (year(EnterDate) < 2020)"# AND month(EnterDate) <= 7)"
    s_cond = s_cond + "year(EnterDate) > 2019 "

    s_cond = s_cond + ")"

    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table + ' WHERE ' + s_cond
    df = pd.read_sql(s_query, cnxn_bi_dev)



    # Removing canceled cases
    df = f_remove_canceled_cases(df)

    # Removing non relevant departments  ----------------orli----------
    #df = f_remove_departments(df)

    df['BASE_FLG'] = 1
    df['REF_FLG'] = 1

    # Excluding from base population

    # Removing "מקרה מיון" from the BASE population
    l_er = ['מקרה מיון']
    df = f_exclude_from_BASE_REF('CaseTypeCode', 'CaseType', l_er, 0, df, 'BASE_FLG')
    
     # Unifying the date and time formats
    df['EnterDate'] = df['EnterDate'].astype('datetime64[s]')
    
    
    df["ExitDate"]= pd.to_datetime(df["ExitDate"] , errors = 'coerce')
    df["ExitDate_bool"]=pd.notna(df["ExitDate"])
    df=df[df["ExitDate_bool"]==True]
    
    #df['ExitDate'] = df['ExitDate'].astype('datetime64[s]')
    df['DeathDate'] = df['DeathDate'].astype('datetime64[s]')

    # TODO! check how many electives within 30 days after admission

    # Removing patients that died during hospitalization from the BASE population
    l_dead = ['פטירה', 'התקבל מת', 'הסבה - התקבל מת']
    df = f_exclude_from_BASE_REF('ShihrurMvType', 'ShihrurMvTypeName', l_dead, 0, df, 'BASE_FLG')
    df.loc[(df['DeathDate'] >= df['EnterDate']) & (df['DeathDate'] <= df['ExitDate']), 'BASE_FLG'] = 0
    df.loc[df['DeathInIshpuzFlg'] != 0, 'BASE_FLG'] = 0
    
    #remove death within 30 days after discharge - orli
    
    df["delta_death"]=df['DeathDate']-df['ExitDate']
    df["delta_death"]=df["delta_death"].dt.days
   # df.loc[df['delta_death'] <= 30,'BASE_FLG'] = 0



    # Removing patients that where released to their home from מיון השהייה from BASE population
    # There is no code parameter for this
    l_release = ['שחרור ממיון השהיה הביתה', 'שחרור ממיון הביתה']
    df = f_exclude_from_BASE_REF('SugShihrurOrgMedFlg', 'SugShihrurDesc', l_release, 0, df, 'BASE_FLG')

    # Removing hospitalizations from 2010 & from 07/19 from the BASE population
    #df.loc[(df.EnterDate.dt.year == 2019) & (df.EnterDate.dt.month == 7), 'BASE_FLG'] = 0
    df.loc[(df.EnterDate.dt.year == 2021) & (df.EnterDate.dt.month == 11), 'BASE_FLG'] = 0

    df.loc[df.EnterDate.dt.year == 2010, 'BASE_FLG'] = 0

    # Removing hospitalizations that have a planned readmission within 30 days from the BASE population
    df.loc[df['ReAdmPlan30DFlg'] == 1, 'BASE_FLG'] = 0

    # Excluding the elective hospitalizations from the REF population
    l_elective = ['אשפוז אלקטיבי']
    df = f_exclude_from_BASE_REF('SugKnisaOrgMedFlg', 'SugKnisaDesc', l_elective, 0, df, 'REF_FLG')



    # The year 9999 (default release year for patients still hospitalized is not recognized as a year by datetime
    # Changing it to 2099
    df['year'] = df['ExitDate'].astype(str).str.slice(0,4,1)
    df.loc[df['year'] == '9999','ExitDate'] = '2099-12-31 23:59:59'
    df.drop(columns=['year'])

   

    df = df.sort_values(by=['PatNum', 'EnterDate'])
    df = df.reset_index(drop=True)
    df.to_pickle("./df_readmin_pop.pkl")
    return df


def f_add_labels(df):
    print("run f_add_labels")
    #s_output_path = "O:/OrlI/readmissions/code/data_extraction/processed/df_readmin_with_labels.pkl"
    s_output_path = output_path+"df_readmin_with_labels.pkl"

   

    df['LABEL_HOSP'] = 0
    df['LABEL_JUST_ER'] = 0

    # Getting the PatNums in the BASE population
    l_patnums = df[df['BASE_FLG'] == 1]['PatNum'].unique()
    i_running = 0
    for s_patnum in l_patnums:
        i_running = i_running + 1
        print(s_patnum + " " + str(i_running))
        tmp_df = df[df['PatNum'] == s_patnum]
        tmp_df = tmp_df[['EnterDate', 'ExitDate', 'BASE_FLG', 'REF_FLG', 'CaseTypeCode', 'CaseType']]

        l_tmp_BASE_indexes = tmp_df[tmp_df['BASE_FLG'] == 1].index
        for i_index in range(len(l_tmp_BASE_indexes)):
            index_BASE = l_tmp_BASE_indexes[i_index]
            l_tmp_REF_indexes = tmp_df[tmp_df['REF_FLG'] == 1].index
            l_tmp_REF_indexes = l_tmp_REF_indexes[l_tmp_REF_indexes > index_BASE]
            for index_REF in l_tmp_REF_indexes:
                dt_time_to_readmin = df.loc[index_REF].EnterDate - df.loc[index_BASE].ExitDate
                if dt_time_to_readmin < dt.timedelta(days=0):
                    continue
                if dt_time_to_readmin < dt.timedelta(days=31):
                    if df.loc[index_REF, 'CaseTypeCode'] == '1':
                        df.at[index_BASE, 'LABEL_HOSP']= 1
                    elif df.loc[index_REF, 'CaseTypeCode'] == '3':
                        df.at[index_BASE, 'LABEL_JUST_ER']= 1
                else:
                    break
    df.to_pickle(output_path+"df_readmin_with_labels.pkl")
   
    df_base=df[df['BASE_FLG'] == 1]
    df_base.to_pickle(output_path+"df_readmin_with_labels_base.pkl")
    df_base.to_csv(output_path+"df_readmin_with_labels_base.csv")

    df_slim =df_base[['CaseNum', 'LABEL_HOSP', 'LABEL_JUST_ER']]
    df_slim.to_pickle(output_path+"df_readmin_with_labels_base_slim.pkl")
    df_slim.to_csv(output_path+"df_readmin_with_labels_base_slim.csv")

    return df

def create_covid_pop(df):
    covid_query='''SELECT 
      [CaseNum]
      
     
      ,[CaseType]
    
    
  FROM [BI_Dev].[dbo].[CLN_Covid19_Population]'''
 
  

    cnxn_bi_dev = f_get_connection('BI_Dev')
    covid_df = pd.read_sql(covid_query, cnxn_bi_dev)
    
    df=pd.merge(covid_df,df,on="CaseNum",how="left")
    df=df.drop(columns=["CaseType_y"])
    df=df.rename(columns={"CaseType_x": "CaseType"})
    return df


warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', 500)

# Creating the population for the research
if IS_RUN_RESEARCH_POPULATION:
    df = f_create_research_population()
    #notice that removing certain dept is under comment
    
    df=create_covid_pop(df)
    
    # Adding the labels
    df = f_add_labels(df)

    # After the labels were added - keeping only the BASE population
    df_base = df[df['BASE_FLG'] == 1]

else:
 #   df_base=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\preprocessed\population\df_readmin_with_labels_base_slim.pkl")
    df_base=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\population\covid\df_readmin_with_labels_base.pkl")
    

print("run_data")

#merge with covid population




 
if IS_RUN_DEMOGRAPHICS:
    df_demo=f_get_demo_pop(list(df_base.PatNum.unique()))
    
if IS_RUN_VITALS:
    df_vitals=f_get_vital_signs_pop(list(df_base.CaseNum.unique()))
    
if IS_RUN_VITALS_NAMER:
    df_vitals_namer=f_get_vital_signs_pop_namer(list(df_base.CaseNum.unique()))

if IS_RUN_DIAGNOSES:
    print("run siagnoses")
    df_diagnoses=f_get_diagnoses_pop(list(df_base.CaseNum.unique()))


#df_HS=f_get_HS(list(df_base.CaseNum.unique()))

if IS_RUN_BLOOD_COUNT:
    get_blood_count(list(df_base.CaseNum.unique()),"full")   

if IS_RUN_BLOOD_CHEM:
    get_blood_chem (list(df_base.CaseNum.unique()),"full")   
    

if IS_RUN_VENTILATION_ICU:
    f_get_ventilation_ICU (list(df_base.CaseNum.unique()))   

if IS_RUN_MECH_VENTILATION_CHAMELEON:
    get_mech_vent_chameleon_pop(list(df_base.CaseNum.unique()))    
        
if IS_RUN_OXYGEN_CHAMELEON:
    get_oxygen_chameleon_pop(list(df_base.CaseNum.unique()))   

if IS_RUN_CCI:
    f_get_CCI_pop(list(df_base.CaseNum.unique()))   

if IS_RUN_BLOOD_COAGULATION:
    get_blood_coag(list(df_base.CaseNum.unique()),"full") 
    
if IS_RUN_MICROBIOLOGY:
    get_microbiology(list(df_base.CaseNum.unique())) 
    
if IS_RUN_SURGERY:
    f_get_surgery(list(df_base.CaseNum.unique())) 
    
if IS_RUN_ISHPUZIM:
    f_get_ishpuzim_pop(list(df_base.CaseNum.unique()))  
    
if IS_RUN_DIAGNOSES_BG:
    f_get_diagnoses_bg_pop(list(df_base.CaseNum.unique()))  
   
if IS_RUN_NORTON:
    f_get_norton(list(df_base.CaseNum.unique()))
    
if IS_RUN_PROCEDURES:
    f_get_procedures_specs_pop(list(df_base.CaseNum.unique()))
    
if IS_RUN_MEDS_HOSP:
    f_get_meds_hosp_pop(list(df_base.CaseNum.unique()))
    
if IS_RUN_MEDS_ADM:
    f_get_meds_adm_pop(list(df_base.CaseNum.unique()))
    
if IS_RUN_MEDS_DIS:
    f_get_meds_dis_pop(list(df_base.CaseNum.unique()))
    
if IS_RUN_HS:
    f_get_HS_pop(list(df_base.CaseNum.unique()))    
    
    