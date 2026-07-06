from operator import index

import pandas as pd
import numpy as np
from fontTools.misc.filenames import userNameToFileName
from mpl_toolkits.axes_grid1 import host_subplot
from sqlalchemy import create_engine

# here import data
df = pd.read_csv("C:/Users/PANKAJ KUMAR/OneDrive/Desktop/collegeProject/customer_shopping_behavior.csv")
# shown a some raw data
print(df)
print(df.head())
print(df.info())
# check null data in data set
print(df.isnull().sum())
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()) )

print(df.isnull().sum())

# replace and rename column name
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
print(df.columns)

# create new columns
labels = ['Young Adult','Adult','Middle-aged','Senior']
df['age_group'] = pd.qcut(df['age'],q=4,labels=labels)

print(df[['age','age_group']].head(10))


# create column purchase_frequency_day

frequency_mapping = {
    'Fortnightly':14,
    'Weekly':7,
    'Monthly':30,
    'Quarterly':90,
    'Bi-Weekly':14,
    'Annually':365,
    'Every 3 Months':90
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

print(df[['purchase_frequency_days','frequency_of_purchases']].head(10))
print(df[['discount_applied','promo_code_used']].head(10))

# check two column values are same
print((df['discount_applied']==df['promo_code_used']).all())

# delete  a not use column
df = df.drop('promo_code_used',axis=1)

print(df.columns)


# here we stable the connection between postgre and python

# connect to postgresql
username = "postgres"
password = "password"
host = "localhost"
port = "5432"
database = "customer_behavior"

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# load dataframe into postgresql

table_name = "customer"
df.to_sql(table_name, engine,if_exists=  "replace", index =False)
print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")








