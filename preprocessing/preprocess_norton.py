# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 16:00:45 2021

@author: orlyk
"""
import pandas as pd
def f_preprocess_norton():
    df_norton=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\norton\df_norton_pop.pkl")
    #df_norton=df_norton.drop(columns=['NRTN_Physical_Text'])
    
    
    for column  in df_norton.iloc[:,1:]:
        df_norton[column]=pd.to_numeric(df_norton[column])
   
    df_norton=df_norton.sort_values(by=['NRTN_Score'])
    df_norton=df_norton.drop_duplicates(subset=['CaseNum'])
     
    df_norton=df_norton[df_norton["NRTN_Score"]>4] 
    
    
     
  
        
    df_norton.to_pickle(r"O:\OrlI\readmissions\preprocessed\norton\norton_for_model\norton_preprocessed.pkl")    
   # df_norton.to_csv(r"C:\Users\orlyk\readmissions\project\preprocessed\CCI\CCI_for_model\CCI_for_model.csv")    

     
    
    return df_norton