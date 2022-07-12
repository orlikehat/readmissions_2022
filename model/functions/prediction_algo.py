# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 15:14:58 2021

@author: orlyk


"""
import pandas as pd
import numpy as np
import xgboost
from catboost import CatBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import pickle




from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt




def run_prediction_model(x_train, y_train,x_test,y_test, path):
    filtering_params=pd.read_csv(r"O:\OrlI\readmissions\code\prediction_models\functions\filtering_params.csv")
    filtering_params=dict(zip(list(filtering_params.condition), list(filtering_params.value)))
    
    if filtering_params['algo']=="xgb":
        print("run XGB model") 
     
        model = xgboost.XGBClassifier(subsample= 0.7, seed= 1001, scale_pos_weight= 6,
                                      min_child_weight= 5, max_depth= 8, learning_rate= 0.01, gamma= 0.5, colsample_bytree= 0.6)
               
        train_model = model.fit(x_train, y_train)
        
        y_pred = model.predict(x_test)
        
            
        probs_test=train_model.predict_proba(x_test)[:, 1]
        probs_train=train_model.predict_proba(x_train)[:, 1]
        pickle.dump(model, open(path+"/finalized_model_XGB.pkl", 'wb'))    

        
        fop, mpv = calibration_curve(y_test, probs_test, n_bins=10, normalize=True)
        # plot perfectly calibrated
        plt.plot([0, 1], [0, 1], linestyle='--')
        # plot model reliability
        plt.plot(mpv, fop, marker='.')
        plt.show()
        plt.figure( )

    
        return train_model, model,y_pred,probs_test,probs_train
    
    
    elif filtering_params['algo']=="LR_l1":

        print("run LR model") 
        
        model = LogisticRegression(max_iter=2000,C= 0.01,penalty='l1',solver='saga',verbose=1, warm_start=True,class_weight='balanced')

        train_model = model.fit(x_train, y_train)
        
        y_pred = model.predict(x_test)
        
            
        probs_test=train_model.predict_proba(x_test)[:, 1]
        probs_train=train_model.predict_proba(x_train)[:, 1]
        pickle.dump(model, open(path+"/finalized_model_LR_l1.pkl", 'wb'))    

        
        fop, mpv = calibration_curve(y_test, probs_test, n_bins=10, normalize=True)
        # plot perfectly calibrated
        plt.plot([0, 1], [0, 1], linestyle='--')
        # plot model reliability
        plt.plot(mpv, fop, marker='.')
        plt.show()
        plt.figure( )

        return train_model, model,y_pred,probs_test,probs_train
    
    elif filtering_params['algo']=="RF":

        print("RF") 
     
        model = RandomForestClassifier(criterion= 'gini',max_depth= 10,max_features='auto',n_estimators=200,class_weight="balanced")

        train_model = model.fit(x_train, y_train)
        
        y_pred = model.predict(x_test)
        
            
        probs_test=train_model.predict_proba(x_test)[:, 1]
        probs_train=train_model.predict_proba(x_train)[:, 1]
        pickle.dump(model, open(path+"/finalized_model_RF.pkl", 'wb'))    

        
        fop, mpv = calibration_curve(y_test, probs_test, n_bins=10, normalize=True)
        # plot perfectly calibrated
        plt.plot([0, 1], [0, 1], linestyle='--')
        # plot model reliability
        plt.plot(mpv, fop, marker='.')
        plt.show()
    
        return train_model, model,y_pred,probs_test,probs_train
    
      
        
    elif filtering_params['algo']=="MLP":
        print("run MLP")
        model = MLPClassifier(solver='adam', alpha=1e-5,hidden_layer_sizes=(25, 15, 5), random_state=1,max_iter=1000)
        
        train_model = model.fit(x_train, y_train)
        
        y_pred = model.predict(x_test)
        
            
        probs_test=train_model.predict_proba(x_test)[:, 1]
        probs_train=train_model.predict_proba(x_train)[:, 1]
        
        
        fop, mpv = calibration_curve(y_test, probs_test, n_bins=10, normalize=True)
        # plot perfectly calibrated
        plt.plot([0, 1], [0, 1], linestyle='--')
        # plot model reliability
        plt.plot(mpv, fop, marker='.')
        plt.show()
    
        return train_model, model,y_pred,probs_test,probs_train

    elif filtering_params['algo']=="NB":
        print("run NB")
        model =  GaussianNB()
        
        train_model = model.fit(x_train, y_train)
        
        y_pred = model.predict(x_test)
        
            
        probs_test=train_model.predict_proba(x_test)[:, 1]
        probs_train=train_model.predict_proba(x_train)[:, 1]
        
        
        fop, mpv = calibration_curve(y_test, probs_test, n_bins=10, normalize=True)
        # plot perfectly calibrated
        plt.plot([0, 1], [0, 1], linestyle='--')
        # plot model reliability
        plt.plot(mpv, fop, marker='.')
        plt.show()
    
        return train_model, model,y_pred,probs_test,probs_train

        
   
    
    elif filtering_params['algo']=="svm":

        print("svm") 
     
        model = svm.SVC(kernel='linear',probability=True,C=0.2,class_weight="balanced")

        train_model = model.fit(x_train, y_train)
        
        y_pred = model.predict(x_test)
        
            
        probs_test=train_model.predict_proba(x_test)[:, 1]
        probs_train=train_model.predict_proba(x_train)[:, 1]
        
        
        fop, mpv = calibration_curve(y_test, probs_test, n_bins=10, normalize=True)
        # plot perfectly calibrated
        plt.plot([0, 1], [0, 1], linestyle='--')
        # plot model reliability
        plt.plot(mpv, fop, marker='.')
        plt.show()
    
        return train_model, model,y_pred,probs_test,probs_train
    


       

