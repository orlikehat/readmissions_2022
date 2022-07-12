# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 13:18:01 2022

@author: orlyk
"""

"""
short version of model development.
includes cross validation and differnt choices for 
imputation, scaling and ML algo (see filtering_params.csv)
final compact model (as reported in the report for המכון הלאומי) ן)
 is a logistic regression (saved in:
 O:\OrlI\readmissions\code\compact_model_final\finalized_model)
   
"""
import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.model_selection import GroupKFold

import shap

from functions.scale_input import run_scaler
from functions.classification_metrics import *
from functions.helpers.get_catagorical import *
from functions.prediction_algo  import *
from functions.impute_input import *

from datetime import datetime


global output_path
output_path="O:/OrlI/readmissions/code/compact_model_final/results/" 
#create folder output folder
directory=datetime.today().strftime('%d-%m-%y - %H%M')
global path
path = os.path.join(output_path, directory) 
os.mkdir(path)

#create sub-folders 
os.mkdir(path + '/metrics')
os.mkdir(path + '/metrics' + "/curve_figures")
os.mkdir(path + '/probs')
os.mkdir(path + '/SHAP')
os.mkdir(path + '/SHAP' + "/SHAP_figures")
os.mkdir(path + '/features')
os.mkdir(path + '/coefs' )
os.mkdir(path + '/coefs'+"/coefs_figures" )

#load filtering params
filtering_params_df=pd.read_csv(r"O:\OrlI\readmissions\code\compact_model_final\code\filtering_params.csv")
global filtering_params
filtering_params=dict(zip(list(filtering_params_df.condition), list(filtering_params_df.value)))


df_train=pd.read_csv(r'O:\OrlI\readmissions\code\compact_model_final\df_train.csv')


y=df_train["LABEL_HOSP"]
x=df_train.drop(columns=['LABEL_HOSP'])

patnums=x["PatNum"]
x=x.drop(columns=['PatNum'])   
features=features=list(x.columns)

#cross validation - making sure same patnum is either in training or validation
gkf = list(GroupKFold(n_splits=int(filtering_params['cv']) ).split(x,y,patnums))
indx=[x[1] for x in gkf]

#initiate
probs_test_df=pd.DataFrame()
probs_train_df=pd.DataFrame()
roc_auc_s =pd.Series()
roc_auc_train_s =pd.Series()
sensitivity_s=pd.Series()
specificity_s=pd.Series()
ppv_s=pd.Series()
f1_s=pd.Series()
pr_auc_s=pd.Series()  
shap_values_mat=np.empty([0,x.shape[1]])
X_importance_mat=pd.DataFrame()
importance_contcat=pd.DataFrame()
features_combined=pd.DataFrame()          
    
if int(filtering_params['cv'])>0: 
    for i in range(len(indx)):  
        x_test=x.iloc[indx[i]]
        x_test_ind=list(x_test.index)
        x_train=x.loc[~x.index.isin(x_test_ind)]
        
        y_test=y.iloc[indx[i]]
        y_test_ind=list(y_test.index)
        y_train=y.loc[~y.index.isin(y_test_ind)]
        
        #imputation
        x_train,x_test=run_impute(x_train,x_test,path)
               
        # scale
        x_train, x_test=run_scaler(x_train,x_test,path)
       
        #train_model 
        train_model, model,y_pred,probs_test,probs_train=run_prediction_model(x_train, y_train,x_test,y_test,path)
              
        #calssification metrics
        sensitivity_recall,specificity,ppv,f1,auc_test,auc_train,accuracy,pr_auc=report_metrics(y_train,y_test, y_pred,probs_train,probs_test,i)                    
                                                                                         
        
        specificity_s,specificity_mean=summarize_metrics(specificity,specificity_s)
        sensitivity_s,sensitivity_mean=summarize_metrics(sensitivity_recall,sensitivity_s)
        ppv_s,ppv_mean=summarize_metrics(ppv,ppv_s)
        f1_s,f1_mean=summarize_metrics(f1,f1_s)
        roc_auc_s,roc_auc_mean=summarize_metrics(auc_test,roc_auc_s)
        roc_auc_train_s,roc_auc_train_mean=summarize_metrics(auc_train,roc_auc_train_s)
        pr_auc_s,pr_auc_mean=summarize_metrics(pr_auc,pr_auc_s)
        
        if filtering_params['algo']=='xgb':
         
            X_importance=pd.DataFrame(x_test,columns=features)
            X_importance_mat=pd.concat([X_importance_mat,X_importance])
            explainer = shap.TreeExplainer(train_model)
            shap_values = explainer.shap_values(X_importance)
            
            shap.summary_plot(shap_values, X_importance)
            plt.savefig(path + '/SHAP/SHAP_figures/SHAP_swarm_'+str(i)+".png") 
            plt.figure()
            shap.summary_plot(shap_values, X_importance, plot_type='bar')
            plt.savefig(path + '/SHAP/SHAP_figures/SHAP_bar_'+str(i)+".png") 
            plt.figure()
            
            shap_sum = np.abs(shap_values).mean(axis=0)
            importance_df = pd.DataFrame([X_importance.columns.tolist(), shap_sum.tolist()]).T
            importance_df.columns = ['column_name', 'shap_importance']
            importance_contcat=pd.concat([importance_contcat,importance_df],axis=1)
 
                       
            importance_df.to_csv(path+"/SHAP/SHAP_importance_list"+str(i)+".csv",index=False)
            importance_contcat.to_csv(path+"/SHAP/shap_all_iter.csv",index=False)
            plt.figure( )

    
                  
        if filtering_params['algo']=='LR_l1':
            print("Non Zero weights:", np.count_nonzero(train_model.coef_))
            coeffs=train_model.coef_
            coeffs=np.transpose(coeffs)


            dff = pd.DataFrame(data=coeffs)

            print(dff.shape)
            dff = pd.DataFrame(data=coeffs,index=features)
            dff=dff.rename(columns={0: "coeffs"})
            
            dff=dff.reindex(dff["coeffs"].abs().sort_values(ascending=False).index)
            importance_contcat=pd.concat([importance_contcat,dff],axis=1)

            dff.to_csv(path+"/coefs/coefs_list"+str(i)+".csv")#,index=False)
            importance_contcat.to_csv(path+"/coefs/coefs_all_iter.csv")#,index=False)
            
            plt.figure( )
            sns.barplot(x=dff["coeffs"], y=dff.index)
            plt.title("LR coefficients")
            plt.savefig(path + '/coefs/coefs_figures'+"/LR_coeffs.png") 
            plt.figure( )

        elif filtering_params['algo']=='RF':
            fi = pd.DataFrame({'feature': list(x_train.columns),
                   'importance': model.feature_importances_}).\
                    sort_values('importance', ascending = False)

            # Display
            fi.head(60)
            importance20=fi.head(20)
            plt.figure(figsize=(8,10))
            
            ax = sns.barplot(x="importance", y="feature", data=importance20,color="steelblue")

            plt.figure( )
        
 
       
        
        probs_test=pd.DataFrame(probs_test)
        probs_test=probs_test.rename(columns={0: "prob_test"})
        y_test_tmp=y_test.reset_index().drop(["index"], axis=1)
        probs_test=pd.merge(y_test_tmp,probs_test,left_index=True, right_index=True)
        probs_test.to_csv(path+"/probs/test_"+str(i)+".csv",index=False)
    
    
        probs_test_df=pd.concat([probs_test_df, probs_test],axis=0)
        
        probs_train=pd.DataFrame(probs_train)
        probs_train=probs_train.rename(columns={0: "prob_train"})
        y_train_tmp=y_train.reset_index().drop(["index"], axis=1)
        probs_train=pd.merge(y_train_tmp,probs_train,left_index=True, right_index=True)
        probs_train.to_csv(path+"/probs/train_"+str(i)+".csv",index=False)
        probs_train_df=pd.concat([probs_train_df, probs_train],axis=0)
        
           

        
        
    
    
    #create final metrics df
    metrics_df=create_metrics_df(roc_auc_train_s,roc_auc_s,sensitivity_s,
                                 specificity_s,ppv_s,f1_s,pr_auc_s,
                                 roc_auc_train_mean,roc_auc_mean,sensitivity_mean,
                                 specificity_mean,ppv_mean,f1_mean,pr_auc_mean)    
        
     
    #create final roc curves 
    plt.figure(figsize=(6,6))
    logit_roc_auc1 = roc_auc_score (probs_test_df.iloc[:,0], probs_test_df.iloc[:,1])
    fpr1, tpr1, thresholds1 = roc_curve (probs_test_df.iloc[:,0], probs_test_df.iloc[:,1])
    plt.plot (fpr1, tpr1, label='AUC   = %0.2f' % logit_roc_auc1)
       
    logit_roc_auc2 = roc_auc_score (probs_train_df.iloc[:,0], probs_train_df.iloc[:,1])
    fpr1, tpr1, thresholds1 = roc_curve (probs_train_df.iloc[:,0], probs_train_df.iloc[:,1])
    plt.plot (fpr1, tpr1, label='AUC   = %0.2f' % logit_roc_auc2)
       
    
    plt.plot ([0, 1], [0, 1], 'r--')
    plt.xlim ([0.0, 1.0])
    plt.ylim ([0.0, 1.05])
    plt.xlabel ('False Positive Rate')
    plt.ylabel ('True Positive Rate')
    #plt.title ('Receiver operating characteristic')
    plt.legend (loc="lower right")
    plt.savefig(path + '/metrics/curve_figures'+"/roc_auc_all.png") 
    plt.figure()
    
    #write to file
    filtering_params_df.to_excel(path+"/filtering_params.xlsx",index=False)
    metrics_df.to_excel(path+"/metrics/classification_metrics.xlsx",index=False)
    probs_test_df.to_excel(path+"/probs/probs_test_all.xlsx",index=False)
    
    
    
        
                    