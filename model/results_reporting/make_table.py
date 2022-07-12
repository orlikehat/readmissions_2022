# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 14:12:32 2021

@author: orlyk
"""



import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
#pio.renderers.default = 'svg'
pio.renderers.default = 'browser'
import matplotlib.pyplot as plt
from tabulate import tabulate



LR_metrics=pd.read_excel(r'O:\OrlI\readmissions\model_results\for_report\LR_2K_fixed_pop\metrics\classification_metrics.xlsx') 
RF_metrics=pd.read_excel(r'O:\OrlI\readmissions\model_results\for_report\RF_fixed_POP\metrics\classification_metrics.xlsx') 
xgb_metrics=pd.read_excel(r'O:\OrlI\readmissions\model_results\for_report\xgb_fixed_POP\metrics\classification_metrics.xlsx') 
HS_metrics=pd.read_excel(r'O:\OrlI\readmissions\model_results\for_report\HS_fixed_POP\metrics\classification_metrics.xlsx') 

frames=[LR_metrics,RF_metrics,xgb_metrics,HS_metrics]
names=pd.Series(["HS","LR","RF","xgb"],name="algo")

table=pd.DataFrame()
for frame in frames:
    temp=frame.iloc[5,:]
    table=table.append(temp)
    
table=table.reset_index()
table=pd.merge(names,table,right_index=True, left_index=True)
table=table[["algo","sensitivity","specificity","ppv","auc_test","pr_auc"]]

print(tabulate(table,headers=table.columns,tablefmt='fancy_grid'))

table.to_csv(r'O:\OrlI\readmissions\model_results\for_report\results\metrics_table.csv')



