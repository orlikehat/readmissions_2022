# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 11:50:44 2021

@author: orlyk
"""


import pandas as pd
import numpy as np
from functions.helpers.get_catagorical import *




def filter_input(df,group=[],compact=[]):
    filtering_params=pd.read_csv(r"O:\OrlI\readmissions\code\prediction_models\functions\filtering_params.csv")
    filtering_params=dict(zip(list(filtering_params.condition), list(filtering_params.value)))
     
    
    print("original_shape: " + str(df.shape))
    
    df["LABEL_HOSP"]=np.where(df["LABEL_HOSP"]==1,1,0)
    df["LABEL_JUST_ER"]=np.where(df["LABEL_JUST_ER"]==1,1,0)

    
     #todo add this to preprocessing
#    if "LABS_albumin_result_min" in df: 
#        
#        df["LABS_acr_1"]=df["LABS_albumin_result_min"]/df["LABS_creatinine_result_max"]
#        df["LABS_acr_2"]=df["LABS_albumin_result_last"]/df["LABS_creatinine_result_last"]   
#        
         #todo add this to preprocessing

    if "ISHP_BactFstAcqDate" in df:
        df=df.drop("ISHP_BactFstAcqDate", axis=1)
    
    if filtering_params['IS_AGE_X']=='1':
        print("adding age interactions")
        ageX_df=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\model_input\age_interaction.pkl")
        df=pd.merge(df,ageX_df,left_index=True, right_index=True)
        
    if filtering_params['IS_ADD_AGE_SQ_INTERACTION']=='1':
        print("adding age sq_interactions")
        ageX_df=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\model_input\age_sq_interaction.pkl")
        df=pd.merge(df,ageX_df,left_index=True, right_index=True)    
        
    if filtering_params['IS_CCI_X']=='1':
       print("adding cci interactions")
       cciX_df=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\model_input\cci_interaction.pkl")
       df=pd.merge(df,cciX_df,left_index=True, right_index=True)
    
    if filtering_params['IS_CONT_TO_CAT']=='1':   
       print("adding IS_CONT_TO_CAT")
       cat_lower=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\model_input\cat_lower.pkl")
       cat_upper=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\model_input\cat_upper.pkl")
       df=pd.merge(df,cat_lower,left_index=True, right_index=True)
       df=pd.merge(df,cat_upper,left_index=True, right_index=True)
     
       
     
       
       
    if filtering_params['labs_data']=="all":
        print("lab data: all")
        
    elif filtering_params['labs_data']=="cont":
        print("lab data: cont")

        lab_cat = [col for col in df.columns if '_CAT_LABS' in col]
        df=df.drop(lab_cat, axis=1)
        
    elif filtering_params['labs_data']=="categorial":
        print("lab data: categorial")

        lab_col = [col for col in df.columns if 'LABS_' in col]
        lab_cat = [col for col in df.columns if '_CAT_' in col]
        df_lab_cat=df[lab_cat]
             
        df=df.drop(lab_col, axis=1)
        df=pd.merge(df.reset_index(),df_lab_cat.reset_index(),left_index=True, right_index=True)



       
    
    #only internal
    if filtering_params['IS_INTERNAL_ONLY']=="1":
        if 'dept_cat_disch_internal' in df.columns:
            df=df[(df["dept_cat_disch_internal"]==1) | (df["dept_cat_disch_internal_ICU"]==1)]# |(df["dept_cat_disch_geriatrics"]==1)]
            print("internal_shape: " + str(df.shape))
            
        else: 
            df=df.loc[(df['dept_cat_disch'] == "internal") | (df['dept_cat_disch'] == "internal_ICU")]#|(df['dept_cat_disch'] == "internal_special")|(df['dept_cat_disch'] == "geriatrics")|(df['dept_cat_disch'] == "general_ICU")]
    
            
    
     #year
    if 'year' in df: 
        df=df[(df.year>=float(filtering_params["TH_year"]))]
    
    #threshold patients
    if 'LABS_BUN_result_last' in df:
        if group=="train":
            
            df=df.dropna(thresh=float(filtering_params["TH_patients"])*(df.shape[1]), axis=0)
            
            if filtering_params["ONLY_IS_CHEM"]=="1":
                df=df.dropna(subset=['LABS_BUN_result_last'])
            if filtering_params["ONLY_IS_COUNT"]=="1":
                df=df.dropna(subset=['LABS_RDW_result_first'])
            
        #threshold features
            df=df.dropna(thresh=float(filtering_params["TH_features"])*(df.shape[0]), axis=1)
    
    #threshold age
    if 'age' in df:
        df=df[df["age"]>float(filtering_params["TH_age"])]
    
    if 'gender' in df:
        if filtering_params["IS_MALE"]=="1":
            df=df[df["gender"]==0] 
        elif filtering_params["IS_MALE"]=="2":
            df=df[df["gender"]==1] 
    #pulmonary        
    if "CCI_bg_cci_Chronicpulmonarydisease" in df:
        if filtering_params["IS_PULMONARY"]=="1":
            df=df[df["CCI_bg_cci_Chronicpulmonarydisease"]==1]
   #hypertension
    if filtering_params["IS_HYPERTENSION"]=="1": 
       df_diag=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\diagnoses\diagnoses_for_model\bg_table_block261.pkl")
       df_hyper=df_diag[["CaseNum","NHypertensive diseases"]]
       #df_hyper=df_hyper[df_hyper["NHypertensive diseases"]==1]
       df_hyper=df_hyper.drop_duplicates()
       df=pd.merge(df,df_hyper,on="CaseNum",how="left")
       df=df[df["NHypertensive diseases"]==1]
       #df["NHypertensive diseases"]=np.where(df["NHypertensive diseases"]==1,1,0)
    
    
    #HF
    if "CCI_bg_cci_CongestiveHeartFailure" in df:
        if filtering_params["IS_HF"]=="1":
            df=df[df["CCI_bg_cci_CongestiveHeartFailure"]==1]
   #CCI
    if 'CCI_CharlsScore' in df:
        df=df[df["CCI_CharlsScore"]>=float(filtering_params["TH_CCI"])]
    
    
        
        
    if filtering_params['IS_VISIT']=='first':
        df=df.sort_values(by="EnterDate")
        df=df.drop_duplicates(subset=['PatNum'])
    elif filtering_params['IS_VISIT']=='last': 
        df=df.sort_values(by="EnterDate")
        df=df.drop_duplicates(subset=['PatNum'],keep="last")
    
    if 'HS_Hospital_Score' in df:
        if filtering_params["IS_HS_in"]=='0':
            df=df.drop(columns=['HS_Hospital_Score','HS_Previos_admissions_cnt'])
            
            
            
    
    #threshold LOS
    if 'LOS' in df:
        filtering_params["MIN_LOS"]=int(filtering_params["MIN_LOS"])   
        if filtering_params["MIN_LOS"]>0:
            df=df[df["LOS"]>(filtering_params["MIN_LOS"]-1)]
            
    if filtering_params["limit_diag"]=="1":
        diag_columns= [col for col in df.columns if 'DIAG_' in col]
        df_diag=df[diag_columns]
        
        dia_adm_columns=[col for col in df_diag.columns if '_adm' in col]
        adm_sum = df_diag[dia_adm_columns].sum(axis=0).reset_index().rename(columns={0: "counts"})
        adm_list=list(adm_sum.sort_values(by=['counts'],ascending=True).head(100)["index"])
        
        
        dia_disch_columns=[col for col in df_diag.columns if '_dis' in col]
        dis_sum = df_diag[dia_disch_columns].sum(axis=0).reset_index().rename(columns={0: "counts"})
        dis_list=list(dis_sum.sort_values(by=['counts'],ascending=True).head(100)["index"])
        
        
        dia_bg_columns=[col for col in df_diag.columns if 'DIAG_BG' in col]
        bg_sum = df_diag[dia_bg_columns].sum(axis=0).reset_index().rename(columns={0: "counts"})
        bg_sum=list(bg_sum.sort_values(by=['counts'],ascending=True).head(100)["index"])
        
        df.drop(columns=adm_list, inplace=True)
        df.drop(columns=dis_list, inplace=True)
        df.drop(columns=bg_sum, inplace=True)

  
    
    

   
  
        
    if filtering_params['algo']=="cat":
          
#        month_cols = [col for col in df.columns if 'month' in col]
#        year_cols=[col for col in df.columns if 'year' in col]
#        sex_cols=[col for col in df.columns if 'sex ' in col]
#        dept_cols=[col for col in df.columns if 'dept' in col]
#        disch_cols=[col for col in df.columns if 'discharge_type' in col]
#        entry_cols=[col for col in df.columns if 'entry' in col]
#        diag_cols=[col for col in df.columns if 'DIAG' in col]
#        vent_cols=[col for col in df.columns if 'VENT' in col]
#        cci_cols=[col for col in df.columns if 'CCI_bg' in col]
#        med=[col for col in df.columns if 'MEDS_' in col]
#        family_stat=[col for col in df.columns if 'family_stat' in col]
#        quarter_cols=[col for col in df.columns if 'Quarter' in col]
#        week_cols=[col for col in df.columns if 'Week' in col]
#        continent_cols=[col for col in df.columns if 'ISHP_ContinentID' in col]
#        cat_list=disch_cols+month_cols+year_cols+dept_cols+ entry_cols+diag_cols+vent_cols+sex_cols+cci_cols+family_stat+med+quarter_cols+week_cols+continent_cols
#        
        
        cat_list=get_categorical(df)

        
        df[cat_list] = df[cat_list].astype('category')
        cat_columns = df.select_dtypes(['category']).columns
        df[cat_columns] = df[cat_columns].apply(lambda df: df.cat.codes)
       
   
    
      
    print("filtered_shape: " + str(df.shape))
      #todo add this to preprocessing

    
    list_to_drop=["year","ISHP_Chest_Pain_on_Disch_Flg","HS_LOS_over5","ISHP_Chest_Pain_Main_on_Adm_Flg",
                  'before_2017','CCI_CharlsScore','ISHP_ArrivedWithInfFlg',
            'ISHP_IsAnyInfFlg',
            'family_stat_ ',
            'family_stat_L',
            'dept_cat_disch_internal_ICU',
            'dept_cat_disch_internal_special',
            'dept_cat_disch_orthopedics',
            'dept_cat_disch_surgical_ICU',
            'dept_cat_disch_surgical_general',
            'dept_cat_disch_surgical_special',
            'dept_cat_disch_women',
            #'discharge_type_discharge_hasava',
#            'discharge_type_discharge_home',
#            'discharge_type_discharge_other_facility',
#            'discharge_type_discharge_refused_treatment',
#            'discharge_type_discharged_left',
#            'discharge_type_other',
            'ISHP_KupaCode_10',
            'ISHP_KupaCode_11',
            'ISHP_KupaCode_12',
            'ISHP_KupaCode_13',
            'ISHP_KupaCode_80',
            'ISHP_KupaCode_81',
            'ISHP_KupaCode_82',
            'ISHP_KupaCode_83',
            'ISHP_KupaCode_98',
            'ISHP_KupaCode_99',
            'ISHP_ContinentID_AF',
            'ISHP_ContinentID_AS',
            'ISHP_ContinentID_EU',
            'ISHP_ContinentID_NA',
            'ISHP_ContinentID_OC',
            'ISHP_ContinentID_SA']
     #       "COUNT_DIAG_BG_diag_count_bg"]
    
    
    for item in list_to_drop:
        if item in df:
            df=df.drop(item, axis=1)
            
            
    if compact==1: 
        print("----------- manual selection data----------------")
        feats=pd.read_csv(r'O:\OrlI\readmissions\code\prediction_models\functions\feature_list2.csv',delimiter=',')
        df=df[[c for c in df.columns if c in feats]]
#    
    
#    
#   

    
   
    print("filtered_shape: " + str(df.shape))

    return df 







    