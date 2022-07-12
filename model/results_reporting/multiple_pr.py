# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 18:28:33 2021

@author: orlyk
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 16:21:52 2021

@author: orlyk
"""





from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import auc
from sklearn.metrics import roc_curve
from sklearn.metrics import precision_recall_curve

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
#pio.renderers.default = 'svg'
pio.renderers.default = 'browser'
import matplotlib.pyplot as plt




#RF
test0=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\rf_model_with_counts\probs\test_0.csv')
test1=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\rf_model_with_counts\probs\test_1.csv')
test2=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\rf_model_with_counts\probs\test_2.csv')
test3=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\rf_model_with_counts\probs\test_3.csv')
test4=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\rf_model_with_counts\probs\test_4.csv')
frames_RF=[test0,test1,test2,test3,test4]

#LR
test0=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\LR_l1_with_counts\probs\test_0.csv')
test1=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\LR_l1_with_counts\probs\test_1.csv')
test2=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\LR_l1_with_counts\probs\test_2.csv')
test3=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\LR_l1_with_counts\probs\test_3.csv')
test4=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\LR_l1_with_counts\probs\test_4.csv')
frames_LR=[test0,test1,test2,test3,test4]

#xgb
test0=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\xgb_with_counts\probs\test_0.csv')
test1=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\xgb_with_counts\probs\test_1.csv')
test2=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\xgb_with_counts\probs\test_2.csv')
test3=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\xgb_with_counts\probs\test_3.csv')
test4=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\xgb_with_counts\probs\test_4.csv')
frames_xgb=[test0,test1,test2,test3,test4]

#HS
test0=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\HS_fixed_POP\probs\test_0.csv')
test1=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\HS_fixed_POP\probs\test_1.csv')
test2=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\HS_fixed_POP\probs\test_2.csv')
test3=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\HS_fixed_POP\probs\test_3.csv')
test4=pd.read_csv(r'O:\OrlI\readmissions\model_results\for_report\HS_fixed_POP\probs\test_4.csv')
frames_HS=[test0,test1,test2,test3,test4]

plt.figure(figsize=(7, 7))

frames=[frames_RF,frames_LR,frames_xgb,frames_HS]
names=["RF","LR","xgb","HS"]

for i in range(len(frames)):
    
    logit_roc_auc=[]
    percision=pd.DataFrame()
    recall=pd.DataFrame()
    auc_score=pd.DataFrame()
    for cv in frames[i]:
        logit_roc_auc1=roc_auc_score(cv.iloc[:,0], cv.iloc[:,1])
        logit_roc_auc1=pd.Series(logit_roc_auc1)
        percision1, recall1,thresholds1 = precision_recall_curve (cv.iloc[:,0], cv.iloc[:,1])
        percision1=pd.Series(percision1, name="fpr")
        recall1=pd.Series(recall1, name="tpr")
        auc_score1 = auc(recall1, percision1)
        auc_score1=pd.Series(auc_score1, name="auc")
    
        #auc_score.append(auc_score1)
        percision=pd.concat([percision,percision1], axis=1)
        recall=pd.concat([recall,recall1], axis=1)
        auc_score=pd.concat([auc_score,auc_score1],axis=1)
    
        
        
    
        
    recall_mean=recall.mean(axis=1)
    percision_mean=percision.mean(axis=1)
    auc_mean=auc_score.mean(axis=1)
    auc_mean=round(auc_mean.loc[0],2)
        
    plt.plot (recall_mean, percision_mean, label='AUC '+ names[i] +' = ' +str(auc_mean))
    
    plt.xlabel ('Recall')
    plt.ylabel ('Percision')
    
    #plt.title ('Receiver operating characteristic')
    plt.legend (loc="upper right")


plt.savefig(r'O:\OrlI\readmissions\report\figures\roc_pr_full_model.png') 



#full model auc_pr

probs=pd.read_csv(r"O:\OrlI\readmissions\model_results\for_report\final_LR_model_\probs\probs_all.csv")
label=pd.read_csv(r"O:\OrlI\readmissions\model_results\for_report\final_LR_model_\probs\y.csv")

    
logit_roc_auc1=roc_auc_score(label, probs)
logit_roc_auc1=pd.Series(logit_roc_auc1)
percision1, recall1,thresholds1 = precision_recall_curve (label, probs)
percision1=pd.Series(percision1, name="fpr")
recall1=pd.Series(recall1, name="tpr")
auc_score1 = round(auc(recall1, percision1),2)
#auc_score1=round(pd.Series(auc_score1, name="auc"),2)



plt.plot (recall1, percision1, label='AUC '+ ' = ' +str(auc_score1))

plt.xlabel ('Recall')
plt.ylabel ('Percision')

#plt.title ('Receiver operating characteristic')
plt.legend (loc="upper right")   
plt.savefig(r'O:\OrlI\readmissions\model_results\for_report\results\pr_curve_full_model.png') 
      
    
#full model compared to HS     
probs=pd.read_csv(r"O:\OrlI\readmissions\model_results\for_report\final_LR_model_\probs\probs_all.csv")
label=pd.read_csv(r"O:\OrlI\readmissions\model_results\for_report\final_LR_model_\probs\y.csv")
    
probs_HS=pd.read_csv(r"O:\OrlI\readmissions\model_results\for_report\final_HS_model\probs\probs_all.csv")
label_HS=pd.read_csv(r"O:\OrlI\readmissions\model_results\for_report\final_HS_model\probs\y.csv")

    
logit_roc_auc1=roc_auc_score(label, probs)
logit_roc_auc1=pd.Series(logit_roc_auc1)
percision1, recall1,thresholds1 = precision_recall_curve (label, probs)
percision1=pd.Series(percision1, name="fpr")
recall1=pd.Series(recall1, name="tpr")
auc_score1 = round(auc(recall1, percision1),2)
#auc_score1=round(pd.Series(auc_score1, name="auc"),2)
plt.plot (recall1, percision1, label='AUC '+ ' = ' +str(auc_score1))



logit_roc_auc2=roc_auc_score(label_HS, probs_HS)
logit_roc_auc2=pd.Series(logit_roc_auc2)
percision2, recall2,thresholds2 = precision_recall_curve (label_HS, probs_HS)
percision2=pd.Series(percision2, name="fpr")
recall2=pd.Series(recall2, name="tpr")
auc_score2 = round(auc(recall2, percision2),2)
#auc_score1=round(pd.Series(auc_score1, name="auc"),2)
plt.plot (recall2, percision2, label='AUC '+ ' = ' +str(auc_score2))



plt.xlabel ('Recall')
plt.ylabel ('Percision')

#plt.title ('Receiver operating characteristic')
plt.legend (loc="upper right")   


