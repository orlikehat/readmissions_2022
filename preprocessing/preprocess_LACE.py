# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 20:11:57 2021

@author: orlyk
"""

import pandas as pd
import numpy as np
import pickle5 as pickle
import pickle
from io import StringIO



df=pd.read_pickle(r'O:\OrlI\readmissions\preprocessed\model_input\internal_with_dummies_with_count.pkl')



df=df[["CaseNum","CCI_CharlsDiseases","LOS","entry_type_elective"]]
df["LACE_LOS"]=np.where(df["LOS"]>3, 4,df["LOS"])
df["LACE_LOS"]=np.where(df["LOS"]>6, 5,df["LACE_LOS"])
df["LACE_LOS"]=np.where(df["LOS"]>13, 7,df["LACE_LOS"])

df["LACE_CCI"]=np.where(df["CCI_CharlsDiseases"]>3, 5,df["CCI_CharlsDiseases"])

df["LACE_acute"]=np.where(df["entry_type_elective"]==1,0,3)

df["CaseNum"]=df["CaseNum"].astype(str)


df_prev=pd.read_pickle(r'O:\OrlI\readmissions\preprocessed\adm_previous_year\ER_previous_mon4.pkl')

er_prev=df_prev[["CaseNum","ER_past_6mon"]]
er_prev["ER_past_6mon"]=np.where(er_prev["ER_past_6mon"]>3,4,er_prev["ER_past_6mon"])
er_prev["CaseNum"]=er_prev["CaseNum"].astype(str)

a=er_prev.head(10000)
df.to_csv(r'O:\OrlI\readmissions\preprocessed\adm_previous_year\temp.csv')

df=pd.merge(df,er_prev,how="left",on="CaseNum")

df["LACE"]=df["LACE_LOS"]+df["LACE_CCI"]+df["LACE_acute"]+df["ER_past_6mon"]

a=df.head(10000)
a.to_csv(r'O:\OrlI\readmissions\preprocessed\adm_previous_year\temp.csv')
