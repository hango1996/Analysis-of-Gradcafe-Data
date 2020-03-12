import requests
from chardet import detect
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np



def get_global_rank(headers, page_num = 1):
    '''
    This function parse the data from the website "https://www.usnews.com/education/best-global-universities/rankings"
    It is about the overall rank in the world.
    We select some key features including rank, name, score, conutry and district.
    We use request function and Beautiful soup to scrape
    '''
    print("Page_num{}".format(page_num))
    url = "https://www.usnews.com/education/best-global-universities/rankings" + '?page=' + str(page_num)
    try:
        response = requests.get(url, headers = headers)
    except requests.exceptions.RequestException:
        print("Request Failed")
        return None
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        collset_content = soup.find_all(name = 'div', attrs = {'class': 'maincontent'})
        results = collset_content[0].find_all(name = 'div', attrs = {'class': "sep"})
        item = 0
        for result in results:
            #print("item_number{}".format(item))
            item = item + 1
            score = result.select_one(r'div[class="t-large t-strong t-constricted"]').text
            name = result.select_one(r'h2[class="h-taut"]').text.strip()
            country_info = result.select_one(r'div[class="t-taut"]').text.strip().split('\n')
            if len(country_info) == 2:
                [country, district] = country_info
            elif len(country_info) == 1:
                country = country_info[0]
                district = np.nan
            else:
                country = np.nan
                district = np.nan
            rank = result.select_one(r'span[class="rankscore-bronze"]').text.strip()[1:4].strip()
            yield {
                "rank": rank,
                "name": name,
                "score": score,
                "country": country,
                "district": district
            }














headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}
page_num = 100
data = []
for page_num in range(page_num):
    info = get_global_rank(page_num = page_num + 1, headers = headers)
    for result in info:
        data.append(result)

df = pd.DataFrame(data)
df.to_csv(r"/Users/hango/Desktop/UCDavis(2019-)/winter2020/STA220/final_project/final_project-master/USnew_overall_rank.csv")
