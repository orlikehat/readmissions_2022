# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 18:40:57 2022

@author: orlyk
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 12:57:06 2021

@author: orlyk
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 12:31:38 2020

@author: orlyk
"""

import pandas as pd
import numpy as np


def f_preprocess_meds_psychiatric():
    
    
    df_meds_adm=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\medications\df_meds_adm_pop.pkl")
   
    df_meds_dis=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\medications\df_meds_dis_pop.pkl")

    output_path="O:/OrlI/readmissions/preprocessed/medications/meds_for_model/"

    def pivot_meds(df,level):
            df["N"]=1
                 
            meds_table = pd.pivot_table(df, values=['N'], index="CaseNum",columns=[level], aggfunc=np.sum, fill_value=0)    
            #diag_table=diag_table.drop_duplicates()
            meds_table = meds_table.reset_index()
            meds_table.columns = list(map("".join, meds_table.columns))
            return meds_table

    df=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\population\df_readmin_with_labels_base.pkl")
    df=df[df["BASE_FLG"]==1]
    df=df[["CaseNum","PatNum","Age","year"]]

    #df_meds_hosp=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\preprocessed\medications\df_meds_hosp_pop.pkl")
    
    df_adm=pd.merge(df,df_meds_adm,on="CaseNum",how="right")
    df_dis=pd.merge(df,df_meds_dis,on="CaseNum",how="right")

    
    df_med_codes = pd.read_excel(r'O:\OrlI\readmissions\code\support_files\medication_codes.xlsx')
    #df_med_codes=df_med_codes.drop_duplicates(subset="medication_upper")
    df_med_codes_ACT3=df_med_codes[["medication_upper","Pharmacological subgroup (ATC3)"]]
    df_med_codes_ACT3=df_med_codes_ACT3.drop_duplicates(subset="medication_upper")

    df_adm=pd.merge(df_adm,df_med_codes_ACT3,how="left",left_on="DrugName",right_on="medication_upper")    
    df_dis=pd.merge(df_dis,df_med_codes_ACT3,how="left",left_on="DrugName",right_on="medication_upper")    

    
    
    df_ATC_adm=pivot_meds(df_adm,'Pharmacological subgroup (ATC3)')
    for col in df_ATC_adm.columns:
        if col !='CaseNum':
            df_ATC_adm[col]=np.where(df_ATC_adm[col]>0,1,0)
            

    df_ATC_dis=pivot_meds(df_dis,'Pharmacological subgroup (ATC3)')
    for col in df_ATC_dis.columns:
        if col !='CaseNum':
            df_ATC_dis[col]=np.where(df_ATC_dis[col]>0,1,0)
            
    df_ATC_adm=df_ATC_adm[["CaseNum","Nanti-dementia drugs","Nantidepressants","Npsychostimulants, agents used for adhd and nootropics"]]
    df_ATC_dis=df_ATC_dis[["CaseNum","Nanti-dementia drugs","Nantidepressants","Npsychostimulants, agents used for adhd and nootropics"]]
    df_ATC_adm["psych_meds_adm_total"]=df_ATC_adm.sum(axis=1)   
    df_ATC_dis["psych_meds_adm_total"]=df_ATC_adm.sum(axis=1)   

  
    df_ATC_adm.to_pickle(output_path+"ATC3_adm_psych.pkl")
    df_ATC_dis.to_pickle(output_path+"ATC3_dis_psych.pkl")
    
    
    
    return df_ATC_adm,df_ATC_dis
    

