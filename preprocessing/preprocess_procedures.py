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


def f_preprocess_procedures():

    df=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\population\df_readmin_with_labels_base.pkl")
    output_path="O:/OrlI/readmissions/preprocessed/procedures_specs/procedures_for_model/procedures_preprocessed.pkl"
    
    df_proced=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\procedures_specs\df_procedures_specs_pop.pkl")
    df_procedure_codes=pd.read_excel(r"O:\OrlI\readmissions\code\support_files\ICD_procedures.xlsx")
    df_proced=pd.merge(df_proced,df_procedure_codes, left_on="ProcedureCode",
                       right_on="SKProcedureCode", how="left")    
    def pivot_diagnoses(df,level):
            df["N"]=1
                    
            proced_table = pd.pivot_table(df, values=['N'], index="CaseNum",columns=[level], aggfunc=np.sum, fill_value=0)    
            #proced_table=proced_table.drop_duplicates()
            proced_table = proced_table.reset_index()
            proced_table.columns = list(map("".join, proced_table.columns))
            return proced_table
        
        
    df=df[df["BASE_FLG"]==1]
    df=df[["CaseNum","PatNum","Age","year"]]
    df=pd.merge(df,df_proced,on="CaseNum",how="left")
    df=df[['CaseNum',"class" ]]
    
    df_class=pivot_diagnoses(df,'class')
    for col in df_class.columns:
        if col !='CaseNum':
            df_class[col]=np.where(df_class[col]>0,1,0)
    df_class['procedures_total']= df_class.sum(axis=1)
    
    df_class.to_pickle(output_path)
            
    return df_class       
  
    
    
    
    


