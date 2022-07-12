 # -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 12:29:35 2021

@author: orlyk
"""

import pandas as pd
import numpy as np
#from get_connection import f_get_connection
from pathlib import Path
import pyodbc



global global_path_processes_file_pop
global_path_processes_file_pop = "O:/OrlI/readmissions/preprocessed/ishpuzim_indicators/df_ishpuzim_pop.pkl"
    

def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn

def f_get_ishpuzim_full():
    s_query='''select  CaseNum,PatNum,EnterQuarterDesc,ExitQuarterDesc,
    ExitEndOfWeekFLG,FirstVisitFlg,KupaCode,
    ICU_Count,TransfersCnt,BidudFlg,AcinetobacterFlg,CDTFlg,CREFlg,MRSAFlg,
       VREFlg,ArrivedWithInfFlg,IsAnyInfFlg,MainSurgCnt,SurgProcCnt,HeadCTCnt,AbdCTCnt,DuplexLimbsCnt,
       CTALungCnt,AnyDuplexCnt,ChestXRayCnt,AnyCTCnt,IsMunshamOnLastTransfFlg,
       Aspirin_InDischFlg,Diabetes_Drugs_Flg,Insulin_Drugs_Flg,AntiTrombDrug_onDischFlg,
       Anti_Coagulant_InAdmFlg,Anti_Agregant_InAdmFlg,Coumadin_InAdmFlg,GeneralCultrCnt,
       GeneralCultrPostvCnt,BloodCultrCnt,BloodCultrPostvCnt,UrineCultrCnt,UrineCultrPostvCnt,
       FirstBlood_Sample_2aday_Flg,AMI_Diag,Diabetes_Flg,Anemia_Flg,Renal_Failure_Flg,
       Diagnosis_on_Disch_Flg,CHF_DiagonDisc_Flg,LVS_function_Flg,MainSymptomsInDischFlg,
       SymptomsInDischFlg,UnspesfdFeverInDischFlg,Hypernatremia_DiagOnDisch_Flg,
       Hyponatremia_DiagOnDisch_Flg,Chest_Pain_Main_on_Adm_Flg,Chest_Pain_on_Disch_Flg,DementiaFlg,
       StrokeFlg_OnDisch,BacteremiaFlg,BactEpisodesCnt,Creatinine_more_2_Flg,
       Gloucose_more_200_Flg,Glucose_more_200_Cnt,First_Sodium_Value,INR_In_24Hrs,
       Hemoglobin_lower_10_Cnt,Bacteremia_CVC_Flag,Bacteremia_CVC_Cnt,ServCnt,BirthCountry
       
       from [BI_Dev].[dbo].[CLN_Ishpuzim_Indicators]'''#IsDahufFlg,
       
       
    s_query_country='''select CountryID,EngCountryName,ContinentID  
    from [DWH_PRD].[dbo].[PRD_DIM_Countries]'''
       
       
    cnxn_dwh_prd=f_get_connection('DWH_PRD')
    df=pd.read_sql(s_query, cnxn_dwh_prd)
    df_country=pd.read_sql(s_query_country, cnxn_dwh_prd)
    df_country=df_country.drop_duplicates(subset=['CountryID'])
    df=pd.merge(df,df_country, how="left", left_on="BirthCountry", right_on="CountryID")
    



    return df




#df = df[~df.Result.str.contains("Cancelled")]

def f_get_ishpuzim_pop(l_casenum=[]):    
    df = f_get_ishpuzim_full()

    if len(l_casenum) > 0:
        df = df[df['CaseNum'].isin(l_casenum)]
        df.to_pickle(global_path_processes_file_pop)
    
    
    
    
   
     
