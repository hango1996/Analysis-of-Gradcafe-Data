from clean import df
import pandas as pd
import numpy as np
import plotnine as p9

UCD_PhD = df[lambda x: (x["institution"].str.contains(
    "Davis")) &
    (x["degree"] == "PhD")]
UCD_PhD["date_md"] = UCD_PhD["admission_date"].apply(
    lambda dt: dt.replace(year=1980))
UCD_PhD["year"] = UCD_PhD["admission_date"].apply(lambda dt: dt.year)

gg = p9.ggplot(UCD_PhD)
gg += p9.aes(x="date_md", y="admission_status")
gg += p9.scale_x_datetime(date_breaks='10 days', date_labels="%m-%d")
gg += p9.geom_count()
gg += p9.ggtitle(UCD_PhD["institution"].iloc[0])
gg
