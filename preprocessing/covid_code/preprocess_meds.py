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


def f_preprocess_meds(x):
    if x=="HOSP":
        df_meds=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\medications\df_meds_hosp_pop_covid.pkl")
    elif x=="ADM":
        df_meds=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\medications\df_meds_adm_pop_covid.pkl")
    else: 
        print("define which medications - ADM or HOSP" )

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
    
    df=pd.merge(df,df_meds,on="CaseNum",how="right")
    
    
    df_med_codes = pd.read_excel(r'O:\OrlI\readmissions\code\support_files\medication_codes.xlsx')
    #df_med_codes=df_med_codes.drop_duplicates(subset="medication_upper")
    df_med_codes_ACT1=df_med_codes[["medication_upper","Anatomical main group (ATC1)"]]
    df_med_codes_ACT1=df_med_codes_ACT1.drop_duplicates(subset="medication_upper")
    df_med_codes_ACT2=df_med_codes[["medication_upper","Therapeutic main group (ATC2)"]]
    df_med_codes_ACT2=df_med_codes_ACT2.drop_duplicates(subset="medication_upper")

      

    df1=pd.merge(df,df_med_codes_ACT1,how="left",left_on="DrugName",right_on="medication_upper")    
    df2=pd.merge(df,df_med_codes_ACT2,how="left",left_on="DrugName",right_on="medication_upper")    

    
    
    df_ATC1=pivot_meds(df1,'Anatomical main group (ATC1)')
    for col in df_ATC1.columns:
        if col !='CaseNum':
            df_ATC1[col]=np.where(df_ATC1[col]>0,1,0)
    df_ATC1['Total_ATC1']= df_ATC1.sum(axis=1)
            
    df_ATC2=pivot_meds(df2,'Therapeutic main group (ATC2)')
    for col in df_ATC2.columns:
        if col !='CaseNum':
            df_ATC2[col]=np.where(df_ATC2[col]>0,1,0)
    df_ATC2['Total_ATC2']= df_ATC2.sum(axis=1)       
   
    
    
   
    df_ATC1.to_pickle(output_path+x+"_ATC1_covid.pkl")
    
    df_ATC2.to_pickle(output_path+x+"_ATC2_covid.pkl")
    
    
    return df_ATC1
    

