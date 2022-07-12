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
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
#pio.renderers.default = 'svg'
pio.renderers.default = 'browser'
import matplotlib.pyplot as plt

#_____cross validation_______________

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



frames=[frames_RF,frames_LR,frames_xgb,frames_HS]
names=["RF","LR","xgb","HS"]
plt.figure(figsize=(7, 7))

for i in range(len(frames)):
    
    logit_roc_auc=pd.DataFrame()
    fpr=pd.DataFrame()
    tpr=pd.DataFrame()
    auc_score=pd.DataFrame()
    for cv in frames[i]:
        
        fpr1, tpr1,thresholds1 = roc_curve (cv.iloc[:,0], cv.iloc[:,1])
        fpr1=pd.Series(fpr1, name="fpr")
        tpr1=pd.Series(tpr1, name="tpr")
        
        logit_roc_auc1=roc_auc_score(cv.iloc[:,0], cv.iloc[:,1])
        logit_roc_auc1=pd.Series(logit_roc_auc1,name='auc_roc')
    
        #auc_score.append(auc_score1)
        fpr=pd.concat([fpr,fpr1], axis=1)
        tpr=pd.concat([tpr,tpr1], axis=1)
        logit_roc_auc=pd.concat([logit_roc_auc,logit_roc_auc1],axis=1)
    
        
        
    
        
    tpr_mean=tpr.mean(axis=1)
    fpr_mean=fpr.mean(axis=1)
    auc_mean=logit_roc_auc.mean(axis=1)
    auc_mean=round(auc_mean.loc[0],2)
    
    plt.plot (fpr_mean, tpr_mean, label='AUC '+ names[i] +' = ' +str(auc_mean))
    plt.plot ([0, 1], [0, 1], 'r--')
    plt.xlim ([0.0, 1.0])
    plt.ylim ([0.0, 1.05])
    plt.xlabel ('False Positive Rate')
    plt.ylabel ('True Positive Rate')
    #plt.title ('Receiver operating characteristic')
    plt.legend (loc="lower right")
    
plt.savefig(r'O:\OrlI\readmissions\report\figures\roc_auc_full_model.png') 


#_______________full model roc_auc____________________

probs=pd.read_csv(r"O:\OrlI\readmissions\model_results\for_report\final_LR_model_\probs\probs_all.csv")
label=pd.read_csv(r"O:\OrlI\readmissions\model_results\for_report\final_LR_model_\probs\y.csv")

    
fpr1, tpr1,thresholds1=roc_curve(label, probs)
logit_roc_auc1=round(roc_auc_score(label, probs),2)

plt.plot (fpr1, tpr1, label='AUC '+' = ' +str(logit_roc_auc1))
plt.plot ([0, 1], [0, 1], 'r--')
plt.xlim ([0.0, 1.0])
plt.ylim ([0.0, 1.05])
plt.xlabel ('False Positive Rate')
plt.ylabel ('True Positive Rate')
#plt.title ('Receiver operating characteristic')
plt.legend (loc="lower right")


plt.savefig(r'O:\OrlI\readmissions\model_results\for_report\results\roc_auc_full_model.png') 
      

#___________full/test model - compare to HS

probs=pd.read_excel(r"O:\OrlI\readmissions\model_results\test_results\internal_test_LR\probs\probs.xlsx")
label=pd.read_excel(r"O:\OrlI\readmissions\model_results\test_results\internal_test_LR\probs\y.xlsx")

probs_HS=pd.read_excel(r"O:\OrlI\readmissions\model_results\test_results\internal_test_HS\probs\probs.xlsx")
label_HS=pd.read_excel(r"O:\OrlI\readmissions\model_results\test_results\internal_test_HS\probs\y.xlsx")

probs=probs.iloc[:,1]
label=label.iloc[:,1]
probs_HS=probs_HS.iloc[:,1]
label_HS=label_HS.iloc[:,1]

fpr1, tpr1,thresholds1=roc_curve(label, probs)
logit_roc_auc1=round(roc_auc_score(label, probs),2)

plt.plot (fpr1, tpr1, label='AUC '+' = ' +str(logit_roc_auc1))
plt.plot ([0, 1], [0, 1], 'r--')
plt.xlim ([0.0, 1.0])
plt.ylim ([0.0, 1.05])
plt.xlabel ('False Positive Rate')
plt.ylabel ('True Positive Rate')
#plt.title ('Receiver operating characteristic')
plt.legend (loc="lower right")


fpr2, tpr2,thresholds1=roc_curve(label_HS, probs_HS)
logit_roc_auc2=round(roc_auc_score(label_HS, probs_HS),2)

plt.plot (fpr2, tpr2, label='AUC '+' = ' +str(logit_roc_auc2))
plt.plot ([0, 1], [0, 1], 'r--')
plt.xlim ([0.0, 1.0])
plt.ylim ([0.0, 1.05])
plt.xlabel ('False Positive Rate')
plt.ylabel ('True Positive Rate')
#plt.title ('Receiver operating characteristic')
plt.legend (loc="lower right")


#test sets

probs_internal=pd.read_excel(r"O:\OrlI\readmissions\report\results\final models\LR_full_internal_test\probs\probs.xlsx")
label_internal=pd.read_excel(r"O:\OrlI\readmissions\report\results\final models\LR_full_internal_test\probs\y.xlsx")

probs_neuro=pd.read_excel(r"O:\OrlI\readmissions\report\results\final models\test_groups\inclusive\neuro_full\probs\probs.xlsx")
label_neuro=pd.read_excel(r"O:\OrlI\readmissions\report\results\final models\test_groups\inclusive\neuro_full\probs\y.xlsx")

probs_surgical=pd.read_excel(r"O:\OrlI\readmissions\report\results\final models\test_groups\inclusive\surgical_full\probs\probs.xlsx")
label_surgical=pd.read_excel(r"O:\OrlI\readmissions\report\results\final models\test_groups\inclusive\surgical_full\probs\y.xlsx")

probs_cardio=pd.read_excel(r"O:\OrlI\readmissions\report\results\final models\test_groups\inclusive\cardio\probs\probs.xlsx")
label_cardio=pd.read_excel(r"O:\OrlI\readmissions\report\results\final models\test_groups\inclusive\cardio\probs\y.xlsx")

probs_covid=pd.read_excel(r"O:\OrlI\readmissions\report\results\final models\test_groups\inclusive\covid\probs\probs.xlsx")
label_covid=pd.read_excel(r"O:\OrlI\readmissions\report\results\final models\test_groups\inclusive\covid\probs\y.xlsx")


probs_internal=probs_internal.iloc[:,1]
label_internal=label_internal.iloc[:,1]

probs_neuro=probs_neuro.iloc[:,1]
label_neuro=label_neuro.iloc[:,1]

probs_surgical=probs_surgical.iloc[:,1]
label_surgical=label_surgical.iloc[:,1]

probs_cardio=probs_cardio.iloc[:,1]
label_cardio=label_cardio.iloc[:,1]

probs_covid=probs_covid.iloc[:,1]
label_covid=label_covid.iloc[:,1]

plt.figure(figsize=(6, 6))


fpr1, tpr1,thresholds1=roc_curve(label_internal, probs_internal)
logit_roc_auc1=round(roc_auc_score(label_internal, probs_internal),2)

plt.plot (fpr1, tpr1, label='AUC internal '+' = ' +str(logit_roc_auc1))
plt.plot ([0, 1], [0, 1], 'r--')
plt.xlim ([0.0, 1.0])
plt.ylim ([0.0, 1.05])
plt.xlabel ('False Positive Rate')
plt.ylabel ('True Positive Rate')
#plt.title ('Receiver operating characteristic')
plt.legend (loc="lower right")


fpr2, tpr2,thresholds1=roc_curve(label_neuro, probs_neuro)
logit_roc_auc2=round(roc_auc_score(label_neuro, probs_neuro),2)

plt.plot (fpr2, tpr2, label='AUC neuro'+' = ' +str(logit_roc_auc2))
plt.plot ([0, 1], [0, 1], 'r--')
plt.xlim ([0.0, 1.0])
plt.ylim ([0.0, 1.05])
plt.xlabel ('False Positive Rate')
plt.ylabel ('True Positive Rate')
#plt.title ('Receiver operating characteristic')
plt.legend (loc="lower right")

fpr3, tpr3,thresholds1=roc_curve(label_surgical, probs_surgical)
logit_roc_auc3=round(roc_auc_score(label_surgical, probs_surgical),2)

plt.plot (fpr3, tpr3, label='AUC surgical '+' = ' +str(logit_roc_auc3))
plt.plot ([0, 1], [0, 1], 'r--')
plt.xlim ([0.0, 1.0])
plt.ylim ([0.0, 1.05])
plt.xlabel ('False Positive Rate')
plt.ylabel ('True Positive Rate')
#plt.title ('Receiver operating characteristic')
plt.legend (loc="lower right")


fpr4, tpr4,thresholds1=roc_curve(label_cardio, probs_cardio)
logit_roc_auc4=round(roc_auc_score(label_cardio, probs_cardio),2)

plt.plot (fpr4, tpr4, label='AUC cardio'+' = ' +str(logit_roc_auc4))
plt.plot ([0, 1], [0, 1], 'r--')
plt.xlim ([0.0, 1.0])
plt.ylim ([0.0, 1.05])
plt.xlabel ('False Positive Rate')
plt.ylabel ('True Positive Rate')
#plt.title ('Receiver operating characteristic')
plt.legend (loc="lower right")


fpr5, tpr5,thresholds1=roc_curve(label_covid, probs_covid)
logit_roc_auc5=round(roc_auc_score(label_covid, probs_covid),2)

plt.plot (fpr5, tpr5, label='AUC covid'+' = ' +str(logit_roc_auc5))
plt.plot ([0, 1], [0, 1], 'r--')
plt.xlim ([0.0, 1.0])
plt.ylim ([0.0, 1.05])
plt.xlabel ('False Positive Rate')
plt.ylabel ('True Positive Rate')
#plt.title ('Receiver operating characteristic')
plt.legend (loc="lower right")



    
plt.savefig(r'O:\OrlI\readmissions\report\figures\roc_auc_all_test_sets.png') 


# testr ages


probs_internal_young=pd.read_excel(r"O:\OrlI\readmissions\model_results\test_results\internal_l1_lessthan65\probs\probs.xlsx")
label_internal_young=pd.read_excel(r"O:\OrlI\readmissions\model_results\test_results\internal_l1_lessthan65\probs\y.xlsx")

probs_internal_old=pd.read_excel(r"O:\OrlI\readmissions\model_results\test_results\internal_l1_65andup\probs\probs.xlsx")
label_internal_old=pd.read_excel(r"O:\OrlI\readmissions\model_results\test_results\internal_l1_65andup\probs\y.xlsx")


probs_internal_young=probs_internal_young.iloc[:,1]
label_internal_young=label_internal_young.iloc[:,1]

probs_internal_old=probs_internal_old.iloc[:,1]
label_internal_old=label_internal_old.iloc[:,1]


plt.figure(figsize=(6, 6))


fpr1, tpr1,thresholds1=roc_curve(label_internal_young, probs_internal_young)
logit_roc_auc1=round(roc_auc_score(label_internal_young, probs_internal_young),2)

plt.plot (fpr1, tpr1, label='AUC under 65 '+' = ' +str(logit_roc_auc1))
plt.plot ([0, 1], [0, 1], 'r--')
plt.xlim ([0.0, 1.0])
plt.ylim ([0.0, 1.05])
plt.xlabel ('False Positive Rate')
plt.ylabel ('True Positive Rate')
#plt.title ('Receiver operating characteristic')
plt.legend (loc="lower right")




fpr3, tpr3,thresholds1=roc_curve(label_internal_old, probs_internal_old)
logit_roc_auc3=round(roc_auc_score(label_internal_old, probs_internal_old),2)

plt.plot (fpr3, tpr3, label='AUC over 65 '+' = ' +str(logit_roc_auc3))
plt.plot ([0, 1], [0, 1], 'r--')
plt.xlim ([0.0, 1.0])
plt.ylim ([0.0, 1.05])
plt.xlabel ('False Positive Rate')
plt.ylabel ('True Positive Rate')
#plt.title ('Receiver operating characteristic')
plt.legend (loc="lower right")


plt.plot (fpr5, tpr5, label='AUC covid'+' = ' +str(logit_roc_auc5))
plt.plot ([0, 1], [0, 1], 'r--')
plt.xlim ([0.0, 1.0])
plt.ylim ([0.0, 1.05])
plt.xlabel ('False Positive Rate')
plt.ylabel ('True Positive Rate')
#plt.title ('Receiver operating characteristic')
plt.legend (loc="lower right")


