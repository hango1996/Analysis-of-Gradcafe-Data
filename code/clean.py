import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder # encode categorical predictors
import geopandas as gpd

df = pd.read_csv('../data/gradcafe.csv')

df.loc[df.admission_via == 'POST', 'admission_via'] = 'Postal Service'
df.loc[~df.degree.isin(['PhD', 'Masters', 'Other']), 'degree'] = 'Other'
for col in ['ST', 'degree', 'admission_status', 'admission_via']:
    df[col] = df[col].astype('category')
for col in ['admission_date', 'Date_added']:
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

# scale GRE sub
df.loc[df.GRE_sub<10, 'GRE_sub'] = np.nan
df.loc[df.GRE_sub<100, 'GRE_sub'] = df.loc[df.GRE_sub<100, 'GRE_sub']*10

# correct unexpected season
df.loc[df.season == '?', 'season'] = 'F09'

# correct name of institutions
df.loc[df.institution.str.contains(
    'stanford', case=False), 'institution'] = 'Stanford University (Department of Statistics)'
df.loc[df.institution.str.contains(
    'berk|UCB', case=False), 'institution'] = 'University of California--Berkeley (Department of Statistics)'
df.loc[df.institution.str.contains(
    'harvard', case=False), 'institution'] = 'Harvard University (Department of Statistics)'
df.loc[df.institution.str.contains('chic', case=False) & ~df.institution.str.contains(
    'loyola|illinois', case=False), 'institution'] = 'University of Chicago (Department of Statistics)'
df.loc[df.institution.str.contains(
    'CMU|Mellon', case=False), 'institution'] = 'Carnegie Mellon University (Department of Statistics)'
df.loc[df.institution.str.contains('wash|seat', case=False) & ~df.institution.str.contains(
    'Louis|George|state', case=False), 'institution'] = 'University of Washington (Department of Statistics)'
df.loc[df.institution.str.contains(
    'duke', case=False), 'institution'] = 'Duke University (Department of Statistical Science)'
df.loc[df.institution.str.contains('Michigan', case=False) & ~df.institution.str.contains(
    'State|Western|Central|Tech', case=False), 'institution'] = 'University of Michigan--Ann Arbor (Department of Statistics)'
df.loc[df.institution.str.contains('Penn|Whar', case=False) & ~df.institution.str.contains(
    'state', case=False), 'institution'] = 'University of Pennsylvania (Department of Statistics)'
df.loc[df.institution.str.contains('Columbia', case=False) & ~df.institution.str.contains(
    'British|Missouri|College|South', case=False), 'institution'] = 'Columbia University (Department of Statistics)'
df.loc[df.institution.str.contains('NCSU|Carolina S|NC S', case=False),
       'institution'] = 'North Carolina State University--Raleigh (Department of Statistics)'
df.loc[df.institution.str.contains('Wisc|Madison|UWM', case=False) & ~df.institution.str.contains(
    'Milwaukee|James', case=False), 'institution'] = 'University of Wisconsin--Madison (Department of Statistics)'
df.loc[df.institution.str.contains('North Caro|UNC|Chap', case=False) & ~df.institution.str.contains(
    'State|Charlotte', case=False), 'institution'] = 'University of North Carolina--Chapel Hill (Department of Statistics & Operations Research)'
df.loc[df.institution.str.contains(
    'Cornell', case=False), 'institution'] = 'Cornell University (Department of Statistical Science)'
df.loc[df.institution.str.contains(
    'Iowa S|ISU', case=False), 'institution'] = 'Iowa State University (Department of Statistics)'
df.loc[df.institution.str.contains('Penn State|PSU|Pennsylvania State|Penn. State', case=False),
       'institution'] = 'Pennsylvania State University (Department of Statistics)'
df.loc[df.institution.str.contains('Texas A&|TAMU|A &', case=False),
       'institution'] = 'Texas A&M University--College Station (Department of Statistics)'
df.loc[df.institution.str.contains(
    'UMN|nesota', case=False), 'institution'] = 'University of Minnesota--Twin Cities (School of Statistics)'
df.loc[df.institution.str.contains('Purdue', case=False) & ~df.institution.str.contains(
    'India', case=False), 'institution'] = 'Purdue University--West Lafayette (Department of Statistics)'
df.loc[df.institution.str.contains('JHU|Johns|Hopkins', case=False),
       'institution'] = 'Johns Hopkins University (Department of Applied Mathematics and Statistics)'
df.loc[df.institution.str.contains('Dav|daiv|Dacis', case=False),
       'institution'] = 'University of California--Davis (Department of Statistics)'
df.loc[df.institution.str.contains(
    'UCLA|Los', case=False), 'institution'] = 'University of California--Los Angeles (Department of Statistics)'
df.loc[df.institution.str.contains(
    'Yale', case=False), 'institution'] = 'Yale University (Department of Statistics)'
df.loc[df.institution.str.contains(
    'OSU|ohio s', case=False), 'institution'] = 'Ohio State University (Department of Statistics)'
df.loc[df.institution.str.contains('Illin|uiuc', case=False) & ~df.institution.str.contains(
    'Chicago|North|State', case=False), 'institution'] = 'University of Illinois--Urbana-Champaign (Department of Statistics)'
df.loc[df.institution.str.contains('Rutgers', case=False) & ~df.institution.str.contains(
    'education', case=False), 'institution'] = 'Rutgers University--New Brunswick (Department of Statistics and Biostatistics)'
df.loc[df.institution.str.contains('Florida|ufl', case=False) & ~df.institution.str.contains(
    'central|south|State', case=False), 'institution'] = 'University of Florida (Department of Statistics)'
df.loc[df.institution.str.contains('Iowa', case=False) & ~df.institution.str.contains(
    'State', case=False), 'institution'] = 'University of Iowa (Department of Statistics and Actuarial Science)'
df.loc[df.institution.str.contains(
    'Rice', case=False), 'institution'] = 'Rice University (Department of Statistics)'
df.loc[df.institution.str.contains(
    'Colorado St', case=False), 'institution'] = 'Colorado State University (Department of Statistics)'
df.loc[df.institution.str.contains('Florida Sta|FSU', case=False),
       'institution'] = 'Florida State University (Department of Statistics)'
df.loc[df.institution.str.contains(
    'conn', case=False), 'institution'] = 'University of Connecticut (Department of Statistics)'
df.loc[df.institution.str.contains('Michigan State|MSU', case=False),
       'institution'] = 'University of Connecticut (Department of Statistics)'
df.loc[df.institution.str.contains(
    'UCI|irvine', case=False), 'institution'] = 'University of California--Irvine (Department of Statistics)'
df.loc[df.institution.str.contains('Austin|austion', case=False),
       'institution'] = 'University of Texas--Austin (Department of Statistics and Data Science)'
df.loc[df.institution.str.contains('Northwestern', case=False),
       'institution'] = 'Northwestern University (Department of Statistics)'
df.loc[df.institution.str.contains(
    'Pitt', case=False), 'institution'] = 'University of Pittsburgh (Department of Statistics)'
df.loc[df.institution.str.contains('george', case=False) & ~df.institution.str.contains(
    'town|mason', case=False), 'institution'] = 'University of Pittsburgh (Department of Statistics)'
df.loc[df.institution.str.contains('new york|nyu', case=False) & ~df.institution.str.contains(
    'state|columbia', case=False), 'institution'] = 'New York University (Department of Information, Operations, and Management Sciences)'
df.loc[df.institution.str.contains('george|uga', case=False) & ~df.institution.str.contains(
    'state|tec', case=False), 'institution'] = 'University of Georgia (Department of Statistics)'
df.loc[df.institution.str.contains('Missouri', case=False) & ~df.institution.str.contains(
    'S & T', case=False), 'institution'] = 'University of Missouri--Columbia (Department of Statistics)'
df.loc[df.institution.str.contains('Virginia Tech|VT|Virginia Polytechnic|VirginiaTech|Virgina Tech',
                                   case=False), 'institution'] = 'Virginia Tech (Department of Statistics)'
df.loc[df.institution.str.contains('UCSB|Barbara|Babara|Barabara', case=False),
       'institution'] = 'University of California--Santa Barbara (Department of Statistics and Applied Probability)'
df.loc[df.institution.str.contains('Indiana|IUB', case=False) & ~df.institution.str.contains(
    'purdue', case=False), 'institution'] = 'Indiana University--Bloomington (Department of Statistics)'
df.loc[df.institution.str.contains('smu|Methodist', case=False),
       'institution'] = 'Southern Methodist University (Department of Statistical Science)'
df.loc[df.institution.str.contains('Maryland|Baltimore', case=False) & ~df.institution.str.contains(
    'college|park', case=False), 'institution'] = 'University of Maryland--Baltimore County (Department of Mathematics and Statistics)'
df.loc[df.institution.str.contains('of Virginia|Virginia University|UVA', case=False) & ~df.institution.str.contains(
    'education', case=False), 'institution'] = 'University of Virginia (Department of Statistics)'
df.loc[df.institution.str.contains(
    'Oregon', case=False), 'institution'] = 'Oregon State University (Department of Statistics)'
df.loc[df.institution.str.contains('UCR|Riverside', case=False),
       'institution'] = 'University of California--Riverside (Department of Statistics)'
df.loc[df.institution.str.contains('Amherst|mass', case=False),
       'institution'] = 'University of Massachusetts--Amherst (Department of Mathematics and Statistics)'
df.loc[df.institution.str.contains('South Carolina|Southern Carolina', case=False),
       'institution'] = 'University of South Carolina (Department of Statistics)'
df.loc[df.institution.str.contains('Arizona S|ASU', case=False),
       'institution'] = 'Arizona State University (School of Mathematical & Statistical Sciences)'
df.loc[df.institution.str.contains('case|Reserve|CWRU', case=False),
       'institution'] = 'Case Western Reserve University (Department of Statistics)'
df.loc[df.institution.str.contains(
    'temple', case=False), 'institution'] = 'Temple University (Department of Statistics)'
df.loc[df.institution.str.contains(
    'baylor', case=False), 'institution'] = 'Baylor University (Department of Statistical Science)'
df.loc[df.institution.str.contains(
    'Mason|GMU', case=False), 'institution'] = 'George Mason University (Department of Statistics)'
df.loc[df.institution.str.contains('Kansas S|KSU', case=False) & ~df.institution.str.contains(
    'central|south|State', case=False), 'institution'] = 'Kansas State University (Department of Statistics)'
df.loc[df.institution.str.contains('Colorado Denver', case=False),
       'institution'] = 'University of Colorado--Denver (Department of Mathematical and Statistical Sciences)'
df.loc[df.institution.str.contains(
    'kentucky', case=False), 'institution'] = 'University of Kentucky (Department of Statistics)'
df.loc[df.institution.str.contains('Commonwealth', case=False),
       'institution'] = 'Virginia Commonwealth University (Department of Statistics)'
df.loc[df.institution.str.contains(
    'Diego S', case=False), 'institution'] = 'San Diego State University (Department of Mathematics and Statistics)'
df.loc[df.institution.str.contains('UNC Charlotte', case=False),
       'institution'] = 'University of North Carolina--Charlotte (Department of Mathematics and Statistics)'
df.loc[df.institution.str.contains(
    'Antonio', case=False), 'institution'] = 'University of Texas--San Antonio (Department of Management Science and Statistics)'
df.loc[df.institution.str.contains(
    'Auburn', case=False), 'institution'] = 'Auburn University (Department of Mathematics and Statistics)'


df.loc[df.institution.str.contains('UCSD|San Diego', case=False) & ~df.institution.str.contains(
    'State', case=False), 'institution'] = 'University of California--San Diego'
df.loc[df.institution.str.contains('Southern California|USC|South Califor',
                                   case=False), 'institution'] = 'University of Southern California'

df.loc[df.institution.str.contains(
    'Toronto', case=False), 'institution'] = 'University of Toronto'
df.loc[df.institution.str.contains('British Columbia', case=False) | df.institution.str.contains(
    'UBC', case=False), 'institution'] = 'University of British Columbia'
df.loc[df.institution.str.contains(
    'Waterl', case=False), 'institution'] = 'University of Waterloo'


# merge stat_rank and overall_rank
# add two new columns: USnew_stat_score and USnew_stat_score
df1 = pd.read_csv('../data/USnew_stat_rank.csv')
df1["postal"] = df1["district"].str.split(',', expand = True).iloc[:,1].str.strip()
df2 = pd.read_csv('../data/USnew_overall_rank.csv')
df = pd.merge(df, df1[['score', 'name', 'postal']],
              left_on='institution', right_on='name')
df = df.rename(columns={'score': 'USnew_stat_score'})
df.name = df.name.str.replace(r' ?\([^)]+\)', '')
df = pd.merge(df, df2[['score', 'name']], on='name')
df = df.rename(columns={'score': 'USnew_overall_score'})
df = df.drop(columns=['name', "Unnamed: 0"])

def decision_tree_process(df):
    df.loc[df.admission_status=='Wait listed', 'admission_status'] = 'Other'
    df.loc[df.admission_status=='Interview', 'admission_status'] = 'Other'
    df.loc[df.degree=='Other', 'degree'] = 'Masters'
    df.loc[df.admission_via=='Postal Service', 'admission_via'] = 'Other'
    df.loc[df.admission_via=='Phone', 'admission_via'] = 'Other'
    df.loc[df.ST=='O', 'ST'] = 'I'
    df = df.dropna()
    X = df[['degree', 'admission_via', 'ST', 'Undergrad_GPA', 'GRE_V', 'GRE_Q', 'GRE_W', 'GRE_sub', 'USnew_stat_score', 'USnew_overall_score']]
    y = df.admission_status
    categorical_feature_mask = X.dtypes=='category'
    ohe = OneHotEncoder(sparse=False)
    X_ohe = ohe.fit_transform(X.loc[:, categorical_feature_mask])
    X_ohe = pd.DataFrame(X_ohe, columns=ohe.get_feature_names(['degree', 'admission_via', 'ST']), index=X.index)
    X = pd.concat([X_ohe, X.loc[:, ~categorical_feature_mask]], axis=1)
    return X, y




map_us = gpd.read_file('../data/states_province/ne_110m_admin_1_states_provinces.shx')
# data munging
summary_gradcafe = df[["postal", "admission_status"]].groupby("postal").apply(lambda df: np.sum(df["admission_status"] == "Accepted") / df["admission_status"].count()).reset_index()
summary_gradcafe["admission_rate"] = df[["postal", "admission_status"]].groupby("postal").count().reset_index().iloc[:,1]
summary_gradcafe["stat_score"] = df[["USnew_stat_score", "postal"]].groupby("postal").mean().reset_index().iloc[:,1]
summary_gradcafe["overall_score"] = df[["USnew_overall_score", "postal"]].groupby("postal").mean().reset_index().iloc[:,1]
summary_gradcafe["sum_stat_score"] = df[["USnew_stat_score", "postal"]].groupby("postal").sum().reset_index().iloc[:,1]
summary_gradcafe = summary_gradcafe.rename(columns = {0 : "admission_rate", "admission_rate": "num_applicants"})

map_us = map_us.merge(summary_gradcafe, on = "postal", how = 'left')
map_us.loc[map_us["num_applicants"].isna(), "num_applicants"]=0
map_us_point = map_us.copy()
map_us_point["rep"] = map_us["geometry"].centroid
map_us_point.set_geometry("rep", inplace = True)

#make copy to set labels
map_us["stat_score2"] = map_us["stat_score"]
map_us["admission_rate2"] = map_us["admission_rate"]
map_us["overall_score2"] = map_us["overall_score"]
map_us["sum_stat_score2"] = map_us["sum_stat_score"]
map_us["num_applicants2"] = map_us["num_applicants"]
map_us.loc[map_us["sum_stat_score2"].isna(), "sum_stat_score2"] = 'NaN'
map_us.loc[map_us["overall_score2"].isna(), "overall_score2"] = 'NaN'
map_us.loc[map_us["admission_rate2"].isna(), "admission_rate2"] = 'NaN'
map_us.loc[map_us["stat_score2"].isna(), "stat_score2"] = 'NaN'
map_us.loc[map_us["num_applicants2"].isna(), "num_applicants2"] = "NaN"
