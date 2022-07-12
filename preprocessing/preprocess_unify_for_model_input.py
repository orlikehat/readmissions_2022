# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 12:17:51 2020

@author: orlyk
"""

import pandas as pd
import numpy as np
import pickle5 as pickle


from preprocess_basic_data import f_preprocess_basic_data
from preprocess_diagnoses import f_preprocess_diagnoses
from preprocess_vital_signs import f_preprocess_VS
from preprocess_blood_count import f_preprocess_blood_count
from preprocess_blood_chem import f_preprocess_blood_chem
from preprocess_ventilation import f_preprocess_ventilation
from preprocess_CCI import f_preprocess_CCI
from preprocess_blood_coag import f_preprocess_blood_coag
from preprocess_microbiology import f_preprocess_microbiology
from preprocess_surgery import f_preprocess_surgery
from preprocess_ishpuzim import f_preprocess_ishpuzim
from preprocess_diagnoses_bg import f_preprocess_diagnoses_bg
from preprocess_diagnoses_manual import f_preprocess_diagnoses_manual
from preprocess_norton import f_preprocess_norton
from preprocess_procedures import f_preprocess_procedures
from preprocess_meds import f_preprocess_meds
from preprocess_diagnoses_count import f_preprocess_diagnoses_count
from preprocess_meds_count import f_preprocess_meds_count
from get_specific_depts import get_specific_depts

from utils.get_features_for_eng import get_features
from utils.get_interactions import *
from utils.cont_to_cat import cont_to_cat
from preprocess_meds import f_preprocess_meds
from preprocess_meds_psych import f_preprocess_meds_psychiatric

IS_RUN_POPULATION=True 
IS_RUN_DIAGNOSES=False
IS_RUN_VS=False
IS_RUN_BLOOD_COUNT=False   
IS_RUN_BLOOD_CHEM=False
IS_RUN_BLOOD_COAG=False
IS_RUN_VENTILATION=False
IS_RUN_CCI=False
IS_RUN_MICROBIOLOGY=False
IS_RUN_SURGERY=False
IS_RUN_HOSP_PREV_YEAR=False#super slow so no option of running here
IS_RUN_ISHPUZIM=False
IS_RUN_DIAGNOSES_BG=False
IS_RUN_NORTON=False
IS_RUN_PROCEDURES=False
IS_RUN_MEDS_HOSP=False
IS_RUN_MEDS_ADM=False 
IS_RUN_HS=False
IS_RUN_DIAG_MANUAL=False
IS_RUN_DIAG_COUNT=False
IS_RUN_MEDS_COUNT=False
IS_RUN_MEDS_DIS=False
IS_RUN_MEDS_PSYCH=False

#todo add other hierarchies in diagnoses bg
#IS_OUTLIER_REMOVAL=True
#IS_FEATURE_REMOVAL=True
IS_DUMMIES=True
IS_DIAG_BLOCK_ONLY=False
IS_ADD_AGE_INTERACTION=False
IS_CONT_TO_CAT=False
IS_ADD_CCI_INTERACTION=False
IS_ADD_AGE_SQ_INTERACTION=False


data_folder_path = "O:/OrlI/readmissions/preprocessed/"
output_path="O:/OrlI/readmissions/preprocessed/model_input/"


#population:
if IS_RUN_POPULATION:
    df=f_preprocess_basic_data()
else: 
    df=pd.read_pickle("O:/OrlI/readmissions/preprocessed/population/population_for_model/df_basic_data_short.pkl")

#diagnoses
if IS_RUN_DIAGNOSES:
    df_diag_adm,df_diag_disch=f_preprocess_diagnoses()
else:
    df_diag_adm = pd.read_pickle (data_folder_path+ "diagnoses/diagnoses_for_model/adm_table.pkl")
    df_diag_disch=pd.read_pickle (data_folder_path+ "diagnoses/diagnoses_for_model/disch_table.pkl")

df_diag_adm=df_diag_adm.add_prefix('DIAG_') 
df_diag_adm=df_diag_adm.add_suffix('_adm') 
 
df_diag_disch=df_diag_disch.add_prefix('DIAG_')    
df_diag_disch=df_diag_disch.add_suffix('_dis') 


#vital signs
if IS_RUN_VS:
    df_VS=f_preprocess_VS()
else:
    df_VS=pd.read_pickle (data_folder_path+ "vital_signs/VS_for_model/vs_processed_short.pkl")    

df_VS=df_VS.add_prefix('VS_')    
#blood_count
if IS_RUN_BLOOD_COUNT:
    df_blood_count=f_preprocess_blood_count()
else:
    df_blood_count=pd.read_pickle (data_folder_path+ "labs/blood_count/lab_blood_count_for_model/blood_count_results_only.pkl")

df_blood_count=df_blood_count.add_prefix('LABS_')    
    
if IS_RUN_BLOOD_CHEM:
    df_blood_chem=f_preprocess_blood_chem()
else:
    df_blood_chem=pd.read_pickle (data_folder_path+ "labs/blood_chem/lab_blood_chem_for_model/blood_chem_results_only.pkl")
df_blood_chem=df_blood_chem.add_prefix('LABS_')    

    
if IS_RUN_VENTILATION:
    df_ventilation=f_preprocess_ventilation()
else: 
    df_ventilation=pd.read_pickle(data_folder_path+ "ventilation/ventilation_for_model/ventilation_for_model.pkl")
df_ventilation=df_ventilation.add_prefix('VENT_')    



if IS_RUN_CCI:
    df_CCI=f_preprocess_CCI()
else:
    df_CCI=pd.read_pickle(data_folder_path+ "CCI/CCI_for_model/CCI_for_model.pkl")
df_CCI=df_CCI.add_prefix('CCI_')    


if IS_RUN_BLOOD_COAG:
    df_blood_coag=f_preprocess_blood_coag()
else:
    df_blood_coag=pd.read_pickle(data_folder_path+ "labs/blood_coagulation/blood_coag_for_model/blood_coag_results_only.pkl")
df_blood_coag=df_blood_coag.add_prefix('LABS_')    


if IS_RUN_MICROBIOLOGY:
    df_microbiology=f_preprocess_microbiology()
else:    
    df_microbiology=pd.read_pickle(data_folder_path+ "microbiology/microbiology_for_model/microbiology_preprocessed.pkl")
df_microbiology=df_microbiology.add_prefix('MICRO_BIO_')    

if IS_RUN_SURGERY:
    df_suregry=f_preprocess_surgery()
else:    
    df_suregry=pd.read_pickle(data_folder_path+ "surgery/surgery_for_model/suregry_preprocessed.pkl")
df_suregry=df_suregry.add_prefix('SURGERY_')    
    
if IS_RUN_HOSP_PREV_YEAR:
    print("run HOSP PREV seperately")
else:
    df_prev=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\preprocessed\adm_previous_year\adm_previous_year.pkl")
    df_prev= df_prev.drop(columns=['EnterDate','PatNum','index'])
df_prev=df_prev.add_prefix('PREV_')    

if IS_RUN_ISHPUZIM:
    df_ishpuzim=f_preprocess_ishpuzim()
else:
    df_ishpuzim=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\preprocessed\ishpuzim_indicators\ishpuzim_for_model\ishpuzim_preprocessed.pkl")
df_ishpuzim=df_ishpuzim.add_prefix('ISHP_')  


if IS_RUN_DIAGNOSES_BG:
    df_diagnoses_bg=f_preprocess_diagnoses_bg()
else:
    df_diagnoses_bg=pd.read_pickle(r"C:/Users/orlyk/readmissions/project/preprocessed/diagnoses/diagnoses_for_model/bg_table_chapter19.pkl")
df_diagnoses_bg=df_diagnoses_bg.add_prefix('DIAG_BG_')  

if IS_RUN_NORTON:
    df_norton=f_preprocess_norton()
else:
    df_norton=pd.read_pickle(r"C:/Users/orlyk/readmissions/project/preprocessed/norton/norton_for_model/norton_preprocessed.pkl")
df_norton=df_norton.add_prefix('NORT_') 
    
if IS_RUN_PROCEDURES:
    df_proced=f_preprocess_procedures()
else:
    df_proced=pd.read_pickle(r"C:/Users/orlyk/readmissions/project/preprocessed/procedures_specs/procedures_for_model/procedures_preprocessed.pkl")
df_proced=df_proced.add_prefix('PROCED_') 
    
if IS_RUN_MEDS_HOSP:
    df_meds_hosp=f_preprocess_meds('HOSP')
    
else:
    df_meds_hosp=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\preprocessed\medications\meds_for_model/HOSP_ATC1.pkl")
df_meds_hosp=df_meds_hosp.add_prefix('MEDS_HOSP_') 

    
if IS_RUN_MEDS_ADM:
    df_meds_adm=f_preprocess_meds('ADM')
    
else:
    df_meds_adm=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\preprocessed\medications\meds_for_model/ADM_ATC1.pkl")
df_meds_adm=df_meds_adm.add_prefix('MEDS_ADM_') 



if IS_RUN_MEDS_DIS:
    df_meds_dis=f_preprocess_meds('DIS')
    
else:
    df_meds_dis=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\medications\meds_for_model\DIS_ATC1.pkl")
df_meds_dis=df_meds_dis.add_prefix('MEDS_DIS_') 




if IS_RUN_DIAG_MANUAL:
    df_diag_adm_manual,df_diag_disch_manual,df_diag_bg_manual=f_preprocess_diagnoses_manual()
else:
    df_diag_adm_manual = pd.read_pickle (data_folder_path+ "diagnoses/diagnoses_for_model/adm_table_manual.pkl")
    df_diag_disch_manual=pd.read_pickle (data_folder_path+ "diagnoses/diagnoses_for_model/disch_table_manual.pkl")
    df_diag_bg_manual=pd.read_pickle (data_folder_path+ "diagnoses/diagnoses_for_model/bg_table_manual.pkl")

df_diag_adm_manual=df_diag_adm_manual.add_prefix('MAN_DIAG_adm_') 
 
df_diag_disch_manual=df_diag_disch_manual.add_prefix('MAN_DIAG_dis_')    

df_diag_bg_manual=df_diag_bg_manual.add_prefix('MAN_DIAG_bg_')    


if IS_RUN_DIAG_COUNT:
    df_disch_count,df_adm_count,df_bg_count=f_preprocess_diagnoses_count()
else:
    df_disch_count = pd.read_pickle (data_folder_path+ "diagnoses/diagnoses_for_model/diagnoses_count_disch.pkl")
    df_adm_count=pd.read_pickle (data_folder_path+ "diagnoses/diagnoses_for_model/diagnoses_count_adm.pkl")
    df_bg_count=pd.read_pickle (data_folder_path+ "diagnoses/diagnoses_for_model/diagnoses_count_bg.pkl")

df_disch_count=df_disch_count.add_prefix('COUNT_DIAG_DIS_') 
 
df_adm_count=df_adm_count.add_prefix('COUNT_DIAG_ADM_')    

df_bg_count=df_bg_count.add_prefix('COUNT_DIAG_BG_')    



if IS_RUN_MEDS_COUNT:
    df_meds_disch_count,df_meds_adm_count,df_meds_hosp_count=f_preprocess_meds_count()
else:
    df_meds_disch_count = pd.read_pickle (data_folder_path+ "medications/meds_for_model/meds_count_disch.pkl")
    df_meds_adm_count=pd.read_pickle (data_folder_path+ "medications/meds_for_model/meds_count_adm.pkl")
    df_meds_hosp_count=pd.read_pickle (data_folder_path+ "medications/meds_for_model/meds_count_hosp.pkl")

df_meds_disch_count=df_meds_disch_count.add_prefix('COUNT_MEDS_DIS_') 
 
df_meds_adm_count=df_meds_adm_count.add_prefix('COUNT_MEDS_ADM_')    

df_meds_hosp_count=df_meds_hosp_count.add_prefix('COUNT_MEDS_HOSP_')    



if IS_RUN_MEDS_PSYCH:
    df_meds_adm_psych,df_meds_dis_psych=f_preprocess_meds_psychiatric()
else:
    df_meds_adm_psych = pd.read_pickle (data_folder_path+ "medications/meds_for_model/ATC3_adm_psych.pkl")
    df_meds_dis_psych=pd.read_pickle (data_folder_path+ "medications/meds_for_model/ATC3_dis_psych.pkl")

df_meds_adm_psych=df_meds_adm_psych.add_prefix('MEDS_ADM_PSYCH_') 
 
df_meds_dis_psych=df_meds_dis_psych.add_prefix('MEDS_DIS_PSYCH_')    




df_HS=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\HS\df_HS_pop.pkl")
df_HS=df_HS.add_prefix('HS_') 
    

df_merged=pd.merge(df,df_VS,how="left",right_on="VS_CaseNum",left_on="CaseNum")
#df_merged=pd.merge(df_merged,df_diag_adm,how="left",right_on="DIAG_CaseNum_adm",left_on="CaseNum")
#df_merged=pd.merge(df_merged,df_diag_disch,how="left",right_on="DIAG_CaseNum_dis",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_blood_count,how="left",right_on="LABS_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_blood_chem,how="left",right_on="LABS_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_ventilation,how="left",right_on="VENT_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_CCI,how="left",right_on="CCI_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_blood_coag,how="left",right_on="LABS_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_microbiology,how="left",right_on="MICRO_BIO_CaseNum",left_on="CaseNum")
#df_merged=pd.merge(df_merged,df_suregry,how="left",right_on="SURGERY_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_prev,how="left",right_on="PREV_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_ishpuzim,how="left",right_on="ISHP_CaseNum",left_on="CaseNum")
#df_merged=pd.merge(df_merged,df_diagnoses_bg,how="left",right_on="DIAG_BG_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_norton,how="left",right_on="NORT_CaseNum",left_on="CaseNum")
#df_merged=pd.merge(df_merged,df_proced,how="left",right_on="PROCED_CaseNum",left_on="CaseNum")
#df_merged=pd.merge(df_merged,df_meds_hosp,how="left",right_on="MEDS_HOSP_CaseNum",left_on="CaseNum")
#df_merged=pd.merge(df_merged,df_meds_adm,how="left",right_on="MEDS_ADM_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_diag_adm_manual,how="left",right_on="MAN_DIAG_adm_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_diag_disch_manual,how="left",right_on="MAN_DIAG_dis_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_diag_bg_manual,how="left",right_on="MAN_DIAG_bg_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_HS,how="left",right_on="HS_Casenum",left_on="CaseNum")

df_merged=pd.merge(df_merged,df_disch_count,how="left",right_on="COUNT_DIAG_DIS_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_adm_count,how="left",right_on="COUNT_DIAG_ADM_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_bg_count,how="left",right_on="COUNT_DIAG_BG_CaseNum",left_on="CaseNum")

df_merged=pd.merge(df_merged,df_meds_disch_count,how="left",right_on="COUNT_MEDS_DIS_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_meds_adm_count,how="left",right_on="COUNT_MEDS_ADM_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_meds_hosp_count,how="left",right_on="COUNT_MEDS_HOSP_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_meds_dis,how="left",right_on="MEDS_DIS_CaseNum",left_on="CaseNum")

df_merged=pd.merge(df_merged,df_meds_adm_psych,how="left",right_on="MEDS_ADM_PSYCH_CaseNum",left_on="CaseNum")
df_merged=pd.merge(df_merged,df_meds_dis_psych,how="left",right_on="MEDS_DIS_PSYCH_CaseNum",left_on="CaseNum")

#### find all NANs in MAN and replace with zero 
manual_diag_cols = [col for col in df_merged.columns if 'MAN_DIAG' in col]
if len(manual_diag_cols)>0:    
    df_merged[manual_diag_cols]=np.where(df_merged[manual_diag_cols]==1,1,0)
        



                   

df_merged.drop(columns=['VS_CaseNum', 'LABS_CaseNum_x','LABS_CaseNum_y','LABS_CaseNum',
                        "VENT_CaseNum","CCI_CaseNum","MICRO_BIO_CaseNum","PREV_CaseNum","ISHP_CaseNum",
                        "NORT_CaseNum","NORT_NRTN_Score","HS_Casenum","MAN_DIAG_adm_CaseNum",
                        "MAN_DIAG_dis_CaseNum","MAN_DIAG_bg_CaseNum",
                        "COUNT_DIAG_DIS_CaseNum","COUNT_DIAG_ADM_CaseNum","COUNT_DIAG_BG_CaseNum",
                        "COUNT_MEDS_DIS_CaseNum","COUNT_MEDS_ADM_CaseNum",
                        "COUNT_MEDS_HOSP_CaseNum","MEDS_DIS_CaseNum","MEDS_ADM_PSYCH_CaseNum",
                        "MEDS_DIS_PSYCH_CaseNum"], inplace=True)#"PROCED_CaseNum","MEDS_HOSP_CaseNum","MEDS_ADM_CaseNum",,"SURGERY_CaseNum","DIAG_CaseNum_dis",



if IS_DUMMIES:
    df_merged=pd.get_dummies(data=df_merged, columns=['family_stat','dept_cat_adm', 'dept_cat_disch','entry_type','discharge_type',
                                                      'ISHP_ExitEndOfWeekFLG','ISHP_KupaCode','ISHP_EnterQuarterDesc',
                                                      'ISHP_ExitQuarterDesc','ISHP_ContinentID'])
    #df_merged["MICRO_BIO_category_anaerobe"]=np.where(df_merged["MICRO_BIO_category_anaerobe"]>0,1,0)
    #df_merged["MICRO_BIO_category_candida"]= np.where(df_merged["MICRO_BIO_category_candida"]>0,1,0)
    #df_merged["MICRO_BIO_category_negative"]=np.where(df_merged["MICRO_BIO_category_negative"]>0,1,0)
    #df_merged["MICRO_BIO_category_positive"]=np.where(df_merged["MICRO_BIO_category_positive"]>0,1,0)
    #df_merged["MICRO_BIO_contaminant"]=np.where(df_merged["MICRO_BIO_contaminant"]>0,1,0)
    #df_merged["MICRO_BIO_is_positive_culture"]=np.where(df_merged["MICRO_BIO_is_positive_culture"]>0,1,0)
    
#fill missing with zeros in surgery and microbiology

surgery_cols = [col for col in df_merged.columns if 'SURGERY' in col]
df_merged[surgery_cols]=df_merged[surgery_cols].fillna(0)

microbio_cols = [col for col in df_merged.columns if 'MICRO_BIO' in col]
df_merged[microbio_cols]=df_merged[microbio_cols].fillna(0)
#todo - add procedures?


    
    
#feature engineering:

##age interactions
#df_num_max= df_merged.filter(regex=r'(max)')
#for col in df_num_max:
#    df_num_max[col]=df_num_max[col]*df_merged['age']
#    
# 
#df_num_max=df_num_max.add_suffix('_AGE_interaction')
#   
#df_merged=pd.merge(df_merged,df_num_max,left_on=None, right_on=None, left_index=True, right_index=True)        
#
#df_num_last= df_merged.filter(regex=r'(last)')
#for col in df_num_last:
#    df_num_last[col]=df_num_last[col]*df_merged['age']
#    
# 
#df_num_last=df_num_last.add_suffix('_AGE_interaction')
#   
#df_merged=pd.merge(df_merged,df_num_last,left_on=None, right_on=None, left_index=True, right_index=True)        
#
#normalize to first
#df_num_last= df_merged.filter(regex=r'(last)')
#for col in df_num_last:
#    df_num_last[col]=df_num_max[col]*df_merged['age']
#    
# 
#df_num_max=df_num_max.add_suffix('_AGE_interaction')
#   
#df_merged=pd.merge(df_merged,df_num_max,left_on=None, right_on=None, left_index=True, right_index=True)        
#






#rename feat
#df_merged=df_merged.rename(columns={"DIAG_NBody mass index (BMI)_adm": "Diag_BMI_adm",
#                   "DIAG_NDentofacial anomalies [including malocclusion] and other disorders of jaw_adm": "DIAG_NDentofacial_anomalies_and_other_disorders_of_jaw_adm",
#                   "DIAG_NHuman immunodeficiency virus [HIV] disease_adm":"DIAG_HIV_disease_adm",
#                   "DIAG_NMood [affective] disorders_adm":"DIAG_NMood_disorders_adm",
#                   "DIAG_BG_NBody mass index (BMI)": "Diag_BMI_bg",
#                   "DIAG_BG_NDentofacial anomalies [including malocclusion] and other disorders of jaw": "DIAG_NDentofacial_anomalies_and_other_disorders_of_jaw_bg",
#                   "DIAG_BG_NHuman immunodeficiency virus [HIV] disease":"DIAG_HIV_disease_bg",
#                   "DIAG_BG_NMood [affective] disorders":"DIAG_NMood_disorders_bg",
#                   "CATEGORY_NAcquired pure red cell aplasia [erythroblastopenia]":"CATEGORY_NAcquired pure red cell aplasia erythroblastopenia,
#                   "CATEGORY_NAcute nasopharyngitis [common cold]":"CATEGORY_NAcute nasopharyngitis [common cold]",              
#                   "CATEGORY_NAcute obstructive laryngitis [croup] and epiglottitis":"CATEGORY_NAcute obstructive laryngitis and epiglottitis",
#                   "CATEGORY_NAnogenital herpesviral [herpes simplex] infections":"CATEGORY_NAnogenital herpesviral herpes simplex infections",
#                   "CATEGORY_NAsymptomatic human immunodeficiency virus [HIV] infection status":"CATEGORY_NAsymptomatic human immunodeficiency virus HIV infection status",
#                   "CATEGORY_NBody mass index [BMI]":"CATEGORY_NBody mass index BMI",
#                   "CATEGORY_NChlamydial lymphogranuloma (venereum)":"CATEGORY_NChlamydial lymphogranuloma venereum",
#                   "CATEGORY_NChronic kidney disease (CKD)":"CATEGORY_NChronic kidney disease CKD",
#                   "CATEGORY_NComplications following (induced) termination of pregnancy":"CATEGORY_NComplications following induced termination of pregnancy",
#                   "CATEGORY_NContact with and (suspected) exposure to communicable diseases":"CATEGORY_NContact with and suspected exposure to communicable diseases",
#                   
#                   
#    })


df_merged.columns = df_merged.columns.str.replace('[', ' ').str.replace(']', ' ').str.replace(')', ' ').str.replace('(', ' ')

    
    # "DIAG_NBody mass index (BMI)_dis":"Diag_BMI_dis",
                  # "DIAG_NDentofacial anomalies [including malocclusion] and other disorders of jaw_dis":"DIAG_NDentofacial_anomalies_and_other_disorders_of_jaw_dis",
                  # "DIAG_NHuman immunodeficiency virus [HIV] disease_dis":"DIAG_HIV_disease_dis",
                  # "DIAG_NMood [affective] disorders_dis":"DIAG_NMood_disorders_adm"})


#df_HS=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\preprocessed\HS\df_HS_pop.pkl")
#l_labels=df_pop[["CaseNum","age","LABEL_HOSP"]]
#df_HS=pd.merge(l_labels,df_HS,on="CaseNum",how="left")
                  
                  
if IS_DIAG_BLOCK_ONLY:
    diag_category_cols = [col for col in df_merged.columns if 'DIAG_BG_CATEGORY' in col]
    df_merged=df_merged.drop(columns=[diag_category_cols])
    diag_chapter_cols = [col for col in df_merged.columns if 'DIAG_BG_CHAPTER' in col]
    df_merged=df_merged.drop(columns=[diag_chapter_cols])
    
    
    
df_merged_head=df_merged.head(150)
    
if IS_DUMMIES:
    #df_merged.to_pickle(output_path+"all_with_dummies.pkl")
    #df_merged_head.to_csv(output_path+"all_with_dummies.csv")
    
   # df_internal=df_merged[(df_merged["dept_cat_disch_internal"]==1) | (df_merged["dept_cat_disch_internal_ICU"]==1)]# |(df["dept_cat_disch_geriatrics"]==1)]
    
    df_all=df_merged[(df_merged["dept_cat_disch_internal"]==1) |(df_merged["dept_cat_disch_internal_ICU"]==1) |
            (df_merged["dept_cat_disch_internal_special"]==1) |
            (df_merged["dept_cat_disch_general_ICU"]==1) |
            (df_merged["dept_cat_disch_surgical_special"]==1) |
            (df_merged["dept_cat_disch_surgical_general"]==1) |
            (df_merged["dept_cat_disch_orthopedics"]==1) |
            (df_merged["dept_cat_disch_surgical_ICU"]==1) ]
            
    df_all_head=df_all.head(250)

    
    df_internal=df_merged[(df_merged["dept_cat_disch_internal"]==1) |(df_merged["dept_cat_disch_internal_ICU"]==1)]        
    df_medical=df_merged[(df_merged["dept_cat_disch_internal"]==1) |(df_merged["dept_cat_disch_internal_ICU"]==1) |
            (df_merged["dept_cat_disch_internal_special"]==1) | (df_merged["dept_cat_disch_general_ICU"]==1) ]        
    df_surgical=df_merged[(df_merged["dept_cat_disch_surgical_special"]==1) |(df_merged["dept_cat_disch_surgical_special"]==1) |
            (df_merged["dept_cat_disch_orthopedics"]==1) | 
            (df_merged["dept_cat_disch_surgical_ICU"]==1)] 
    
   
    df_all=df_all.reset_index(drop=True)
    df_internal=df_internal.reset_index(drop=True)
    df_medical=df_medical.reset_index()
    df_surgical=df_surgical.reset_index(drop=True)    
    
    df_neuro,df_cardio,df_dermo,df_uro=get_specific_depts(df_all)
    
    
    HS_cols = [col for col in df_internal.columns if 'HS' in col]
    df_HS_internal= df_internal[HS_cols]
    df_HS_internal=pd.merge(df_HS_internal,df_internal[["CaseNum","EnterDate",
                                                        "LABEL_HOSP",
                                                        "PatNum"]],
                            left_index=True, right_index=True)
    
    df_all.to_pickle(output_path+"all_with_dummies_with_count_7days_14_3.pkl")
    df_all_head.to_csv(output_path+"all_with_dummies_head_7days_14_3.csv")
    df_internal.to_pickle(output_path+"internal_with_dummies_with_count_7days_14_3.pkl")
    df_medical.to_pickle(output_path+"medical_with_dummies_with_count_7days_14_3.pkl")
    df_surgical.to_pickle(output_path+"surgical_with_dummies_with_count_7days_14_3.pkl")
    df_HS_internal.to_pickle(output_path+"HS_internal_7days_14_3.pkl")
    df_neuro.to_pickle(output_path+"neuro_with_dummies_with_count_7days_14_3.pkl")
    df_cardio.to_pickle(output_path+"cardio_with_dummies_with_count_7days_14_3.pkl")
    df_dermo.to_pickle(output_path+"dermo_with_dummies_with_count_7days_14_3.pkl")
    df_uro.to_pickle(output_path+"uro_with_dummies_with_count_7days_14_3.pkl")

    
    
    

else:
    #df_merged.to_pickle(output_path+"all_no_dummies.pkl")
    #df_merged_head.to_csv(output_path+"all_no_dummies.csv")
    
    df_all=df_merged.loc[(df_merged['dept_cat_disch'] == "internal") | (df_merged['dept_cat_disch'] == "internal_ICU")|
            (df_merged['dept_cat_disch'] == "internal_special")|(df_merged['dept_cat_disch'] == "general_ICU")|
            (df_merged['dept_cat_disch'] == "surgical_special") | (df_merged['dept_cat_disch'] == "surgical_general")|
            (df_merged['dept_cat_disch'] == "orthopedics")|(df_merged['dept_cat_disch'] == "surgical_ICU")]
    df_internal=df_merged.loc[(df_merged['dept_cat_disch'] == "internal") | (df_merged['dept_cat_disch'] == "internal_ICU")]#|(df['dept_cat_disch'] == "internal_special")|(df['dept_cat_disch'] == "geriatrics")|(df['dept_cat_disch'] == "general_ICU")]
    df_medical=df_merged.loc[(df_merged['dept_cat_disch'] == "internal") | (df_merged['dept_cat_disch'] == "internal_ICU")|(df_merged['dept_cat_disch'] == "internal_special")|(df_merged['dept_cat_disch'] == "general_ICU")]#|(df['dept_cat_disch'] == "geriatrics")
    df_surgical=df_merged.loc[(df_merged['dept_cat_disch'] == "surgical_special") | (df_merged['dept_cat_disch'] == "surgical_general")|(df_merged['dept_cat_disch'] == "orthopedics")|(df_merged['dept_cat_disch'] == "surgical_ICU")]#|(df['dept_cat_disch'] == "geriatrics")    

    df_all=df_all.reset_index(drop=True)
    df_internal=df_internal.reset_index(drop=True)
    df_medical=df_medical.reset_index()
    df_surgical=df_surgical.reset_index(drop=True)    
    
    
    HS_cols = [col for col in df_internal.columns if 'HS_' in col]
    df_HS_internal= df_internal[HS_cols]
   

    
    df_all.to_pickle(output_path+"all_no_dummies.pkl")
    df_internal.to_pickle(output_path+"internal_no_dummies.pkl")
    df_medical.to_pickle(output_path+"medical_no_dummies.pkl")
    df_surgical.to_pickle(output_path+"surgical_no_dummies.pkl")
    df_HS_internal.to_pickle(output_path+"HS_internal.pkl")
#feature engineering  
    
feat_list,cont_list,cat_list,lab_vs_list=get_features(df_internal) 
if "ISHP_BactFstAcqDate" in feat_list: feat_list.remove("ISHP_BactFstAcqDate")
if "ISHP_BactFstAcqDate" in cont_list: cont_list.remove("ISHP_BactFstAcqDate")

if IS_ADD_AGE_INTERACTION:
    ageX_df=get_age_interactions(df_internal,cont_list) 
    ageX_df=ageX_df.reset_index(drop=True)
    ageX_df.to_pickle(output_path+"age_interaction.pkl")

if IS_ADD_AGE_SQ_INTERACTION:
    ageX_df=get_age_interactions(df_internal,cont_list) 
    ageX_df=ageX_df.reset_index(drop=True)
    ageX_df.to_pickle(output_path+"age_sq_interaction.pkl")

if IS_CONT_TO_CAT:
    cat_upper_df,cat_lower_df=cont_to_cat(df_internal,lab_vs_list)
    cat_upper_df=cat_upper_df.reset_index(drop=True)
    cat_lower_df=cat_lower_df.reset_index(drop=True)
    
    cat_upper_df.to_pickle(output_path+"cat_upper.pkl")
    cat_lower_df.to_pickle(output_path+"cat_lower.pkl")



if IS_ADD_CCI_INTERACTION:
    cciX_df=get_cci_interactions(df_internal,cont_list)
    cciX_df=cciX_df.reset_index(drop=True)
    
    cciX_df.to_pickle(output_path+"cci_interaction.pkl")



    
    
    















































    
#if IS_ADD_CATEGORICAL_LABS:
#    lab_cols = [col for col in df_internal.columns if 'LABS_' in col]
#    df_labs_cat_upper=pd.DataFrame(columns = lab_cols)
#    df_labs_cat_lower=pd.DataFrame(columns = lab_cols)
#
#    for col in lab_cols:
#        df_labs_cat_upper[col]=np.where(df_internal[col]>df_internal[col].quantile(q=0.90),1,0)
#        df_labs_cat_lower[col]=np.where(df_internal[col]>df_internal[col].quantile(q=0.10),1,0)
#
#        
#    df_labs_cat_upper=df_labs_cat_upper.add_suffix('_CAT_LABS_UPPER')
#    df_labs_cat_lower=df_labs_cat_lower.add_suffix('_CAT_LABS_LOWER')
#
#    
#    df_internal=pd.merge(df_internal.reset_index(),df_labs_cat_upper.reset_index(),left_index=True, right_index=True)
#    df_internal=pd.merge(df_internal.reset_index(),df_labs_cat_lower.reset_index(),left_index=True, right_index=True)
#
#    index_cols = [col for col in df_internal.columns if 'index' in col]
#    df_internal=df_internal.drop(index_cols, axis=1)
#
#    #df_internal_w_ageX_catLabs.to_pickle(output_path+"internal_with_dummies_w_ageX_w_labsCat.pkl")
# 
#        
#if IS_ADD_CCI_INTERACTION:
#    feat=list(df_internal.columns)
#    new_df = pd.DataFrame(columns = feat)
#    new_df=new_df.drop(columns=['CaseNum',  'EnterDate', 'ExitDate','LABEL_JUST_ER','enter_month','discharge_month','log_LOS',
#                                'LABEL_HOSP','PatNum','ISHP_BactFstAcqDate','HS_Hospital_Score','HS_Previos_admissions_cnt'])
#    feat=list(new_df.columns)
#    
#    for i in feat:
#        temp=df_internal_w_ageX_catLabs[i]*df_internal_w_ageX_catLabs["CCI_CharlsDiseases"]
#        new_df[i]=temp
#    new_df=new_df.add_suffix('_X_CCI')
#    
#    df_internal_w_ageX_catLabs_CCIX=pd.merge(df_internal_w_ageX_catLabs.reset_index(),new_df.reset_index(),left_index=True, right_index=True)
#    
#    df_internal_w_ageX_catLabs_CCIX.to_pickle(output_path+"internal_with_dummies_w_ageX_w_labsCat_cciX.pkl")
#   
#    
#





    
    
#df_HS.to_pickle(output_path+"HS_only.pkl")