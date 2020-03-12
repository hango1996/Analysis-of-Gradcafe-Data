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


event_counts_date("Davis")
event_counts_date("Stanford")


def wordcloud_df(request_disc=None):
    '''
    request should be given as a dictionary
    '''
    request = np.ones(df.shape[0], dtype=bool)
    for key in request_disc.keys():
        if key == "institution":
            request = request & (df[key].str.contains(request_disc[key]))
        else:
            request = request & (df[key] == request_disc[key])
    wordcloud = WordCloud().generate(df[request]["notes"].str.cat())
    samp = df[request].iloc[0]
    title = ""
    for key in request_disc.keys():
        title += samp[key]
        title += " "
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(title)


wordcloud_df({"degree": "PhD"})
wordcloud_df({"admission_status": "Rejected", "degree": "PhD"})
wordcloud_df({"admission_status": "Interview", "degree": "PhD"})

wordcloud_df({"institution": "Davis", "degree": "PhD"})


def prop_piechart(which_prop="ST", request_disc=None):
    request = np.ones(df.shape[0], dtype=bool)
    for key in request_disc.keys():
        if key == "institution":
            request = request & (df[key].str.contains(request_disc[key]))
        else:
            request = request & (df[key] == request_disc[key])
    df_selected = df[request]
    prop = df_selected[which_prop].value_counts()
    prop /= np.sum(prop)
    samp = df_selected.iloc[0]
    title = ""
    for key in request_disc.keys():
        title += samp[key]
        title += " "
    plt.pie(
        prop, explode=0.1*(prop == np.max(prop)), labels=prop.index, autopct='%1.1f%%', shadow=True)
    plt.title(title)


prop_piechart("ST", {"institution": "Davis",
                     "admission_status": "Accepted", "degree": "PhD"})
prop_piechart("ST", {"institution": "Davis",
                     "degree": "PhD"})

prop_piechart("admission_status", {"institution": "Davis", "degree": "PhD"})
prop_piechart("admission_status", {"institution": "Berkeley", "degree": "PhD"})
prop_piechart("admission_status", {
              "institution": "of Washington", "degree": "PhD"})
