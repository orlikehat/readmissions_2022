# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 12:29:48 2021

@author: orlyk
"""

import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



probs=pd.read_csv(r'O:\OrlI\readmissions\report\results\final models\LR_full_final\probs\probs_all.csv')
y=pd.read_csv(r'O:\OrlI\readmissions\report\results\final models\LR_full_final\probs\y.csv')


#for test sets:
probs["prob_test"]=probs.iloc[:,0]
y["LABEL_HOSP"]=y.iloc[:,0]

y["LABEL_HOSP"]=np.where(y["LABEL_HOSP"]==1, "readmission", "no readmission")
sns.boxplot(x=y["LABEL_HOSP"], y=probs["prob_test"],whis=[1, 99],showfliers=False,order=["readmission","no readmission"])
        #plt.title("Test (N=71)", fontdict=None, loc='center')
plt.ylabel ("probabilities") 
plt.xlabel (None) 

plt.ylim(0.1, 1)

plt.savefig(r'O:\OrlI\readmissions\report\results\tables_and_figures\probs_internal_full.png',bbox_inches='tight') 
#ax = sns.heatmap(probs, cmap="YlGnBu")
#
#
#ax.colorbar( orientation="horizontal")