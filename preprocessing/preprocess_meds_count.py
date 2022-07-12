# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 16:31:50 2021

@author: orlyk
"""

import pandas as pd
import numpy as np


def f_preprocess_meds_count():
    df_meds_hosp=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\medications\df_meds_hosp_pop.pkl")
    df_meds_adm=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\medications\df_meds_adm_pop.pkl")
    df_meds_dis=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\medications\df_meds_dis_pop.pkl")
    
   
    output_path="O:/OrlI/readmissions/preprocessed/medications/meds_for_model/"

    
    df_meds_dis=df_meds_dis.drop_duplicates()
    df_meds_adm=df_meds_adm.drop_duplicates()
    df_meds_hosp=df_meds_hosp.drop_duplicates()

    df_disch_count=df_meds_dis.groupby(by="CaseNum").count().reset_index()
    df_adm_count=df_meds_adm.groupby(by="CaseNum").count().reset_index()
    df_meds_hosp_count=df_meds_hosp.groupby(by="CaseNum").count().reset_index()
    
    df_disch_count=df_disch_count[["CaseNum","DrugCode"]]
    df_adm_count=df_adm_count[["CaseNum","DrugCode"]]
    df_meds_hosp_count=df_meds_hosp_count[["CaseNum","DrugName"]]
    
    df_disch_count=df_disch_count.rename(columns={"DrugCode":"meds_count_disch"})
    df_adm_count=df_adm_count.rename(columns={"DrugCode":"meds_count_adm"})
    df_meds_hosp_count=df_meds_hosp_count.rename(columns={"DrugName":"meds_count_hosp"})

    df_disch_count.to_pickle(r'O:\OrlI\readmissions\preprocessed\medications\meds_for_model\meds_count_disch.pkl')
    df_adm_count.to_pickle(r'O:\OrlI\readmissions\preprocessed\medications\meds_for_model\meds_count_adm.pkl')
    df_meds_hosp_count.to_pickle(r'O:\OrlI\readmissions\preprocessed\medications\meds_for_model\meds_count_hosp.pkl')
    return df_disch_count,df_adm_count,df_meds_hosp_count
    

