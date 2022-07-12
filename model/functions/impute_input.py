# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 10:11:45 2021

@author: orlyk
"""

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer
import pickle

def run_impute(x_train,x_test,path):
    filtering_params=pd.read_csv(r"O:\OrlI\readmissions\code\prediction_models\functions\filtering_params.csv")
    filtering_params=dict(zip(list(filtering_params.condition), list(filtering_params.value)))
    
    if filtering_params['impute']=="simple" or filtering_params['algo']=="cat":
        print("median imputation")
        #x_train=pd.DataFrame(SimpleImputer(strategy='median').fit_transform(x_train), columns = x_train.columns)
        my_imputer = SimpleImputer(strategy='median')
        x_train=pd.DataFrame(my_imputer.fit_transform(x_train), columns = x_train.columns)
        x_test=pd.DataFrame(my_imputer.transform(x_test), columns = x_test.columns)
        pickle.dump(my_imputer, open(path+'/imputer.pkl', 'wb'))  

    elif filtering_params['impute']=="most_frequent" :
#      
        print("most frequent imputation")
        my_imputer = SimpleImputer(strategy='most_frequent')
        x_train=pd.DataFrame(my_imputer.fit_transform(x_train), columns = x_train.columns)
             
        x_test=pd.DataFrame(my_imputer.transform(x_test), columns = x_test.columns)
            
        
    elif filtering_params['impute']=="knn" :
        print("knn imputation")
        
        my_imputer = KNNImputer(n_neighbors=2, weights="uniform")
        x_train=pd.DataFrame(my_imputer.fit_transform(x_train), columns = x_train.columns)
        x_test=pd.DataFrame(my_imputer.transform(x_test), columns = x_test.columns)
        
     
    else:
        print("no imputation")
        
    return x_train,x_test
