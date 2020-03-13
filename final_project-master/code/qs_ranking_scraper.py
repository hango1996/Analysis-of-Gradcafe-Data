#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import time
import pandas as pd
from time import sleep
from selenium import webdriver


# In[47]:


#dataframe initiation
column_name = ['institution', 'location', 'year', 'rank', 'ovr_score', 'academic_reputation', 'employer_reputation', 'cite_per_paper', 'h_index_citation']
qs_rank = pd.DataFrame(columns = column_name)
qs_rank


# In[67]:


#start webdriver
driver = webdriver.Chrome("../chromedriver")


# In[197]:


#get ranking info for 2014-2020 manually
#number of ranking & html change for every year
year = 2014
url = 'https://www.topuniversities.com/university-rankings/university-subject-rankings/' + str(year) + '/statistics-operational-research'
driver.get(url)


# In[198]:


#manully click to show all ranking in one page
temp_rank = driver.find_elements_by_xpath('//tr[@role="row"]')


# In[200]:


#get all the rank info
rank_list = []
for i in range(3, 203):
    temp = temp_rank[i].text
    rank = temp.splitlines()
    rank_list.append(rank)


# In[202]:


#manually click button to turn to ranking indicator page
temp_score = driver.find_elements_by_xpath('//tr[@role="row"]')


# In[204]:


#get all ranking indicator info
score_list = []
for i in range(205, 405):
    temp = temp_score[i].text
    score = temp.splitlines()
    score_list.append(score)


# In[206]:


#attach info in two lists to the dataframe
#need manual change as column name changes each year
for i in range(0, 200):
    institution = rank_list[i][1]; location = rank_list[i][3]; year = 2014; ranking = rank_list[i][0]
    if i < 50:
        overall_score = score_list[i][2]; aca_rep = score_list[i][3]; emp_rep = score_list[i][4]; paper_cite = score_list[i][5]; h_index = score_list[i][6]
    else:
        overall_score = 'NaN'; aca_rep = score_list[i][2]; emp_rep = score_list[i][3]; paper_cite = score_list[i][4]; h_index = score_list[i][5]
    
    temp_list = [institution, location, year, ranking, overall_score, aca_rep, emp_rep, paper_cite, h_index]
    qs_rank.loc[len(qs_rank), :] = temp_list


# In[207]:


qs_rank


# In[208]:


qs_rank.to_csv ('qs_rank.csv', index = False, header=True)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




