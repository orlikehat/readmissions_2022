# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 22:37:27 2020

@author: orlyk
"""

import pandas as pd
import numpy as np
import math




#population: basic data:

def f_preprocess_basic_data():


#    df=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\population\df_readmin_with_labels_base.pkl")
#    df_demo=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\demographics\df_demographics_pop.pkl")
    df=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\population\df_readmin_with_labels_base.pkl")
    df_demo=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\demographics\df_demographics_pop.pkl")    
    df_dept_classification=pd.read_csv(r"O:\OrlI\readmissions\code\support_files\departments_classification_v2.csv")
    
    output_path="O:/OrlI/readmissions/preprocessed/population/population_for_model/"
    
    #only relevant columns
    df=df[['CaseNum','CaseTypeCode','PatNum',
           'Age', 'EnterDate',
           'ExitDate','SugKnisaDesc',
           'SugKnisaOrgMedFlg',
           'ShihrurMvType',
           'SugShihrurOrgMedFlg',
           'ShihrurMvTypeName',
           'DeathDate',
           'DeathInIshpuzFlg',
           'OrgMedAdmTatYahidaDesc',
           'MedOrgTreeAdm',
           'MedOrgTreeDisch',
           'OrgMedDischTatYahidaDesc',
           'LABEL_HOSP',
           'LABEL_JUST_ER' ]]
    
    #remove patients that died up to 3 months after discharge
    
    
    #dates
    df["EnterDate"]=pd.to_datetime(df["EnterDate"])
    df["ExitDate"]=pd.to_datetime(df["ExitDate"])
    df["DeathDate"]=pd.to_datetime(df["DeathDate"])
    
    df['year'] = df['ExitDate'].dt.year
    #df=df[df["year"]<2020]
    df["enter_month"]=df['ExitDate'].dt.month
    df["discharge_month"]=df['ExitDate'].dt.month
    
    df["before_2017"]=np.where(df["year"]<2017,1,0)
    
    #remove patients that died up to 3 months after discharge
    df["delta_death"]=df['DeathDate']-df['ExitDate']
    df["delta_death"]=df["delta_death"].dt.days
    count_pre=len(df)
    df["delta_death"]=df["delta_death"].fillna(9999)
    df=df[df["delta_death"]>=30]
    print("% of patient that died up to 30 days after discharge: "+str((count_pre-len(df))/count_pre*100))
    
    
    #age
    bins=[15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,99,120]
    df["age_bins5"]=pd.cut(df["Age"],bins=bins)
    
    
    #entry type
    df["entry_type"]= df["SugKnisaOrgMedFlg"]                                                         
    df=df.replace({'entry_type' : { 5 : "elective", 2 : "ED2hosp", 8 : "ED2EDwait",4:"urgentHosp",10:"ED2hosp" }})
    other_entry=df["entry_type"][(df["entry_type"] != "elective")&
                   (df["entry_type"] != "ED2hosp")&
                   (df["entry_type"] != "ED2EDwait")&
                   (df["entry_type"] != "urgentHosp")&
                   (df["entry_type"] != "ED2hosp")]
    other_entry_indx=other_entry.index.tolist()
    df["entry_type"].loc[other_entry_indx]="other"
    
    #discharge destination
    
    df["discharge_type"]= df["ShihrurMvType"]                                                         
    df=df.replace({'discharge_type' : { "10" : "discharge_home", "60" : "discharge_other", 
                                       "20" : "discharge_other_facility",
                                       "30":"discharge_refused_treatment",
                                       "52":"discharged_left",
                                       "50":"discharged_left",
                                       "51":"discharged_left",
                                       "97":"discharge_hasava",
                                       "94":"discharge_hasava",
                                       "96":"discharge_hasava"
                                       }})
    
    
    other_discharge=df["discharge_type"][(df["discharge_type"] != "discharge_home")&
                   (df["discharge_type"] != "discharge_other_facility")&
                   (df["discharge_type"] != "discharged_left")&
                   (df["discharge_type"] != "discharge_hasava")&
                   (df["discharge_type"] != "discharge_refused_treatment")]
    other_discharge_indx=other_discharge.index.tolist()
    df["discharge_type"].loc[other_discharge_indx]="other"
                   
    #add gender from df_demographics
    df_demo=df_demo[["PatNum","gender","family_stat","HolocaustSurvivor_flg","ChildrenNum"]]
    
    df_demo["gender"]=np.where(df_demo["gender"]=="1",1,0)
    df_demo["family_stat"]=np.where(df_demo["family_stat"]=="ג","divorced",df_demo["family_stat"])
    df_demo["family_stat"]=np.where(df_demo["family_stat"]=="נ","married",df_demo["family_stat"])
    df_demo["family_stat"]=np.where(df_demo["family_stat"]=="ר","single",df_demo["family_stat"])
    df_demo["family_stat"]=np.where(df_demo["family_stat"]=="א","widow",df_demo["family_stat"])
    df_demo["family_stat"]=np.where(df_demo["family_stat"]=="ל","L",df_demo["family_stat"])
    
    df_demo["ChildrenNum"] = [i.lstrip("0") for i in df_demo["ChildrenNum"]]
    df_demo["ChildrenNum"]=np.where(df_demo["ChildrenNum"]=="",0,df_demo["ChildrenNum"])
    df_demo["ChildrenNum"]=np.where(df_demo["ChildrenNum"]==" ",0,df_demo["ChildrenNum"])
    df_demo["ChildrenNum"]=df_demo["ChildrenNum"].astype('int32')

    
    
        
    
    df=pd.merge(df,df_demo,on="PatNum",how="left")
   
    
    #LOS
    
    df["LOS"]= df["ExitDate"]-df["EnterDate"]
    df["LOS"] = df["LOS"].dt.days
    df["log_LOS"]=np.log10(df["LOS"]+1)
    
    #departments
    df=pd.merge(df,df_dept_classification,how="left", on="MedOrgTreeAdm")
    df["dept_cat_adm"]=df["dept_cat"]
    df=df.drop(["dept_cat"],axis=1)
    df=pd.merge(df,df_dept_classification,how="left", left_on="MedOrgTreeDisch",right_on="MedOrgTreeAdm")
    df["dept_cat_disch"]=df["dept_cat"]
    df=df.drop(["dept_cat"],axis=1)
    
    df=df.rename(columns={"Age": "age"})
     
        
       
    
    ######finalize
        
    df_short=df[['CaseNum',
     'PatNum',
     'EnterDate',
     'ExitDate',
     'dept_cat_adm',
     'dept_cat_disch',
     'entry_type',
     'discharge_type',
     'age',
     'year',
     'enter_month',
     'discharge_month',
     'before_2017',
     
     'LOS',
     'log_LOS',
     'gender',
     'family_stat',
     'HolocaustSurvivor_flg',
     'ChildrenNum',  
     'LABEL_HOSP',
     'LABEL_JUST_ER']]
        
    
    df_short.to_pickle(output_path+"df_basic_data_short.pkl")
    #df_short.to_csv(output_path+"df_basic_data_short.csv")
    
#    

    return df_short





