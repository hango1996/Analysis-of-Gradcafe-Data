from clean import df
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotnine as p9
from wordcloud import WordCloud


def event_counts_date(abbr_institution="Davis", degree="PhD"):
    df_selected = df[lambda x: (x["institution"].str.contains(
        abbr_institution)) & (x["degree"] == degree)]
    df_selected["date_md"] = df_selected["admission_date"].apply(
        lambda dt: dt.replace(year=1980))
    df_selected["year"] = df_selected["admission_date"].apply(
        lambda dt: dt.year)

    gg = p9.ggplot(df_selected)
    gg += p9.aes(x="date_md", y="admission_status")
    gg += p9.scale_x_datetime(date_breaks='10 days',
                              date_labels="%m-%d",
                              limits=np.array([np.min(df_selected["date_md"]), pd.to_datetime("1980-4-20")]))
    gg += p9.geom_count()
    gg += p9.ggtitle(df_selected["institution"].iloc[0])
    return gg


# def wordcloud(abbr_institution="Davis", degree="PhD"):
def wordcloud_df(request=lambda x: x["degree"] == "PhD"):
    df_selected = df[request]
    wordcloud = WordCloud().generate(df_selected["notes"].str.cat())
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")


wordcloud_df(lambda x: x["degree"] == "PhD")
wordcloud_df(lambda x: x["degree"] == "Masters")

wordcloud_df(lambda x: (x["admission_status"] ==
                        "Accepted") & (x["degree"] == "PhD"))
wordcloud_df(lambda x: (x["admission_status"] ==
                        "Interview") & (x["degree"] == "PhD"))

wordcloud_df(lambda x: (x["institution"].str.contains(
                        "Davis")) & (x["degree"] == "PhD"))


event_counts_date("NCSU")
