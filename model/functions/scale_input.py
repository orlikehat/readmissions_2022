# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 11:02:56 2021

@author: orlyk
"""
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
import pickle


def run_scaler(x_train,x_test,path):
    filtering_params=pd.read_csv(r"O:\OrlI\readmissions\code\prediction_models\functions\filtering_params.csv")
    filtering_params=dict(zip(list(filtering_params.condition), list(filtering_params.value)))
   
    if filtering_params['scale']=="standard":
        print("run standard scaler")
#       
        scaler = StandardScaler()
        x_train=pd.DataFrame(scaler.fit_transform(x_train), columns = x_train.columns)
              
        x_test=pd.DataFrame(scaler.transform(x_test), columns = x_test.columns)
        pickle.dump(scaler, open(path+'/scaler.pkl', 'wb'))  

    
    elif filtering_params['scale']=="robust":
        print("run robust scaler")
#      
        scaler = RobustScaler()
        x_train=pd.DataFrame(scaler.fit_transform(x_train), columns = x_train.columns)
              
        x_test=pd.DataFrame(scaler.transform(x_test), columns = x_test.columns)
        
        
    else:
        print("no scaling")
        
        
    return x_train, x_test
        
        
    