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
df.Undergrad_GPA = np.where((df.Undergrad_GPA > 4) & (
    df.Undergrad_GPA <= 5), df.Undergrad_GPA*4/5, df.Undergrad_GPA)
df.Undergrad_GPA = np.where((df.Undergrad_GPA > 5) & (
    df.Undergrad_GPA <= 10), df.Undergrad_GPA*4/10, df.Undergrad_GPA)


# scale GRE: old to new

GRE = pd.DataFrame(list(zip(np.arange(200, 810, 10).tolist(), np.repeat(130, 4).tolist()+np.arange(131, 143).tolist() +
                            [143, 143, 144, 145, 146, 146, 147, 148, 149, 149, 150, 151, 151, 152, 152, 153, 154, 154, 155, 156, 156, 157, 158, 158, 159, 160, 160, 161, 162, 162, 163, 164, 164, 165, 165, 166, 167, 168, 168, 169, 169, 170, 170, 170, 170, 170])), columns=['old', 'new'])


for index, row in df.iterrows():
    if df.loc[index, 'GRE_V'] > 200:
        df.loc[index, 'GRE_V'] = GRE.new[GRE.old ==
                                         df.loc[index, 'GRE_V']].to_numpy()
    if df.loc[index, 'GRE_Q'] > 200:
        df.loc[index, 'GRE_Q'] = GRE.new[GRE.old ==
                                         df.loc[index, 'GRE_Q']].to_numpy()

# correct unexpected input: 179 to 169, 180 to 170
df.loc[df.GRE_V == 179, 'GRE_V'] = 169
df.loc[df.GRE_V == 180, 'GRE_V'] = 170
df.loc[df.GRE_V < 130, 'GRE_V'] = np.nan
df.loc[df.GRE_Q == 179, 'GRE_Q'] = 169
df.loc[df.GRE_Q == 180, 'GRE_Q'] = 170
df.loc[df.GRE_Q < 130, 'GRE_Q'] = np.nan

# scale GRE AW
# 0 to nan, 30 to 3, 0.3 to 3, 4.8, 42, 44 to 4

df.loc[df.GRE_W == 0, 'GRE_W'] = np.nan
df.loc[df.GRE_W == 30, 'GRE_W'] = 3
df.loc[df.GRE_W == 0.3, 'GRE_W'] = 3
df.loc[df.GRE_W == 4.8, 'GRE_W'] = 4
df.loc[df.GRE_W == 42, 'GRE_W'] = 4
df.loc[df.GRE_W == 44, 'GRE_W'] = 4
df.loc[df.GRE_W > 6, 'GRE_W'] = np.nan

# correct unexpected season
df.loc[df.season == '?', 'season'] = 'F09'

# correct name of institutions
df["institution"][lambda x:x.str.contains("Stanford")] = "Stanford University"
df["institution"][lambda x:x.str.contains("Duke")] = "Duke University"
df["institution"][lambda x:x.str.contains("Berkeley") | x.str.contains(
    "UCB")] = "University Of California, Berkeley (UCB)"
df["institution"][lambda x:x.str.contains("Seattle") | x.str.contains(
    "Of Washington")] = "University Of Washington"
df["institution"][lambda x:x.str.contains("Harvard")] = "Harvard University"
df["institution"][lambda x:x.str.contains("CMU") | x.str.contains(
    "Carnegie") | x.str.contains("Mellon")] = "Carnegie Mellon University (CMU)"

df["institution"][lambda x:x.str.contains("NCSU") | x.str.contains(
    "Carolina State")] = "North Carolina State University (NCSU)"

df["institution"][lambda x:x.str.contains("UCLA") | x.str.contains(
    "Los Angeles")] = "University Of California, Los Angeles (UCLA)"
df["institution"][lambda x: x.str.contains(
    "Davis")] = "University of California, Davis (UC Davis)"
df["institution"][lambda x:x.str.contains(
    "Oregon")] = "Oregon State University"
df["institution"][lambda x:x.str.contains("OSU") | x.str.contains(
    "Ohio S")] = "Ohio State University (OSU)"
df["institution"][lambda x:x.str.contains("UMN") | x.str.contains(
    "nesota")] = "University Of Minnesota - Twin Cities (UMN)"
df["institution"][lambda x:x.str.contains(
    "University Purdue") | x.str.contains("IUPUI")] = "IUPUI"
df["institution"][lambda x:x.str.contains("Purdue")]="Purdue University"
