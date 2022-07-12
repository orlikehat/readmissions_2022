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
output_path="O:/OrlI/readmissions/preprocessed/labs/blood_chem/blood_chem_preprocessed/"    


    
def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn



def extract_blood_chem(code,name):
    s_columns = 'CaseNum,PatNum,PatIdNum,Result,Approval_Time,Approval_Date,Is_Cancelled,Test_Code'
    s_table = 'AUTODB_Labs_Fact_Tests'
    s_cond = code
    s_query = 'SELECT ' + s_columns + ' FROM ' + s_table + ' WHERE ' + s_cond
    cnxn_dwh_prd=f_get_connection('DWH_PRD')
    df=pd.read_sql(s_query, cnxn_dwh_prd)
    df = df[~df.Result.str.contains("Cancelled")]

    df = df[df['Is_Cancelled'] != 1]
    df.Result = df['Result'].replace({'.': '-', '':'-','.....': '-',":::::":"-","-----":"-",
                  "+++++":"-","----":"-","XXXX":"-","....":"-","DeltaWorks":"-","++++":"-",
                  "XXXXX":"-","Canceled":"-","cancelled":"-","פסול":"-", 
                  ">0.01":"-","<0":"-","X-NORESULT":"-",
                  ">5":"6","<0.01":"0.009","<6":"5","<60":"59","<25":"24","<5":"4","<1":"0","<0.1":"0.01",
                  "<0.2":"0.1","<0.15":"0.14","<10":"9",">200":"201","<0.001":"0.0001","< 0.1":"0.09",
                  "<0.004":"0.003","< 0.01":"0.009","<0.03":"0.02",">0.03":"0.04","<0.4":"0.3",
                  "<15":"14","<0.3":"0.2","<8":"7",">1":"2","<7":"6","<0.5":"0.4","<12":"11",
                  "<20":"19",">1650.0":"1651","<9":"8","<2":"1","<1.3":"1.2","<1.3":"1.2",">8250":"8251",
                  ">1650":"1651",">5000.00":"5001","<2.00":"1","<0.015":"0.001",">50.0000":"51",
                  ">50.0":"51",">50.000":"51",">250":"251","> 50.00":"51",">50000.00":"50001",
                  "<2.50":"2.4",">25000.00":"25001","<2.5":"2.4",">0.1":"0.09",">0.001":"0.0001",
                  ">50000":"50001","< 2.50":"2.49","<2.500":"2.4",">25000.000":"25001",">10":"11",
                  ">150.000":"151","<0.008":"0.007",">150.00":"151",">150":"151",">12.00":"13",
                  "<0.10":"0.09",">12":"11","< 10":"9","LDLC ביטול. לא נתן לחשוב בשל ר":"-",
                  ">5000":"5000"})
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

def get_blood_chem_full():
    global df_globulin
    df_globulin=extract_blood_chem('Test_Code=802175010',"globulin")
    global df_lipase
    df_lipase=extract_blood_chem('Test_Code=883690010',"lipase")
    global df_iron
    df_iron=extract_blood_chem('Test_Code=883540010',"iron")
    global df_ferritin
    df_ferritin=extract_blood_chem('Test_Code=882728010',"ferritin")
    global df_transferrin
    df_transferrin=extract_blood_chem('Test_Code=884466010',"transferrin")
    global df_transferin_saturation
    df_transferin_saturation=extract_blood_chem('Test_Code=884466970',"transferin_saturation")
    global df_LDL
    df_LDL=extract_blood_chem('Test_Code=802152970',"LDL")
    
    global df_HDL
    df_HDL=extract_blood_chem('Test_Code=883718010',"HDL")
    global df_triglycerides
    df_triglycerides=extract_blood_chem('Test_Code=884478010',"triglycerides")
    global df_BNP
    df_BNP=extract_blood_chem('Test_Code=803176010',"BNP")
    global df_troponin
    df_troponin=extract_blood_chem('Test_Code=884484010',"troponin")
    global df_ethanol
    df_ethanol=extract_blood_chem('Test_Code=882055010',"ethanol")
    global df_TSH
    df_TSH=extract_blood_chem('Test_Code=884443010',"TSH")
    global df_T4
    df_T4=extract_blood_chem('Test_Code=884439010',"T4")
    global df_protein_total    
    df_protein_total=extract_blood_chem('Test_Code=884155010',"protein_total")
    global df_amylase    
    df_amylase=extract_blood_chem('Test_Code=882150010',"amylase")
    global df_LD
    df_LD=extract_blood_chem('Test_Code=883615010',"LD")
    global df_uric_acid
    df_uric_acid=extract_blood_chem('Test_Code=884550010',"uric_acid")
    global df_GGT
    df_GGT=extract_blood_chem('Test_Code=882977010',"GGT")
    global df_alkaline_phos
    df_alkaline_phos=extract_blood_chem('Test_Code=884075010',"alkaline_phos")
    global df_AST
    df_AST=extract_blood_chem('Test_Code=884450010',"AST")
    global df_chloride    
    df_chloride=extract_blood_chem('Test_Code=882435010',"chloride")
    global df_GPT
    df_GPT=extract_blood_chem('Test_Code=884460010',"GPT")
    global df_phosphorus
    df_phosphorus=extract_blood_chem('Test_Code=884100010','phosphorus')
    global df_CPK
    df_CPK=extract_blood_chem('Test_Code=882550010','CPK')
    global df_magnesium    
    df_magnesium=extract_blood_chem('Test_Code=883735010','magnesium')
    global df_CRP
    df_CRP=extract_blood_chem('Test_Code=886141010','CRP')
    global df_albumin    
    df_albumin=extract_blood_chem('Test_Code=882040010','albumin')
    global df_bilirubin    
    df_bilirubin=extract_blood_chem('Test_Code=882248010 OR Test_Code=802086010 OR Test_Code=882247010','bilirubin') 
    global df_creatinine    
    df_creatinine=extract_blood_chem('Test_Code=882565010','creatinine')  
    global df_potassium    
    df_potassium=extract_blood_chem('Test_Code=884132010','potassium')  
    global df_sodium
    df_sodium=extract_blood_chem('Test_Code=884295010','sodium')  
    global df_glucose    
    df_glucose=extract_blood_chem('Test_Code=882947010','glucose')  
    global df_BUN
    df_BUN=extract_blood_chem('Test_Code=802021010 OR Test_Code=1802021010','BUN')  
    print("full")
    return df_globulin,df_lipase,df_iron,df_ferritin,df_transferrin,df_transferin_saturation,
    df_LDL,df_HDL,df_triglycerides,df_BNP,df_troponin,
    df_ethanol,df_TSH, df_T4,
    df_protein_total,df_amylase,df_LD,
    df_uric_acid,df_GGT,
    df_alkaline_phos,df_AST,
    df_chloride,df_GPT,
    df_phosphorus,df_CPK,
    df_magnesium,df_CRP,
    df_albumin,df_bilirubin,
    df_creatinine, df_potassium,
    df_sodium,df_glucose,df_BUN


###################################################################################


def get_blood_chem(l_casenum,is_full): 
    
    if is_full=="full":
        get_blood_chem_full()
    
    frames=[
    df_globulin,
    df_lipase,
    df_iron,
    df_ferritin,
    df_transferrin,
    df_transferin_saturation,
    df_LDL,
    df_HDL,
    df_triglycerides,
    df_BNP,
    df_troponin,
    df_ethanol,
    df_TSH,
    df_T4,
    df_protein_total,
    df_amylase,
    df_LD,
    df_uric_acid,
    df_GGT,
    df_alkaline_phos,
    df_AST,
    df_chloride,
    df_GPT,
    df_phosphorus,
    df_CPK,
    df_magnesium,
    df_CRP,
    df_albumin,
    df_bilirubin,
    df_creatinine,
    df_potassium,
    df_sodium,
    df_glucose, 
    df_BUN]
  
    names=["globulin",
    "lipase",
    "iron",
    "ferritin",
    "transferrin",
    "transferin_saturation",
    "LDL",
    "HDL",
    "triglycerides",
    "BNP",
    "troponin",
    "ethanol",
    "TSH",
    "T4",
    "protein_total",
    "amylase",
    "LD",
    "uric_acid",
    "GGT",
    "alkaline_phos",
    "AST",
    "chloride",
    "GPT",
    "phosphorus",
    "CPK",
    "magnesium",
    "CRP",
    "albumin",
    "bilirubin",
    "creatinine",
    "potassium",
    "sodium",
    "glucose", 
    "BUN"]  
    
    if len(l_casenum) > 0:
        for i in range(len(frames)):
            frames[i]=frames[i][frames[i]['CaseNum'].isin(l_casenum)]
            frames[i].to_pickle(output_path+names[i]+"_pop.pkl")
   
#df=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\preprocessed\population\df_readmin_with_labels_base.pkl")       
#l_casenum=df["CaseNum"]  
#get_blood_chem(l_casenum,"full")           
##df=pd.read_pickle(r"C:\Users\orlyk\readmissions\project\preprocessed\population\df_readmin_with_labels_base.pkl")       
##l_casenum=df["CaseNum"]  
##get_blood_count(l_casenum,"full")   



#todo: check lit for icteric index, hemolytic index, lipemic index