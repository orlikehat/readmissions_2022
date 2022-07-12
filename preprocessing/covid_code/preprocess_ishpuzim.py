# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 12:07:40 2021

@author: orlyk
"""
import pandas as pd
import numpy as np
def f_preprocess_ishpuzim():

    df=pd.read_pickle(r"O:/OrlI/readmissions/preprocessed/ishpuzim_indicators/df_ishpuzim_pop_covid.pkl")
    
    #quarters admitted/discharged
    df['EnterQuarterDesc'] = df['EnterQuarterDesc'].str[:2]
    df['ExitQuarterDesc'] = df['ExitQuarterDesc'].str[:2]
    
    #dummies
    #df=pd.get_dummies(data=df, columns=['ExitEndOfWeekFLG','KupaCode','EnterQuarterDesc',
    #                                    'ExitQuarterDesc'])
    
    #isreali born or other
    df["oleh"]=np.where(df["EngCountryName"]=="Israel",0,1)
    
  
    #drop unessecary
    df=df.drop(columns=['First_Sodium_Value','PatNum','BirthCountry',
                        'CountryID','EngCountryName'])
    
    
    df.to_pickle(r"O:\OrlI\readmissions\preprocessed\ishpuzim_indicators\ishpuzim_for_model\ishpuzim_preprocessed_covid.pkl")
    
    return df