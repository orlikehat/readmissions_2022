

import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


#manually added headings to csv sheet
#feature	  coeffs1	coeffs2	coeffs3	coeffs4	coeffs5


#for cv:
os.chdir(r"O:\OrlI\readmissions\report\final_models\LR_l1_with_counts\coefs")
file = 'coefs_all_iter.csv'
df= pd.read_csv (file)
df["feature"]=df.iloc[:,0]
df["ave"]=df.iloc[:, 1:5].mean(axis=1)
df["ave_abs"]=df["ave"].abs()
df=df.sort_values(by="ave_abs", ascending=False)

df_plot=df.head(25)


df_plot=df_plot.iloc[:, 0:6]

df_plot=pd.melt(df_plot, id_vars=['feature'], value_vars=["coeffs1", "coeffs2","coeffs3",
                                                "coeffs4","coeffs5"])


#df_plot=df_plot[["feature","ave"]]
df_plot=df_plot.set_index("feature")

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
                 'LABS_neutro_abs_result_max':	'maximum neutrophiles count'
})
                 
                 
                 



df_plot['feature'] = df_plot.index


plt.figure(figsize=(7, 7))
sns.barplot(x="value", y="feature", data=df_plot,color="steelblue")

plt.savefig(r'O:\OrlI\readmissions\report\figures\coefs_LR_cv.png',bbox_inches='tight') 

#for full model:
os.chdir(r'O:\OrlI\readmissions\report\results\final models\LR_full_final_compact\coefs')
file = 'coefs_list.csv'
df= pd.read_csv (file)
#df["feature"]=df.iloc[:,0]


df_plot=df.head(20)
df_plot=df_plot[["features","coeffs"]]
df_plot=df_plot.set_index("features")

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
              #   'HS_ActiveCancer':	'background diagnosis: cancer',
                 'family_stat_single':	'family status: single',
                 'LABS_platetelet_min_result_normed':'minimum platelet/first platelet',
                 'CCI_bg_cci_Chronicpulmonarydisease':	'background diagnosis:pulmonary',
                # 'HS_Sodium_under135':	'minimum sodium',
                 'LABS_neutro_abs_result_max':	'maximum neutrophiles count',
                 'NORT_NRTN_Score_wo_Comorbidity':'Norton Score',
                 'NORT_NRTN_Activity':'Norotn - activity',
                 'LABS_RDW_result_first':'first RDW',
                 'LABS_eosinophils_min_result_normed_x':'eosinophils minimum/eosinophils first',
                 'LABS_hgb_result_last':'last hemoglobin',
                 'LABS_hgb_result_min':'minimum hemoglobin',
                 'LABS_chloride_result_last':'last chloride',
                 'LABS_alkaline_phos_result_min':'minimum alkaline phos',
                 'LABS_glucose_result_max':'maximum glucose',
                 'LABS_GGT_result_min':'minimum GGT',
                 'LABS_HCT_result_last':'last HCT',
                 'HS_Sodium_under135':'sodium unde 135',
                 'HS_ActiveCancer':'active cancer'
                 
                 
                 
})
df_plot['abs_coeffs']=df_plot['coeffs'].abs()

df_plot['feature'] = df_plot.index

plt.figure(figsize=(7, 7))
#sns.barplot(x="abs_coeffs", y="feature", data=df_plot,color="steelblue")
sns.barplot(x="coeffs", y="feature", data=df_plot,color="steelblue")
plt.xlabel ('coefficients')
plt.savefig(r'O:\OrlI\readmissions\report\results\tables_and_figures\coefs_internal_compact.png',bbox_inches='tight') 

#---------------------------------------------------------------------------------------------------------------
os.chdir(r'O:\OrlI\readmissions\model_results\for_report\lr_full_model_with_counts\coefs')
file = 'coefs_list.csv'
df= pd.read_csv (file)
#df["feature"]=df.iloc[:,0]


df_plot=df.head(20)
df_plot=df_plot[["features","coeffs"]]
df_plot=df_plot.set_index("features")

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
              #   'HS_ActiveCancer':	'background diagnosis: cancer',
                 'family_stat_single':	'family status: single',
                 'LABS_platetelet_min_result_normed':'minimum platelet/first platelet',
                 'CCI_bg_cci_Chronicpulmonarydisease':	'background diagnosis:pulmonary',
                # 'HS_Sodium_under135':	'minimum sodium',
                 'LABS_neutro_abs_result_max':	'maximum neutrophiles count',
                 'NORT_NRTN_Score_wo_Comorbidity':'Norton Score',
                 'NORT_NRTN_Activity':'Norotn - activity',
                 'LABS_RDW_result_first':'first RDW',
                 'LABS_eosinophils_min_result_normed_x':'eosinophils minimum/eosinophils first',
                 'LABS_hgb_result_last':'last hemoglobin',
                 'LABS_hgb_result_min':'minimum hemoglobin',
                 'LABS_chloride_result_last':'last chloride',
                 'LABS_alkaline_phos_result_min':'minimum alkaline phos',
                 'LABS_glucose_result_max':'maximum glucose',
                 'LABS_GGT_result_min':'minimum GGT',
                 'LABS_HCT_result_last':'last HCT',
                 'HS_Sodium_under135':'sodium unde 135',
                 'HS_ActiveCancer':'active cancer'
                 
                 
                 
})
df_plot['abs_coeffs']=df_plot['coeffs'].abs()

df_plot['feature'] = df_plot.index

plt.figure(figsize=(7, 7))
sns.barplot(x="abs_coeffs", y="feature", data=df_plot,color="steelblue")
plt.xlabel ('coefficients')
plt.savefig(r'O:\OrlI\readmissions\report\figures\coefs_test_internal_manual.png',bbox_inches='tight') 
