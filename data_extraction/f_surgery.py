# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 15:45:45 2021

@author: orlyk
"""

import pyodbc
import pandas as pd
import os



global global_path_processes_file_pop
global_path_processes_file_pop = r"O:\OrlI\readmissions\preprocessed\surgery\df_surgery_pop.pkl"




def f_get_connection(s_data_base):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                 "Server=BIDWHPRD;"
                                 "Database=" + s_data_base + ";"
                                 "Trusted_Connection=yes;")
    return cnxn

def f_get_surgery_full():
    s_columns = ''' [ServSqNum]
      ,[CaseNum]
      ,[PatNum]     
      ,[SurgeryStartDate]     
      ,[SesiaFLG]

     
      ,[UrgencyFLG]     
   
      ,[IsAdmissionsUrgentFLG]     
      ,[UrgencyType],[SurgeryTypes]
     
     '''
     #[ExecutionDtTm]
    
    
    s_table = 'FACT_Surgeries'
    s_dwh = 'Surgery DM'
    s_query = 'SELECT DISTINCT' + s_columns + ' FROM ' + s_table 
    cnxn = f_get_connection(s_dwh)
    df = pd.read_sql(s_query, cnxn)
    #df_cases.to_pickle(global_path_dwh_table)
    return df

def f_get_surgery(l_casenum=[]):
    df=f_get_surgery_full()
    if len(l_casenum) > 0:
        df = df[df['CaseNum'].isin(l_casenum)]
        df.to_pickle(global_path_processes_file_pop)
        #df.to_csv(global_path_processes_file_pop_csv)






#df=f_get_surgery_full()
#urgency_type_d = {1: 'elective', 2: 'urgent', 3: 'sessia'}
#df['urgency_type_cat'] = df['UrgencyType'].map(urgency_type_d)
#
#surgery_type_d= {1: 'morning', 2: 'toranut', 3: 'sessia'}
#df['surgery_type_cat'] = df['SurgeryTypes'].map(surgery_type_d)
#
#df=df.sort_values(by='SurgeryStartDate', ascending=True)
##df=df.drop_duplicates()
#
#df=pd.merge(l_casenum,df,on="CaseNum",how="left")



