# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jJrX4r8DOm6v06BKGzXF2p8N6Cw1fSRx

IMPORTING LIBRARIES
"""

import numpy as np #linear algebra
import pandas as pd #data processing

import matplotlib.pyplot as plt #data visualization
import seaborn as sns #data visualization

import warnings
warnings.filterwarnings("ignore") #to ignore the warnings

#for model building
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
import xgboost as xgb

"""DATA PREPROCESSING"""

df=pd.read_csv('heart.csv')
# looking at the first 5 rows of our data
df.head()

df.isnull().sum()
df.drop_duplicates(inplace=True)
list_col=['sex','chol','trtbps','cp','thall','exng']

"""COUNT OF ROWS AND COLOUMN DATA"""

print(f'Number of people having sex as 0 are {df.sex.value_counts()[0]} and Number of people having sex as 1 are {df.sex.value_counts()[1]}')
p = sns.countplot(data=df, x="sex", palette='pastel')
plt.show()

print("The count of chest pain type:")
sns.countplot(x='cp', data=df, palette='pastel')

print("The count of fbs type:")
sns.countplot(x='fbs', data=df, palette='pastel')

print("The count of thal type:")
sns.countplot(x='thall', data=df, palette='pastel')

print("The count of resteg type:")
sns.countplot(x='restecg', data=df, palette='pastel')

"""Swarn Plot between age and caa."""

plt.figure(figsize = (10,10))
sns.swarmplot(x=df['caa'],y=df['age'],hue=df['output'], palette='pastel')

"""Outliners:"""

sns.color_palette("pastel")
plt.title('Checking Outliers with distplot()')
sns.distplot(df.trtbps, label='trtbps', kde=True, bins=10, color='green')
plt.legend()

plt.title('Checking Outliers with distplot()')
sns.distplot(df.chol, label='chol', kde=True, color='red')
plt.legend()

plt.title('Checking Outliers with distplot()')
sns.distplot(df['thalachh'],label='thalachh', kde=True )
plt.legend()

X = df.drop('output', axis = 1)
y = df['output']

df.reset_index(drop=True, inplace=True)

columns_to_scale = df.iloc[:,[0,3,4,7,9,]]
columns_to_scale

"""Splitting of Dataset and Feature Scaling

"""

# Spliting the data
from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

ss = StandardScaler()
scaled_values = ss.fit_transform(columns_to_scale)
scaled_values = pd.DataFrame(scaled_values, columns=columns_to_scale.columns)
scaled_values

scaled_df = pd.concat([scaled_values,df.iloc[:,[1,2,5,6,8,10,11,12,13]]],axis=1)
scaled_df

"""Building Models

"""

key = ['LogisticRegression','KNeighborsClassifier','SVC','DecisionTreeClassifier','RandomForestClassifier','GradientBoostingClassifier','AdaBoostClassifier','XGBClassifier']
value = [LogisticRegression(random_state=9), KNeighborsClassifier(), SVC(), DecisionTreeClassifier(), RandomForestClassifier(), GradientBoostingClassifier(), AdaBoostClassifier(), xgb.XGBClassifier()]
models = dict(zip(key,value))

predicted =[]

X = scaled_df.drop('output', axis = 1)
y = scaled_df['output']
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

for name,algo in models.items():
    model=algo
    model.fit(X_train,y_train)
    predict = model.predict(X_test)
    acc = accuracy_score(y_test, predict)
    predicted.append(acc)
    print(name,acc)

plt.figure(figsize = (10,5))
sns.barplot(x = predicted, y = key, palette='pastel')

lr = LogisticRegression(solver='lbfgs', max_iter=10000)
rs = []
acc = []
for i in range(1,100,1):
    X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.2, random_state = i)    
    model_lr_rs = lr.fit(X_train, y_train.values.ravel())
    predict_values_lr_rs = model_lr_rs.predict(X_test)
    acc.append(accuracy_score(y_test, predict_values_lr_rs))
    rs.append(i)

plt.figure(figsize=(10,10))
plt.plot(rs, acc)

for i in range(len(rs)):
    print(rs[i],acc[i])

"""CONCLUSION:
1 -  A person with High Blood Pressure, High Cholesterol, High Heart Rate is having more chance of heart attack.
2 - Person with age between 40-60 years having more chances of a heart attack.
3 - Males are having more chances of a heart attack rather than women.
4 - People with Non-agnigal chest pain having more chance of heart attack.
5 - People with No exercise with angina having more chance of a heart attack


"""