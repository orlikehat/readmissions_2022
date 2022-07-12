# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:08:16 2021

@author: orlyk
"""


import pyodbc
import pandas as pd



global output_path
output_path="O:/OrlI/readmissions/preprocessed/microbiology/"


#df_microorg=pd.read_excel(r"C:\Users\orlyk\readmissions\project\code\support_files\microorg_categories.xlsx")
def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn


def get_microbiology_full():

    mic_query='''SELECT 
    labs.CaseNum,
          labs.[Order_Code]
    	  ,labs.Order_Num
    	 
    	  ,LABS.Reception_date
    	  ,LABS.Reception_time
    	  ,[Entry_Date]
          ,[Entry_Time]     
        
          ,labs.[Label]
          ,labs.[Test_Num]
          ,labs.[Result] lab_result
          ,labs.[Approval_Time]
    	  ,CAST(LABS.Test_Code AS VARCHAR(20)) as 'TestCode'
    	  ,dim.name
    	  ,Labs.First_Report_Date+Labs.First_Report_Time  ApprovalDtTM
          ,micro.[organism_code]
          ,micro.[organism_name]
          ,micro.[result] micro_result
    	  ,micro.approval_time micro_approval
    	 
    
       
    
      FROM[DWH_PRD].[dbo].[AUTODB_Labs_Fact_Tests] labs
     
      join [DWH_SRC].[dbo].[AUTODB_SRC_Microorganisms] micro
      on labs.Order_Code = micro.order_code and labs.Label = micro.label
      join [DWH_PRD].[dbo].[AUTODB_Dim_Tests] dim
      on LABS.test_code = dim.test_code
      where LABS.Department_Code not in (54,69)'''
    #  and year(Reception_date) >= 2015'''
      
      
    cnxn_dwh_prd=f_get_connection('DWH_PRD')
    df=pd.read_sql(mic_query, cnxn_dwh_prd)
    
    
    df=df[["CaseNum","ApprovalDtTM","organism_code","organism_name","micro_approval"]]
    
    df_short=df.drop_duplicates()
  
   # df_short=pd.merge(df_short,df_microorg,on="organism_code",how="left")
   # df_short=df_short.drop(columns=['organism_name_y'])
   # df_short=df_short.rename(columns={"organism_name_x": "organism_name"})
    #up to here there could be several rows for each patient = several microorganisms
    

    
    return df_short


def get_microbiology(l_casenum):
     df=get_microbiology_full()
     if len(l_casenum) > 0:
        df = df[df['CaseNum'].isin(l_casenum)]
        df.to_pickle(output_path+"microbiology_pop.pkl")

        








