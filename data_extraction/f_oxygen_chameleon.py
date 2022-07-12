# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 14:20:39 2020

@author: orlyk
"""
"""
ventialtion in chameleon
provides information on CaseNums that underwent 
mechanical ventilatation outside of ICUs: casenum and date-time"""



import pandas as pd
import numpy as np
#from get_connection import f_get_connection
from pathlib import Path
import pyodbc




global output_path
output_path="O:/OrlI/readmissions/preprocessed/ventilation/oxygen_chameleon/"

def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn



def f_get_ventilation_chameleon_full():
    
    
    file = Path("C:/Users/orlyk/readmissions/ventilation/nevermind.pkl")
    if file.is_file():
        df=pd.read_pkl("C:/Users/orlyk/readmissions/ventilation/nevermind.pkl")
    else:
        
       
        mrr_monitor="""SELECT 
          [Medical_Record]
          ,[Monitor_Date]
          ,[Parameter]
          ,[Result]
         
         
      FROM [Chameleon_MRR].[dbo].[Chameleon_MRR_Monitor]
      where Parameter in (542,4898)
         """
        mrr_monitor_arch="""SELECT 
      [Medical_Record]
      ,[Monitor_Date]
      ,[Parameter]
      ,[Result]
     
         
      FROM [Chameleon_MRR].[dbo].[Chameleon_MRR_MonitorArch]
    where Parameter in (542,4898)     """
        mrr_device="""SELECT  
          [Medical_Record]
          
          ,[Monitor_Date]
          ,[Parameter]
          ,[Result]
          
      FROM [Chameleon_MRR].[dbo].[Chameleon_MRR_DeviceMonitor]
      where Parameter in (542,4898)"""
       
       
        mrr_device_arch="""SELECT  
          [Medical_Record]
          
          ,[Monitor_Date]
          ,[Parameter]
          ,[Result]
          
      FROM [Chameleon_MRR].[dbo].[Chameleon_MRR_DeviceMonitorArch]
      where Parameter in (542,4898)"""
       
           
      
        vital_signs="""SELECT   [CaseNum]
          ,[Medical_Record]
          ,[Monitor_Date]
          ,[Parameter_Name]
          ,[Parameter_EnteredValue]
          
    from [BI_Dev].[dbo].[CLN_Vital_Signals_Chameleon] 
    where Parameter_Name='SUTUR_Oxygen' """
     
        mrr_v_execution="""SELECT  [Execution_Date]
          ,[Medical_Record]
          ,[Parameter]
          ,[Result]
          
      FROM [Chameleon_MRR].[dbo].[Chameleon_MRR_V_Execution]
      where Parameter in (542,4898)"""
      
        convert_case="""SELECT Medical_Record,CaseNum
     
  FROM [DWH_PRD].[dbo].[Chameleon_Fact_MedicalRecords]"""
      
      
        cnxn_dwh_prd=f_get_connection('DWH_PRD')
        df_monitor=pd.read_sql(mrr_monitor, cnxn_dwh_prd)
        df_monitor_arch=pd.read_sql(mrr_monitor_arch, cnxn_dwh_prd)
        df_monitor_device=pd.read_sql(mrr_device, cnxn_dwh_prd)
        df_monitor_device_arch=pd.read_sql(mrr_device_arch, cnxn_dwh_prd)
        df_mrr_v_execution=pd.read_sql(mrr_v_execution, cnxn_dwh_prd)
        
        
        
        df_vital_signs=  pd.read_sql(vital_signs, cnxn_dwh_prd)
        df_casenum=pd.read_sql(convert_case, cnxn_dwh_prd)
       # df_casenum=pd.read_pickle("O:/OrlI/readmissions/ventilation/code/med_records_to_casnum.pkl")
           
            
        #mrr data
        df_mrr_v_execution=df_mrr_v_execution.rename(columns = {"Execution_Date": "Monitor_Date", 
                                      "Parameter_EnteredValue":"Result" 
                                      })    
        
        
        df_monitor=pd.merge(df_monitor,df_casenum, how="left", on="Medical_Record")
        df_monitor_arch=pd.merge(df_monitor_arch,df_casenum, how="left", on="Medical_Record")
        df_monitor_device=pd.merge(df_monitor_device,df_casenum, how="left", on="Medical_Record")
        df_monitor_device_arch=pd.merge(df_monitor_device_arch,df_casenum, how="left", on="Medical_Record")
        df_mrr_v_execution=pd.merge(df_mrr_v_execution,df_casenum, how="left", on="Medical_Record")
    
        
           
        frames=[df_monitor,df_monitor_arch,df_monitor_device,df_monitor_device_arch,df_mrr_v_execution]
        names=["monitor_chameleon","monitor_arch_chameleon","monitor_device_chameleon","monitor_device_arch_chameleon","v_exec_chameleon"]
        df= pd.DataFrame()
        for f in range(0,len(frames)):
            frames[f]=frames[f][["CaseNum","Medical_Record","Monitor_Date",
                               "Parameter","Result"]]
            frames[f]["source"]=names[f]
            frames[f].sort_values(by='Monitor_Date',ascending=True, inplace=True)
            frames[f]=frames[f].drop_duplicates(subset='CaseNum', keep='first', inplace=False)
            df=pd.concat([df,frames[f]])
            
            
       
    #    param_names= {
    #      5309: "RR_MACHINE",
    #      5311: "TV_MACHINE",
    #      327: 'PEEP'
    #    }
    #    
    #    df["parameter_name"]=df["Parameter"].map(param_names) 
    #    
        #vital signs data
        df_vital_signs = df_vital_signs.rename(columns = {"Parameter_Name": "parameter_name", 
                                      "Parameter_EnteredValue":"Result" 
                                      })    
        
        df_vital_signs["Parameter"]=df_vital_signs["parameter_name"]
        df_vital_signs["source"]="VS"
        
        df_vital_signs=df_vital_signs[["CaseNum","Medical_Record","Monitor_Date",
                               "Parameter","Result","source","parameter_name"]]
        
        
        df=pd.concat([df,df_vital_signs])
        
        df.sort_values(by='source',ascending=True, inplace=True)
       
        df.sort_values(by='Monitor_Date',ascending=True, inplace=True)
        df=df.drop_duplicates(subset='CaseNum', keep='first', inplace=False)
        
           
         #drop duplicates from different sources     
        df=df.dropna(subset=['CaseNum'])
        
        #CaseNum	PatNum	PatIdNum	Admission_id	Time	type	source
        df["type"]=""
        df=df[["CaseNum","Medical_Record","Monitor_Date","type","source"]]
         
            
       # df.to_pickle(dwr_path + "chameleon_data_oxygen_ventilation.pkl")
        return df
    
    
def get_oxygen_chameleon_pop(l_casenum=[]):
    df = f_get_ventilation_chameleon_full()
    if len(l_casenum) > 0:
        df = df[df['CaseNum'].isin(l_casenum)]
        df.to_pickle(output_path+"oxygen_support_chameleon_pop.pkl")
       # df.to_csv(output_path+"oxygen_support_chameleon_pop.csv")
       
    return df


    
    