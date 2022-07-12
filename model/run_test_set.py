# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 12:58:31 2022

@author: orlyk
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 16:17:20 2021

@author: orlyk
"""
""" 
run test set on final logistic regression compact model (21 features)
loads imputation (as was done on the training data), 
 scaling (as was done on the training data) and LR model.
 provides classification metrics
 
 final logistic regression model is here: 
     O:\OrlI\readmissions\code\compact_model_final\finalized_model
 """


import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.impute import KNNImputer
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from collections import Counter
#from imblearn.over_sampling import SMOTE
#from imblearn.under_sampling import RandomUnderSampler
from functions.helper_functions import *
#from feature_selection import feature_selection_func
#from feature_selection import feature_selection_l1
import xgboost
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GroupKFold
import shap
#from feature_selection_SHAP import feature_selection_shap
from sklearn.metrics import plot_roc_curve
from sklearn.metrics import auc
from functions.filter_input import filter_input
from functions.feature_selection_methods import * 
from functions.impute_input import *
#from functions.over_under_sample import run_over_under_sample
from functions.scale_input import run_scaler
from functions.classification_metrics import *
from functions.helpers.get_catagorical import *
from datetime import datetime

from functions.prediction_algo  import *
from pickle import load


path_final_model="O:/OrlI/readmissions/code/compact_model_final/finalized_model/"

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
os.mkdir(path + '/coefs' )
os.mkdir(path + '/coefs'+"/coefs_figures" )

df_test=pd.read_csv(r'O:\OrlI\readmissions\code\compact_model_final\df_test.csv')

y=df_test["LABEL_HOSP"]
x=df_test.drop(columns=['LABEL_HOSP','PatNum'])
features=list(x.columns)    

#impute
imputer = load(open(path_final_model+"/imputer.pkl", "rb"))
x =pd.DataFrame(imputer.transform(x), columns = features)

#scaling
scaler=load(open(path_final_model+'/scaler.pkl', 'rb'))
x=pd.DataFrame(scaler.transform(x), columns =features)

#load and run model:
loaded_model = load(open(path_final_model+'/finalized_model_LR_l1.pkl', 'rb'))

y_pred_loaded = loaded_model.predict(x)
y_proba_loaded = loaded_model.predict_proba(x)
y_proba_loaded=pd.DataFrame(y_proba_loaded[:,1])

y_proba_loaded.to_excel(path + '/probs'+'/probs.xlsx')
y.to_excel(path + '/probs'+'/y_actual.xlsx')



coeffs=loaded_model.coef_
coeffs=np.transpose(coeffs)
dff = pd.DataFrame(data=coeffs)
dff=dff.rename(columns={0: "coeffs"})
dff["features"]=pd.Series(features,name="feature")
dff=dff.reindex(dff["coeffs"].abs().sort_values(ascending=False).index)
dff.to_csv(path+"/coefs/coefs_list.csv")#,index=False)




def make_roc(y_test, y_pred,probs_test):
    plt.figure(figsize=(5,5))
    logit_roc_auc1 = roc_auc_score (y_test, probs_test)
    fpr1, tpr1, thresholds1 = roc_curve (y_test, probs_test)
    plt.plot (fpr1, tpr1, label='AUC   = %0.2f' % logit_roc_auc1)
      
    
    plt.plot ([0, 1], [0, 1], 'r--')
    plt.xlim ([0.0, 1.0])
    plt.ylim ([0.0, 1.05])
    plt.xlabel ('False Positive Rate')
    plt.ylabel ('True Positive Rate')
    #plt.title ('Receiver operating characteristic')
    plt.legend (loc="lower right")
    plt.savefig(path + '/metrics/curve_figures'+'/roc_auc_.png') 
    plt.figure()
    
def report_metrics(y_test, y_pred,probs_test):

    cm = confusion_matrix(y_test, y_pred)
    tn=cm[0][0]
    fp=cm[0][1]
    fn=cm[1][0]   
    tp=cm[1][1]    
    sensitivity_recall=round(tp/(tp+fn),2)#.round(2)
    specificity=round(tn/(tn+fp),2)
    ppv=round(tp/(tp+fp),2)
    f1=round(2*tp/(2*tp+fp+fn),2)
    auc_test = round(roc_auc_score(y_test, probs_test),3)
    accuracy=round(accuracy_score(y_test, y_pred),2) * 100
    lr_precision, lr_recall,_ = precision_recall_curve(y_test, probs_test)
    pr_auc=auc(lr_recall, lr_precision)
    
    print("ROC AUC test = "+str(auc_test))
    print("accuracy score = "+str(accuracy))
    print("RP AUC = " +str(pr_auc))
    
    print("confusion matrix: ")
    print(cm)
    print("---------------------------------")
    print('sensitivity/recall = '+str(sensitivity_recall))
    print('specificity = '+str(specificity))
    print('ppv = '+str(ppv))
    print('f1 = '+str(f1))
    
    make_roc(y_test, y_pred,probs_test)
    df_metrics=pd.Series(["AUC","sensitivity","specificity","ppv","f1","accuracy","pr_auc"],name="metric")
    df_metrics_temp=pd.Series([auc_test,sensitivity_recall,
                               specificity,ppv,f1,accuracy,pr_auc],name="value")
    df_metrics=pd.concat([df_metrics,df_metrics_temp], axis=1)
    return df_metrics

df_metrics=report_metrics(y,y_pred_loaded,y_proba_loaded)
df_metrics.to_csv(path + '/metrics/test_metrics.csv')

    
