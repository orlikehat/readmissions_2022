# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:57:12 2020

@author: orlyk
"""

import pyodbc
import pandas as pd
import numpy as np



#global dwr_path
#dwr_path="C:/Users/orlyk/readmissions/project/dwh/"


global output_path
output_path="O:/OrlI/readmissions/preprocessed/labs/blood_count/blood_count_preprocessed/"





def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn




def extract_blood_count(code,name):
    s_columns = 'CaseNum,PatNum,PatIdNum,Result,Approval_Time,Approval_Date,Is_Cancelled'
    s_table = 'AUTODB_Labs_Fact_Tests'
    s_cond = code
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table + ' WHERE ' + s_cond
    cnxn_dwh_prd=f_get_connection('DWH_PRD')
    df=pd.read_sql(s_query, cnxn_dwh_prd)
    df = df[~df.Result.str.contains("Cancelled")]

    df = df[df['Is_Cancelled'] != 1]
    df.Result = df['Result'].replace({'.': '-', '':'-','.....': '-',":::::":"-","-----":"-",
                  "+++++":"-","----":"-","XXXX":"-","....":"-","<25":"0","DeltaWorks":"-","++++":"-",
                  "XXXXX":"-"})
    
    df.Result = df.Result.fillna('-')
    df = df[df['Result'] != '-']
    df["Result"]=pd.to_numeric(df["Result"])
    df['Approval_Date'] = pd.to_datetime (df['Approval_Date'])
    df["Approval_Time"]=df["Approval_Time"].astype(str)
    df['time'] = df['Approval_Time'].str[11:16]
    df['date'] = df['Approval_Date'].dt.date
    df["date"]=df["date"].astype(str)
    df["date_time"+"_"+name]=df.apply(lambda x: np.datetime64(x['date'] + ' ' + x['time']), axis=1)
    
    df.rename(columns={"Result":name+'_'+'result'}, inplace=True)    

    df=df.drop(columns={"PatNum","PatIdNum","Is_Cancelled","Approval_Date",
                        "Approval_Time","date","time"})
    
    #df.to_pickle(dwr_path+name+".pkl")
    
    return df

def get_blood_count_full():
    global df_RDW
    df_RDW=extract_blood_count('Test_Code=805009010','RDW')
    
    global df_hgb
    df_hgb=extract_blood_count('Test_Code=803551010 OR Test_Code=803551150  OR Test_Code=885018010','hgb')  
    
    global df_HCT
    df_HCT=extract_blood_count('Test_Code=805004010 OR Test_Code=802320150  OR Test_Code=802320010','HCT')  
   
    global df_MCH
    df_MCH=extract_blood_count('Test_Code=805006010','MCH')
   
    global df_MCHC
    df_MCHC=extract_blood_count('Test_Code=805007010','MCHC')
    print("dddd")
    global df_NRBC_WBC
    df_NRBC_WBC=extract_blood_count('Test_Code=805210010','NRBV_WBC')
   
    global df_neutrophils_perc
    df_neutrophils_perc=extract_blood_count('Test_Code=805015010','neutro_perc')
   
    global df_neutrophils_abs
    df_neutrophils_abs=extract_blood_count('Test_Code=805021010','neutro_abs')
  
    global df_lymphocytes_perc
    df_lymphocytes_perc=extract_blood_count('Test_Code=805016010','lymphocytes_perc')
   
    global df_lymphocytes_abs
    df_lymphocytes_abs=extract_blood_count('Test_Code=805022010','lymphocytes_abs')
    
    global df_monocytes_perc
    df_monocytes_perc=extract_blood_count('Test_Code=805017010','monocytes_perc')
  
    global df_monocytes_abs
    df_monocytes_abs=extract_blood_count('Test_Code=805023010','monocytes_abs')
  
    global df_eosinophils_perc
    df_eosinophils_perc=extract_blood_count('Test_Code=805024010','eosinophils_perc')
    
    global df_eosinophils_abs
    df_eosinophils_abs=extract_blood_count('Test_Code=805018010','eosinophils_abs')
    print("dsdsds")
    global df_basophils_perc
    df_basophils_perc=extract_blood_count('Test_Code=805019010','basophils_perc')
  
    global df_basophils_abs
    df_basophils_abs=extract_blood_count('Test_Code=805025010','basophils_abs')    
   
    global df_platetelet_count
    df_platetelet_count=extract_blood_count('Test_Code=885049010','platetelet_count')
   
    global df_platelet_volume
    df_platelet_volume=extract_blood_count('Test_Code=805012010','platelet_volume')
    
    
    return df_RDW,df_hgb,df_HCT,df_MCH,df_MCHC,df_NRBC_WBC,df_neutrophils_perc,df_neutrophils_abs,df_lymphocytes_perc,df_lymphocytes_abs,df_monocytes_perc,
    df_monocytes_abs,df_eosinophils_perc,df_eosinophils_abs,df_basophils_perc,
    df_basophils_abs,df_platetelet_count,df_platelet_volume

def get_blood_count(l_casenum,is_full):
    
    if is_full=="full":
        get_blood_count_full()
    
    frames=[df_RDW,df_hgb,df_HCT,
            df_MCH,df_MCHC,
            df_NRBC_WBC,df_neutrophils_perc,
            df_neutrophils_abs,df_lymphocytes_perc,
            df_lymphocytes_abs,df_monocytes_perc,
            df_monocytes_abs,df_eosinophils_perc,
            df_eosinophils_abs,df_basophils_perc,
            df_basophils_abs,df_platetelet_count,
            df_platelet_volume]
  
    names=["RDW","hgb","HCT",
           "MCH","MCHC",
            "NRBC_WBC","neutrophils_perc",
            "neutrophils_abs","lymphocytes_perc",
            "lymphocytes_abs","monocytes_perc",
            "monocytes_abs","eosinophils_perc",
            "eosinophils_abs","basophils_perc",
            "basophils_abs","platetelet_count",
            "platelet_volume"]  
    
    if len(l_casenum) > 0:
        for i in range(len(frames)):
            frames[i]=frames[i][frames[i]['CaseNum'].isin(l_casenum)]
            frames[i].to_pickle(output_path+names[i]+"_pop.pkl")
       
        
#df=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\preprocessed\population\df_readmin_with_labels_base.pkl")       
#l_casenum=df["CaseNum"]  
#get_blood_count(l_casenum,"full")   


    
    
 