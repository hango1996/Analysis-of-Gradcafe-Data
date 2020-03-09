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
