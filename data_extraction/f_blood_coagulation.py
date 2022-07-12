# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 14:31:25 2020

@author: orlyk
"""
import pyodbc
import pandas as pd
import numpy as np
#todo improve code
#1. read tests and codes from excel file
#2. create dictionary of dataframes for test results

global output_path
output_path="O:/OrlI/readmissions/preprocessed/labs/blood_coagulation/blood_coag_preprocessed/"    


    
def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn



def extract_blood_coag(code,name):
    s_columns = 'CaseNum,PatNum,PatIdNum,Result,Approval_Time,Approval_Date,Is_Cancelled,Test_Code'
    s_table = 'AUTODB_Labs_Fact_Tests'
    s_cond = code
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table + ' WHERE ' + s_cond
    cnxn_dwh_prd=f_get_connection('DWH_PRD')
    df=pd.read_sql(s_query, cnxn_dwh_prd)
    df = df[~df.Result.str.contains("Cancelled")]

    df = df[df['Is_Cancelled'] != 1]
##    df.Result = df['Result'].replace({'.': '-', '':'-','.....': '-',":::::":"-","-----":"-",
##                  "+++++":"-","----":"-","XXXX":"-","....":"-","DeltaWorks":"-","++++":"-",
##                  "XXXXX":"-","Canceled":"-","cancelled":"-","פסול":"-", 
##                  ">0.01":"-","<0":"-","X-NORESULT":"-","*****":"-",
##                  ">5":"6","<0.01":"0.009","<6":"5","<60":"59","<25":"24","<5":"4","<1":"0","<0.1":"0.01",
##                  "<0.2":"0.1","<0.15":"0.14","<10":"9",">200":"201","<0.001":"0.0001","< 0.1":"0.09",
##                  "<0.004":"0.003","< 0.01":"0.009","<0.03":"0.02",">0.03":"0.04","<0.4":"0.3",
##                  "<15":"14","<0.3":"0.2","<8":"7",">1":"2","<7":"6","<0.5":"0.4","<12":"11",
##                  "<20":"19",">1650.0":"1651","<9":"8","<2":"1","<1.3":"1.2","<1.3":"1.2",">8250":"8251",
##                  ">1650":"1651",">5000.00":"5001","<2.00":"1","<0.015":"0.001",">50.0000":"51",
##                  ">50.0":"51",">50.000":"51",">250":"251","> 50.00":"51",">50000.00":"50001",
##                  "<2.50":"2.4",">25000.00":"25001","<2.5":"2.4",">0.1":"0.09",">0.001":"0.0001",
##                  ">50000":"50001","< 2.50":"2.49","<2.500":"2.4",">25000.000":"25001",">10":"11",
##                  ">150.000":"151","<0.008":"0.007",">150.00":"151",">150":"151",">12.00":"13",
##                  "<0.10":"0.09",">12":"11",">120":"121","120<":"119",">120                  ":"121"})
    df=df[pd.to_numeric(df['Result'], errors='coerce').notnull()]
    df.Result = df.Result.fillna('-')
    df = df[df['Result'] != '-']
    df["Result"]=pd.to_numeric(df["Result"])
    df = df[df['Result'] >=0]
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
print("dfs")

def get_blood_coag_full():
    global df_ptt
    df_ptt=extract_blood_coag('Test_Code=885730010',"ptt")
    global df_pt_sec
    df_pt_sec=extract_blood_coag('Test_Code=806469010',"pt_sec")
    global df_pt_inr
    df_pt_inr=extract_blood_coag('Test_Code=806468010',"pt_inr")
    


###################################################################################


def get_blood_coag(l_casenum,is_full): 
    
    if is_full=="full":
        get_blood_coag_full()
    
    frames=[
    df_ptt,
    df_pt_sec,
    df_pt_inr]
  
    names=["ptt",
    "ptt_sec",
    "pt_inr",
    ]  
    
    if len(l_casenum) > 0:
        for i in range(len(frames)):
            frames[i]=frames[i][frames[i]['CaseNum'].isin(l_casenum)]
            frames[i].to_pickle(output_path+names[i]+"_pop.pkl")
   
#df=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\preprocessed\population\df_readmin_with_labels_base.pkl")       
#l_casenum=df["CaseNum"]  
#get_blood_coag(l_casenum,"full")           
##df=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\preprocessed\population\df_readmin_with_labels_base.pkl")       
##l_casenum=df["CaseNum"]  
##get_blood_count(l_casenum,"full")   



#todo: check lit for icteric index, hemolytic index, lipemic index