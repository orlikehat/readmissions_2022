# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 15:38:22 2021

@author: orlyk
"""


# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import pyodbc




def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn
query='''SELECT  [CaseNum]
    
      ,[PatNum]
  
      ,[EnterDate]
    
  FROM [BI_Dev].[dbo].[CLN_Ishpuzim_Indicators]
  where [CaseTypeCode]=3'''
cnxn_dwh_prd=f_get_connection('DWH_PRD')
df_ER=pd.read_sql(query, cnxn_dwh_prd)  
df_ER["EnterDate"]=pd.to_datetime(df_ER["EnterDate"])

df=pd.read_pickle(r'O:\OrlI\readmissions\preprocessed\population\df_readmin_with_labels_base.pkl')
df=df[["CaseNum","PatNum","EnterDate"]]
cases_pat=df["PatNum"]
df_=pd.concat([df,df_ER])
df_=df_.drop_duplicates()
df_=pd.merge(cases_pat,df_,on="PatNum",how="left")
df_=df_.drop_duplicates()

pat_l=list(df_["PatNum"].unique())
df_["EnterDate"]=pd.to_datetime(df_["EnterDate"])
df_fin=pd.DataFrame()
counter=0
for pat in pat_l:
    counter=counter+1
    df_pat=df_[df_["PatNum"]==pat]
    df_pat=df_pat.reset_index()
    temp_df=pd.DataFrame()
   
    for i in range(len(df_pat)):
        temp_df[i]=(df_pat["EnterDate"]-df_pat["EnterDate"][i]).dt.days
    
    temp_df=np.where(temp_df>=0,0,np.where(temp_df>-183,1,0))
    df_pat["ER_past_6_mo"]=temp_df.sum(axis=0)
    df_fin=df_fin.append(df_pat)
    print(counter)

cases=df["CaseNum"]
df_fin_base=pd.merge(cases,df_fin,on="CaseNum",how="left")   
#df_fin.to_pickle(r"O:\OrlI\readmissions\preprocessed\adm_previous_year\ER_past_6_mo.pkl") 
#df_fin_base.to_pickle(r"O:\OrlI\readmissions\preprocessed\adm_previous_year\ER_past_6_mo_base.pkl") 

df_hosp_6=pd.read_pickle(r'O:\OrlI\readmissions\preprocessed\adm_previous_year\adm_previous_6months.pkl')

df_ER_6=pd.merge(df_fin_base,df_hosp_6,on="CaseNum")
df_ER_6["ER_6"]= df_ER_6["ER_past_6_mo"]+df_ER_6["hosp_past_year"]
df_ER_6=df_ER_6[["CaseNum","ER_6"]]

df_ER_6.to_pickle(r"O:\OrlI\readmissions\preprocessed\adm_previous_year\ER_past_6_mo_base.pkl") 




