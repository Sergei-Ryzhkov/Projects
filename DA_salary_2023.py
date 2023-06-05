import pandas as pd
import numpy as np 
import os 
import matplotlib as plt

list = (r"C:\Users\aser\OneDrive\Рабочий стол\DATASETS\ds_salaries.csv")
df = pd.read_csv(list)

# DATA EXPLORATION
df.shape
df.dtypes
df.head(5)
df.describe()
categorical = df.dtypes[df.dtypes == 'object'].index
df[categorical].describe()
df['salary_in_usd'][0:15]
df.info()
df['salary'].head(20)
df['salary_in_usd'].describe().apply("{0:.5f}".format)

df[df['emloyee_residence'] == 'RU'].hist(column = 'salary_in_usd', 
                  figsize=(9,6),
                  range=(0,304000),
                  bins=20)
df.boxplot(column='salary_in_usd')
df.boxplot(column='salary_in_usd',
           by = 'experience_level',
           figsize = (6,6))
df['company_size'].unique()
df[['emloyee_residence'] == 'RU']
df.loc[:,['salary', 'salary_in_usd']]
df['emloyee_residence'] == 'US'