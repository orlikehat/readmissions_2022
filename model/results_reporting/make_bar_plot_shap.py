# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 12:12:24 2021

@author: orlyk
"""

import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt





#for cv:
path="O:/OrlI/readmissions/report/final_models/xgb_with_counts/SHAP"
df1=pd.read_csv(path+'/SHAP_importance_list0.csv')
df1=df1.rename(columns={"shap_importance":"shap1"})
df2=pd.read_csv(path+'/SHAP_importance_list1.csv')
df2=df2.rename(columns={"shap_importance":"shap2"})
df3=pd.read_csv(path+'/SHAP_importance_list2.csv')
df3=df3.rename(columns={"shap_importance":"shap3"})
df4=pd.read_csv(path+'/SHAP_importance_list3.csv')
df4=df4.rename(columns={"shap_importance":"shap4"})
df5=pd.read_csv(path+'/SHAP_importance_list4.csv')
df5=df5.rename(columns={"shap_importance":"shap5"})


df=pd.merge(df1,df2,on="column_name")
df=pd.merge(df,df3,on="column_name")
df=pd.merge(df,df4,on="column_name")
df=pd.merge(df,df5,on="column_name")

df["ave"]=df.mean(axis=1)
df["ave_abs"]=df["ave"].abs()
df=df.sort_values(by="ave_abs", ascending=False)

df_plot=df.head(25)
df_plot=df_plot.iloc[:, 0:6]

df_plot=pd.melt(df_plot, id_vars=['column_name'], value_vars=["shap1",
                "shap2","shap3",
                "shap4","shap5"])





#df_plot=df_plot[["column_name","ave"]]
df_plot=df_plot.set_index("column_name")

df_plot=df_plot.rename(index={"PREV_hosp_past_year": "previous visits in last year",
                 "VS_result_last_HR": "last HR recorded",
                 "NORT_NRTN_Physical_state": "Norton physical state",
                 "LABS_hgb_result_first":"first hemoglobin",
                 "LABS_HCT_last_result_normed":"last HCT/first HCT",
                 "LABS_neutro_abs_result_last":"last neutrophiles count",
                 "LABS_albumin_result_min":"minimum albumin",
                 "LABS_BUN_result_last":"last BUN",
                 "LABS_albumin_result_last":"last albumin",
                 "DIAG_BG_NMental and behavioural disorders":"background mental and behavioral disorders",
                 "LABS_neutro_perc_result_last":"last neutrophiles perc",
                 "LABS_neutro_perc_result_max":"max neutrophiles perc",
                 "LABS_lymphocytes_perc_result_last":" last lymphocytes perc",
                 "LABS_ptt_last_result_normed":"last ptt/first ptt",
                 "LABS_bilirubin_result_last":"last bilirubin",
                 "LABS_LD_result_last":"last LD",
                 'entry_type_elective':	'enrty type: elective',
                 'ISHP_FirstVisitFlg':	'first visit',
                 'LABS_RDW_result_min':	'minimum RWD',
                 'COUNT_MEDS_DIS_meds_count_disch':	'medication at discharge count',
                 'VS_result_max_sys_BP':	'maximum systolic BP',
                 'HS_ActiveCancer':	'background diagnosis: cancer',
                 'family_stat_single':	'family status: single',
                 'LABS_platetelet_min_result_normed':'minimum platelet/first platelet',
                 'CCI_bg_cci_Chronicpulmonarydisease':	'background diagnosis:pulmonary',
                 'HS_Sodium_under135':	'minimum sodium',
                 'LABS_neutro_abs_result_max':	'maximum neutrophiles count',
                'previous visits in last year':	'previous visits in last year',
'LABS_RDW_result_max':	'maximum RDW',
'LABS_hgb_result_min':	'minimum hemoglobin',
'NORT_NRTN_Score_wo_Comorbidity':	'Norton score',
'CCI_CharlsDiseases':	'Charlson Comorbidity Index',
'LABS_BUN_result_max':	'maximum BUN ',
'minimum albumin':	'minimum albumin',
'last albumin':	'last albumin',
' last lymphocytes perc':	'last lymphocytes perc',
'LABS_RDW_result_last':	'last RDW',
'LABS_HCT_result_min':	'minimum HTC',
'NORT_NRTN_Activity':	'Norton: activity evaluation',
'first visit':	'first visit',
'LABS_acr_2':	'albumin to creatinine ratio1',
'LABS_chloride_result_last':	'chloride last result',
'last neutrophiles perc':	'last neutrophiles perc',
'LOS':	'LOS',
'LABS_RDW_result_first':	'first RDW',
'LABS_chloride_result_min':	'last RDW',
'LABS_hgb_result_last':	'last hemoglobin',
'age':	'age',
'NORT_NRTN_Mobility':	'Norton: mobility evaluation',
'ISHP_ServCnt':	'number of services',
'enrty type: elective':	'enrty type: elective',
'LABS_acr_1':	'albumin to creatinine ratio1',

})
                 
                 
                 



df_plot['column_name'] = df_plot.index

plt.figure(figsize=(7, 7))
sns.barplot(x="value", y="column_name", data=df_plot,color="steelblue")

plt.savefig(r'O:\OrlI\readmissions\report\figures\shap_xgb.png',bbox_inches='tight') 
