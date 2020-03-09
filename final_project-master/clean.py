import pandas as pd
import numpy as np
import re

df = pd.read_csv("gradcafe.csv")

df["admission_via"][df["admission_via"] == "POST"] = "Postal Service"
df["degree"][np.logical_not(df["degree"].isin(
    ["PhD", "Masters", "Other"]))] = "Other"
for col in ["ST", "degree", "admission_status", "admission_via"]:
    df[col] = df[col].astype("category")
for col in ["admission_date", "Date_added"]:
    df[col] = pd.to_datetime(df[col])

# scale GPA
df.Undergrad_GPA = np.where((df.Undergrad_GPA > 4)&(df.Undergrad_GPA <= 5), df.Undergrad_GPA*4/5, df.Undergrad_GPA)
df.Undergrad_GPA = np.where((df.Undergrad_GPA > 5)&(df.Undergrad_GPA <= 10), df.Undergrad_GPA*4/10, df.Undergrad_GPA)

# scale GRE: old to new
GRE = pd.DataFrame(list(zip(np.arange(200, 810, 10).tolist(), np.repeat(130, 4).tolist()+np.arange(131, 143).tolist()+[143, 143, 144, 145, 146, 146, 147, 148, 149, 149, 150, 151, 151, 152, 152, 153, 154, 154, 155, 156, 156, 157, 158, 158, 159, 160, 160, 161, 162, 162, 163, 164, 164, 165, 165, 166, 167, 168, 168, 169, 169, 170, 170, 170, 170, 170])), columns=['old', 'new'])

for index, row in df.iterrows():
    if df.loc[index, 'GRE_V']>200:
        df.loc[index, 'GRE_V']=GRE.new[GRE.old == df.loc[index, 'GRE_V']].to_numpy()
    if gradcafe.loc[index, 'GRE_Q']>200:
        df.loc[index, 'GRE_Q']=GRE.new[GRE.old == df.loc[index, 'GRE_Q']].to_numpy()
# correct unexpected input: 179 to 169, 180 to 170
df.loc[df.GRE_V==179, 'GRE_V']=169
df.loc[df.GRE_V==180, 'GRE_V']=170
df.loc[df.GRE_V<130, 'GRE_V']=np.nan
df.loc[df.GRE_Q==179, 'GRE_Q']=169
df.loc[df.GRE_Q==180, 'GRE_Q']=170
df.loc[df.GRE_Q<130, 'GRE_Q']=np.nan

# correct unexpected season
df.loc[df.season=='?', 'season']='F09'