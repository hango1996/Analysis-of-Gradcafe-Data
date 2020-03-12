from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import numpy as np
import time



def get_stat_rank(headers = headers):
    '''
    This function parse the data from "https://www.usnews.com/best-graduate-schools/top-science-schools/statistics-rankings",
    We need to deal with the scrolling down issue of this page
    It is about statistics ranking in the United States.
    we select some key features like rank, name, score, and district. 
    We use selenium develop tool with Beautiful soup to scrape
    '''
    url = "https://www.usnews.com/best-graduate-schools/top-science-schools/statistics-rankings"
    browser = webdriver.Safari()
    browser.get('https://www.usnews.com/best-graduate-schools/top-science-schools/statistics-rankings')
    time.sleep(5)

    #scroll down until the end
    SCROLL_PAUSE_TIME = 2
    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    datalist = browser.find_elements_by_xpath("//table[@class='TableTabular__TableContainer-swxyo9-0 edxlVD']")
    soup = BeautifulSoup(browser.page_source, 'lxml')
    collset_content = soup.find_all(name = 'table', attrs = {'class': 'TableTabular__TableContainer-swxyo9-0 edxlVD'})
    results = collset_content[0].find_all(name = 'tr', attrs = {'class': ["TableTabular__TableRow-swxyo9-1 gxGITF", "zebra TableTabular__TableRow-swxyo9-1 gxGITF"]})
    item = 0
    for result in results[0:]:
        print("item_number{}".format(item))
        item = item + 1
        score = result.select_one(r'span[class="Span-aabx0k-0 RNL"]').text.strip()
        name = result.select_one(r'h3[class="Heading-bocdeh-1 iqkCSQ Heading__HeadingStyled-bocdeh-0-h3 dtIFQE"]').text.strip()
        district = result.select_one(r'p[class="Paragraph-s10q84gy-0 bgyixv"]').text.strip()
        rank0 = result.select_one(r'strong[class="NameRank__RankPosition-s4melbd-0 Wtokh Strong-s144f3me-0 cRVRij"]')
        if rank0 is None:
            rank = np.nan
        else:
            rank = rank0.text.strip()[1:3]
        yield {
            "score": score,
            "name": name,
            "rank": rank,
            "district": district
        }
    time.sleep(2)
    browser.quit()

data = []
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}
info = get_stat_rank(headers = headers)
for result in info:
    data.append(result)

df = pd.DataFrame(data)
df.to_csv(r"/Users/hango/Desktop/UCDavis(2019-)/winter2020/STA220/final_project/final_project-master/USnew_stat_rank.csv")
