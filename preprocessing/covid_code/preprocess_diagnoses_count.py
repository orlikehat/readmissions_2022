# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 15:57:44 2021

@author: orlyk
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 12:31:38 2020

@author: orlyk
"""

import pandas as pd
import numpy as np


def f_preprocess_diagnoses_count():
    
    df=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\population\covid\df_readmin_with_labels_base.pkl")
    output_path="O:/OrlI/readmissions/preprocessed/diagnoses/diagnoses_for_model/"
    
    df_diag=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\diagnoses\df_diagnoses_pop_covid.pkl")

    #df_diag=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\dwh\df_dwh_prd_prd_fact_diagnosis.pkl")
   
    df=df[df["BASE_FLG"]==1]
    df=df["CaseNum"]
    df=pd.merge(df,df_diag,on="CaseNum",how="left")
    df=df.dropna(subset=["Diag_Type_Code"])
    df_disch=df[df["Diag_Type_Code"]==4]
    df_adm=df[df["Diag_Type_Code"]==2]
    df_bg=df[df["Diag_Type_Code"]==1]

    
    #count number of casenums each appears
    df_disch_count=df_disch.groupby(by="CaseNum").count().reset_index()
    df_adm_count=df_adm.groupby(by="CaseNum").count().reset_index()
    df_bg_count=df_bg.groupby(by="CaseNum").count().reset_index()

    
    df_disch_count=df_disch_count[["CaseNum","date_time"]]
    df_adm_count=df_adm_count[["CaseNum","date_time"]]
    df_bg_count=df_bg_count[["CaseNum","date_time"]]
    
    df_disch_count=df_disch_count.rename(columns={"date_time":"diag_count_disch"})
    df_adm_count=df_adm_count.rename(columns={"date_time":"diag_count_adm"})
    df_bg_count=df_bg_count.rename(columns={"date_time":"diag_count_bg"})

    df_disch_count.to_pickle(r'O:\OrlI\readmissions\preprocessed\diagnoses\diagnoses_for_model\diagnoses_count_disch_covid.pkl')
    df_adm_count.to_pickle(r'O:\OrlI\readmissions\preprocessed\diagnoses\diagnoses_for_model\diagnoses_count_adm_covid.pkl')
    df_bg_count.to_pickle(r'O:\OrlI\readmissions\preprocessed\diagnoses\diagnoses_for_model\diagnoses_count_bg_covid.pkl')
    return df_disch_count,df_adm_count,df_bg_count
    
    
    
    
    #df_disch["N"]=1
    #    
    #        
    #diag_table = pd.pivot_table(df_disch, values=['N'], index="CaseNum",columns=['Block'], aggfunc=np.sum, fill_value=0)    
    ##diag_table=diag_table.drop_duplicates()
    #diag_table = diag_table.reset_index()
    #diag_table.columns = list(map("".join, diag_table.columns)
    #)
    #
    #
    #
    ##df["DiagCode_ICD9"]=df["DiagCode_ICD9"].astype('str')
    ##
    ##df["DiagCode_ICD9"] =df["DiagCode_ICD9"].str.lstrip('0') 
    ##
    ##df_ICD["icd9code"]=df_ICD["icd9code"].astype('str')
    #df["DiagCode_ICD9"] =df["DiagCode_ICD9"].str.lstrip('0') 
    #
    #df["DiagCode_ICD9"]=pd.to_numeric(df["DiagCode_ICD9"],errors="ignore")
    #df_ICD["icd9code"]=pd.to_numeric(df_ICD["icd9code"],errors="ignore")
    #
    #df_m=pd.merge(df,df_ICD,left_on="DiagCode_ICD9",right_on="icd9code",how="left")
    #
    #
    #
    #df_disch=df[df["Diag_Type_Code"]==4]
    #
    
    
    
    
    
    
    #df_icd_cat=pd.read_excel(r"C:\Users\orlyk\readmissions\project\code\support_files\ICD_categorization.xlsx")
    #df = pd.merge(df,df_icd_cat, how='left', left_on='icd9_final',right_on="icd9code")
    #df=df[["CaseNum","Diag_Type_Code","Depth1","Depth2"]]
    #
    #
    #df_discharge=df[df["Diag_Type_Code"]==1]
    #
    #df_discharge["N"]=1
    #    
    #       
    #diag_table = pd.pivot_table(df_discharge, values=['N'], index="CaseNum",columns=['Depth2'], aggfunc=np.sum, fill_value=0)    
    #diag_table=diag_table.drop_duplicates()
    #diag_table = diag_table.reset_index()
    #diag_table.columns = list(map("".join, diag_table.columns))
    #
    ##df=pd.merge(df,diag_table, how="left",on="CaseNum")
    #
    

