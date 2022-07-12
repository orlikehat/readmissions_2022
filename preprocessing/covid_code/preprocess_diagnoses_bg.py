
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 12:57:06 2021

@author: orlyk
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 12:31:38 2020

@author: orlyk
"""

import pandas as pd
import numpy as np


def f_preprocess_diagnoses_bg():

    df=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\population\covid\df_readmin_with_labels_base.pkl")
    output_path="O:/OrlI/readmissions/preprocessed/diagnoses/diagnoses_for_model/"
    
    df_diag=pd.read_pickle(r"O:\OrlI\readmissions\preprocessed\diagnoses\df_diagnoses_bg_pop_covid.pkl")
    
    
    
    
    def pivot_diagnoses(df,level):
            df["N"]=1
                    
            diag_table = pd.pivot_table(df, values=['N'], index="CaseNum",columns=[level], aggfunc=np.sum, fill_value=0)    
            #diag_table=diag_table.drop_duplicates()
            diag_table = diag_table.reset_index()
            diag_table.columns = list(map("".join, diag_table.columns))
            return diag_table
        
        
    df=df[df["BASE_FLG"]==1]
    df=df[["CaseNum","PatNum","Age","year"]]
    df=pd.merge(df,df_diag,on="CaseNum",how="left")
    
    df_mdclone = pd.read_excel(r'C:\Users\orlyk\readmissions\project\code\support_files\Diagnosis_codes_MDClone_2021.xlsx')
    df_mdclone = df_mdclone.rename(index=str, columns={"Code": "Diag_Free_Text"})    
    
    df_mdclone=df_mdclone[(df_mdclone['Chapter'] != 'UNSPECIFIED')]
    df_mdclone=df_mdclone[(df_mdclone['Chapter'] != 'Not specified')]
    

   # # Changing to uppercase in df
    df['Diag_Free_Text'] = df['Diag_Free_Text'].str.upper()
    df = df.merge(df_mdclone, how='left', on='Diag_Free_Text')
       
    df=df[['CaseNum', 'PatNum_x','DiagCode_ICD9','Diag_Free_Text','Category', 'Block', 'Chapter']]
    
    df_bg_block261=pivot_diagnoses(df,'Block')
    for col in df_bg_block261.columns:
        if col !='CaseNum':
            df_bg_block261[col]=np.where(df_bg_block261[col]>0,1,0)
    df_bg_block261['Total_bg_block']= df_bg_block261.sum(axis=1)
            
           
    df_bg_chapter19=pivot_diagnoses(df,'Chapter')
    for col in df_bg_chapter19.columns:
        if col !='CaseNum':
            df_bg_chapter19[col]=np.where(df_bg_chapter19[col]>0,1,0)
    df_bg_chapter19['Total_bg_chapter']= df_bg_chapter19.sum(axis=1)
    
    df_bg_category1395=pivot_diagnoses(df,'Category')
    for col in df_bg_category1395.columns:
        if col !='CaseNum':
            df_bg_category1395[col]=np.where(df_bg_category1395[col]>0,1,0)
    df_bg_category1395['Total_bg_category']= df_bg_category1395.sum(axis=1)
    
    #df_bg_no_category=df.dropna(subset=["Diag_Free_Text"])
    #df_bg_no_category=df_bg_no_category[['CaseNum','Diag_Free_Text']].drop_duplicates()
    #df_bg_no_category=pivot_diagnoses(df_bg_no_category,'Diag_Free_Text')
    #for col in df_bg_no_category.columns:
    #    if col !='CaseNum':
    #        df_bg_no_category[col]=np.where(df_bg_no_category[col]>0,1,0)
    #df_bg_no_category['Total_bg_no_category']= df_bg_no_category.sum(axis=1)
    
    
    
    
    df_bg_block261.to_pickle(output_path+"bg_table_block261_covid.pkl")
    df_bg_block261=df_bg_block261.add_prefix('BLOCK_')
    df_bg_block261=df_bg_block261.rename(columns={"BLOCK_CaseNum": "CaseNum"})

    df_bg_chapter19.to_pickle(output_path+"bg_table_chapter19_covid.pkl")
    df_bg_chapter19=df_bg_chapter19.add_prefix('CHAPTER_')
    df_bg_chapter19=df_bg_chapter19.rename(columns={"CHAPTER_CaseNum": "CaseNum"})

    df_bg_category1395.to_pickle(output_path+"bg_table_category1395_covid.pkl")
    df_bg_category1395=df_bg_category1395.add_prefix('CATEGORY_')
    df_bg_category1395=df_bg_category1395.rename(columns={"CATEGORY_CaseNum": "CaseNum"})

    
    #df_fin=pd.merge(df_bg_block261,df_bg_chapter19,how="left",right_on="CHAPTER_CaseNum",left_on="BLOCK_CaseNum")
    #df_fin=pd.merge(df_fin,df_bg_category1395,how="left",right_on="CATEGORY_CaseNum",left_on="BLOCK_CaseNum")
    
    #df_fin=df_fin.drop(columns=['BLOCK_CaseNum', 'CHAPTER_CaseNum'])
    #df_fin = df_fin.rename(columns={"CATEGORY_CaseNum": "CaseNum"})
    #df_fin=df_fin.rename(columns={"CHAPTER_CaseNum": "CaseNum"})
    
    return  df_bg_chapter19#,df_bg_chapter19,df_bg_category1395,df_fin
    


