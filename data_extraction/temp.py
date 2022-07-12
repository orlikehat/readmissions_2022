# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 10:45:37 2022

@author: orlyk
"""

import pandas as pd
import numpy as np
'''
#PANDAS DATAFRAME: two-dimensional labeled data structures with columns of potentially different types.
#In general, you could say that the Pandas DataFrame consists of three main components: the data, the index, and the columns.
'''
data = {'subject_num':["001","002","003","004","005","006","007","008","009"],
        'first_name':["Esther","Eyal","Liran","Brenda","Tal","Bar","Noa","Orli","Shmulik"],
        'city':["Tel_Aviv","Ramat_Gan","Tel_Aviv","Givataim","Tel_Aviv","Ramat_Hasharon","Haifa","Zoran",np.nan],
    'apples': [3, 2, 0, 1,3,6,np.nan,7,15], 
    'oranges': [9, 3, 7, 2,4,7,2,8,1]
}


df = pd.DataFrame(data)

#series
apples=data["apples"]
first_names=data["first_name"]
df_short=df[["first_name","apples","oranges"]]



#-know youe dataframe:
df.shape
print(df.info())

df.describe(include='all')

df["city"].value_counts()
df.columns

df["first_name"].nunique()

df["city"].nunique()


#-------------------------------------
#rename


#selecting

df.loc[0,"first_name"]
df.loc[0:3]
df.loc[0:3,"first_name"]
df.loc[0:3,["first_name","subject_num"]]

#conditionals and filtering:
df["city"]=="Tel_Aviv"
df[df["city"]=="Tel_Aviv"]
df.loc[df["city"]=="Tel_Aviv"]
df.loc[df["city"]=="Tel_Aviv",["subject_num","first_name"]]

df.loc[(df["city"]=="Tel_Aviv")&(df["apples"]==3),["subject_num","first_name"]]

df.loc[(df["city"]=="Tel_Aviv")|(df["apples"]==3),["subject_num","first_name"]]

df.loc[(df["city"]=="Tel_Aviv")|(df["apples"]>4),["subject_num","first_name"]]

population_list=["Noa","Tal","Liran"]

df.loc[df['first_name'].isin(population_list)]
df.loc[(df['first_name'].isin(population_list)),["subject_name","city"]]









