# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:44:34 2021

@author: orlyk
"""
import pandas as pd

from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import auc
from sklearn.metrics import roc_curve


import matplotlib.pyplot as plt

def make_roc(y_train,y_pred,probs_train):
    plt.figure(figsize=(6,6))
    
    logit_roc_auc2 = roc_auc_score (y_train, probs_train)
    fpr1, tpr1, thresholds1 = roc_curve (y_train, probs_train)
    plt.plot (fpr1, tpr1, label='AUC   = %0.2f' % logit_roc_auc2)
   
    
    plt.plot ([0, 1], [0, 1], 'r--')
    plt.xlim ([0.0, 1.0])
    plt.ylim ([0.0, 1.05])
    plt.xlabel ('False Positive Rate')
    plt.ylabel ('True Positive Rate')
    #plt.title ('Receiver operating characteristic')
    plt.legend (loc="lower right")
   # plt.savefig(path + '/metrics/curve_figures'+'/roc_auc_'+str(i)+".png") 
    plt.figure()
    
    
    
    
def report_metrics(y_train, y_pred,probs_train):
    cm = confusion_matrix(y_train, y_pred)
    tn=cm[0][0]
    fp=cm[0][1]
    fn=cm[1][0]   
    tp=cm[1][1]    
    sensitivity_recall=round(tp/(tp+fn),2)#.round(2)
    specificity=round(tn/(tn+fp),2)
    ppv=round(tp/(tp+fp),2)
    f1=round(2*tp/(2*tp+fp+fn),2)
    auc_train = round(roc_auc_score(y_train, probs_train),3)
    lr_precision, lr_recall,_ = precision_recall_curve(y_train, probs_train)
    pr_auc=auc(lr_recall, lr_precision)
    
    print("ROC AUC train = "+str(auc_train))
    print("confusion matrix: ")
    print(cm)
    print("---------------------------------")
    print('sensitivity/recall = '+str(sensitivity_recall))
    print('specificity = '+str(specificity))
    print('ppv = '+str(ppv))
    print('f1 = '+str(f1))
    
    make_roc(y_train,y_pred,probs_train)
    
    return(sensitivity_recall,specificity,ppv,f1,auc_train)
    
    
def summarize_metrics(param,param_s):
    param=pd.Series(param)
    param_s=pd.concat([param_s, param],axis=0)
    param_s=param_s.reset_index()
    param_s=param_s.drop(['index'], axis=1)
    param_mean=param_s.mean()
    
    return param_s,param_mean


def create_metrics_df(roc_auc_train_s,roc_auc_s,sensitivity_s,
                             specificity_s,ppv_s,f1_s,pr_auc_s,
                             roc_auc_train_mean,roc_auc_mean,sensitivity_mean,
                             specificity_mean,ppv_mean,f1_mean,pr_auc_mean):
    metrics_l=[roc_auc_train_s,roc_auc_s,sensitivity_s,specificity_s,ppv_s,f1_s,pr_auc_s]
    df_metrics = pd.concat(metrics_l, axis=1)
    df_metrics["iteration"]=df_metrics.index
    df_metrics.columns = ['auc_train', 'auc_test','sensitivity','specificity',
                          'ppv','f1','pr_auc','iteration']
    
    
    metrics_means_l=[roc_auc_train_mean,roc_auc_mean,sensitivity_mean,
                     specificity_mean,ppv_mean,f1_mean,pr_auc_mean,pd.Series('mean')]
    df_metrics_means = pd.concat(metrics_means_l, axis=1)
    df_metrics_means.columns = ['auc_train', 'auc_test','sensitivity','specificity',
                          'ppv','f1','pr_auc','iteration']
    
    df_metrics=pd.concat([df_metrics,df_metrics_means]) 
    df_metrics = df_metrics[['iteration','auc_train', 'auc_test','sensitivity','specificity',
                          'ppv','f1','pr_auc']]
    
    return df_metrics


#    







