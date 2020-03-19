from clean import df
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotnine as p9
from wordcloud import WordCloud
from sklearn.feature_extraction import text
from sklearn.model_selection import cross_val_score
from sklearn import tree
import graphviz


def event_counts_date(request_disc=None):
    '''
    Plot the average timeline of a certain institution
    request should be given as a dictionary
    '''
    request = np.ones(df.shape[0], dtype=bool)
    for key in request_disc.keys():
        if key == "institution":
            request = request & (df[key].str.contains(request_disc[key]))
        else:
            request = request & (df[key] == request_disc[key])
    df_selected = df[request]
    df_selected["date_md"] = df_selected["admission_date"].apply(
        lambda dt: dt.replace(year=1980))
    df_selected["year"] = df_selected["admission_date"].apply(
        lambda dt: dt.year)

    samp = df[request].iloc[0]
    title = ""
    for key in request_disc.keys():
        title += samp[key]
        title += " "
    gg = p9.ggplot(df_selected)
    gg += p9.aes(x="date_md", y="admission_status")
    gg += p9.scale_x_datetime(date_breaks='10 days',
                              date_labels="%m-%d",
                              limits=np.array([np.min(df_selected["date_md"]), pd.to_datetime("1980-4-20")]))
    gg += p9.geom_count()
    gg += p9.ggtitle(title)
    return gg


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


def prop_piechart(which="ST", request_disc=None):
    '''
    request should be given as a dictionary
    '''
    request = np.ones(df.shape[0], dtype=bool)
    for key in request_disc.keys():
        if key == "institution":
            request = request & (df[key].str.contains(request_disc[key]))
        else:
            request = request & (df[key] == request_disc[key])
    df_selected = df[request]
    prop = df_selected[which].value_counts(sort=False)
    prop /= np.sum(prop)
    samp = df_selected.iloc[0]
    title = ""
    for key in request_disc.keys():
        title += samp[key]
        title += " "

    if which == "ST":
        plt.pie(
            prop, explode=0.1*(prop.index == "I"), labels=prop.index, autopct='%1.1f%%', shadow=True)
        ST_dic = {"A": "American", "U": "International, with US degree",
                  "I": "International, without US degree", "O": "Other"}
        plt.legend([ST_dic[i] for i in prop.index], bbox_to_anchor=(1, 0.5), loc="center right",
                   bbox_transform=plt.gcf().transFigure)
        plt.subplots_adjust(left=0.0, bottom=0.1, right=0.45)
    elif which == "admission_status":
        plt.pie(
            prop, explode=0.1*(prop.index == "Accepted"), labels=prop.index, autopct='%1.1f%%', shadow=True)
    plt.title(title)
    #plt.savefig(fname=title + ".png", dpi=1000)


def notes_decision_tree_classifier():
    df_sel = df[["notes", "admission_status"]].dropna()
    tfidf = text.TfidfVectorizer()
    X = tfidf.fit_transform(df_sel["notes"]).toarray()
    feature_names = tfidf.get_feature_names()
    y = df_sel["admission_status"]
    clf = tree.DecisionTreeClassifier(random_state=0, ccp_alpha=0.001)
    clf.fit(X, y)
    print("20 Most Important Words: ", np.array(tfidf.get_feature_names())[
        np.argsort(clf.feature_importances_)[::-1]][0:20])
    print("10-fold Cross Validation Accuracy: ",
          np.mean(cross_val_score(clf, X, y, cv=10)))
    dot_data = tree.export_graphviz(clf, out_file=None,
                                    max_depth=7, feature_names=feature_names, class_names=sorted(y.unique().tolist()),
                                    filled=True, rounded=True,
                                    rotate=True,
                                    special_characters=True)
    graph = graphviz.Source(dot_data)
    return(graph)


if __name__ == "__main__":
    event_counts_date({"institution": "Davis", "degree": "PhD"})
    event_counts_date({"institution": "Stanford", "degree": "PhD"})

    wordcloud_df({"degree": "PhD"})
    wordcloud_df({"institution": "Davis", "degree": "PhD"})

    prop_piechart("ST", {"institution": "Davis",
                         "admission_status": "Accepted", "degree": "PhD"})
    prop_piechart("ST", {"institution": "Berkeley",
                         "admission_status": "Accepted", "degree": "PhD"})

    def summary_ST_prop(x):
        t = x["ST"].value_counts()
        return t["I"]/np.sum([t[i] for i in t.index])
    (df.loc[(df["admission_status"] == "Accepted") & (df["degree"] == "PhD")]).groupby(
        "institution").apply(summary_ST_prop).sort_values(ascending=False)[df["institution"].value_counts() >= 50]

    prop_piechart("admission_status", {
                  "institution": "Davis", "degree": "PhD"})
    prop_piechart("admission_status", {
                  "institution": "Berkeley", "degree": "PhD"})

    def summary_admission_prop(x):
        t = x["admission_status"].value_counts()
        return t["Accepted"] / (t["Accepted"] + t["Rejected"])
    (df.loc[df["degree"] == "PhD"]).groupby(
        "institution").apply(summary_ST_prop).sort_values()[df["institution"].value_counts() >= 50]

    notes_decision_tree_classifier().render(filename="Notes_Tree")
