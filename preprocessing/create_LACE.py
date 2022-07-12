# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 17:06:36 2022

@author: orlyk
"""

import pandas as pd
import numpy as np


df=pd.read_pickle(r'O:\OrlI\readmissions\preprocessed\model_input\internal_with_dummies_with_count.pkl')

df_er=pd.read_pickle(r'O:\OrlI\readmissions\preprocessed\adm_previous_year\ER_past_6_mo_base.pkl')


#df=df[["CaseNum","LOS","entry_type_ED2hosp","CCI_CharlsScore",'LABEL_HOSP','EnterDate']]
df=pd.merge(df, df_er,on="CaseNum", how="left")

#LOS

df["LOS_cat"]=np.where(df["LOS"]>=4,4,df["LOS"])
df["LOS_cat"]=np.where(df["LOS"]>=7,5,df["LOS_cat"])
df["LOS_cat"]=np.where(df["LOS"]>=14,7,df["LOS_cat"])


df["entry_cat"]=np.where(df["entry_type_ED2hosp"]==1,3,df["entry_type_ED2hosp"])


df["CCI_cat"]=np.where(df["CCI_CharlsScore"]>=4,5,df["CCI_CharlsScore"])

df["ER_6"]=np.where(df["ER_6"]>=4,4,df["ER_6"])

df["LACE"]=df["LOS_cat"]+df["entry_cat"]+df["CCI_cat"]+df["ER_6"]

df=df[["CaseNum","LACE",'LABEL_HOSP','EnterDate','ExitDate','enter_month','discharge_month','log_LOS','LABEL_JUST_ER',
       'PatNum']]

df.to_pickle(r'O:\OrlI\readmissions\preprocessed\model_input\LACE.pkl')


