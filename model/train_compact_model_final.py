# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 15:02:48 2021

@author: orlyk
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:43:25 2021

@author: orlyk
"""

# -*- coding: utf-8 -*-

"""
run and save the final logistic regression compact model as described in the 
 report for the מכון לאומי לבריאות

model and prior imputation and scaling is saved in
O:\OrlI\readmissions\code\compact_model_final\finalized_model

to run a test set on this model use: run_test_set.py
"""


import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from functions.classification_metrics_train_only import *



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

df_train=pd.read_csv(r'O:\OrlI\readmissions\code\compact_model_final\df_train.csv')


y=df_train["LABEL_HOSP"]
x=df_train.drop(columns=['LABEL_HOSP','PatNum'])

features=list(x.columns)

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

x_train=x
y_train=y
 
features=features=list(x_train.columns)
#feature_array= pd.Series(features)
feature_array= pd.DataFrame(features)

#immutation by median
my_imputer = SimpleImputer(strategy='median')
x_train=pd.DataFrame(my_imputer.fit_transform(x_train), columns = x_train.columns)
pickle.dump(my_imputer, open(path+'/imputer.pkl', 'wb'))  


#standard scaler
scaler = StandardScaler()
x_train=pd.DataFrame(scaler.fit_transform(x_train), columns = x_train.columns)
pickle.dump(scaler, open(path+'/scaler.pkl', 'wb'))  
             

#train_model 
model = LogisticRegression(max_iter=2000,C= 0.01,penalty='l1',solver='saga',verbose=1, warm_start=True,class_weight='balanced')

train_model = model.fit(x_train, y_train)

y_pred = model.predict(x_train)
    
probs_train=train_model.predict_proba(x_train)[:, 1]
pickle.dump(model, open(path+"/finalized_model_LR_l1.pkl", 'wb'))    


      
#calssification metrics
sensitivity_recall,specificity,ppv,f1,auc_train=report_metrics(y_train,y_pred,probs_train)                    
df_metrics=pd.DataFrame([auc_train,sensitivity_recall,specificity,ppv,f1])
df_metrics.index = ["auc_train","sensitivity","specificity","ppv","f1"]

df_metrics.to_excel(path+"/metrics/classification_metrics.xlsx",index=False)




#coefficients:
print("Non Zero weights:", np.count_nonzero(train_model.coef_))
coeffs=train_model.coef_
coeffs=np.transpose(coeffs)

dff = pd.DataFrame(data=coeffs)

dff = pd.DataFrame(data=coeffs,index=features)
dff=dff.rename(columns={0: "coeffs"})

dff=dff.reindex(dff["coeffs"].abs().sort_values(ascending=False).index)
importance_contcat=pd.concat([importance_contcat,dff],axis=1)

dff.to_csv(path+"/coefs/coefs_list.csv")#,index=False)
importance_contcat.to_csv(path+"/coefs/coefs_all_iter.csv")#,index=False)

plt.figure( )
sns.barplot(x=dff["coeffs"], y=dff.index)
plt.title("LR coefficients")
plt.savefig(path + '/coefs/coefs_figures'+"/LR_coeffs.png") 
plt.figure( )


