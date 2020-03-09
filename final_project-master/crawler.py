import requests
from chardet import detect
from bs4 import BeautifulSoup
import pandas as pd
import re


def get_admission_result(q="statistics", pp=250, page_num=1):
    url = "https://www.thegradcafe.com/survey/index.php"
    try:
        response = requests.get(url, params={"q": q, "pp": pp, "p": page_num})
    except requests.exceptions.RequestException:
        print("Request Failed")
        return None
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find('table', attrs={'class': 'submission-table'})
        results = table.select('tr')[1:]
        # the first tr is information about columns

        for result in results:
            institution = result.select_one(
                r'td[class*="tcol1"]').text
            program_degree_season = result.select_one(
                r'td[class="tcol2"]').text
            # print(program_degree_season)
            program, degree, season = re.match(
                r"(.+), (.+) \((.+)\)", program_degree_season).groups()
            admission_via_date = result.select_one('td[class*="tcol3"]')
            grade = admission_via_date.select_one('a[class="extinfo"]')
            if (grade is None):
                admission_status, admission_via, admission_date = re.match(
                    r'(.*) via (.*) on (.*) ', admission_via_date.text).groups()
            else:
                admission_status, admission_via, admission_date = re.match(
                    r'(.*) via (.*) on (.*) Under', admission_via_date.text).groups()
                last_x = ""
                for x in grade.stripped_strings:
                    if last_x == "Undergrad GPA":
                        Undergrad_GPA = x[2:]
                    elif last_x == "GRE General (V/Q/W)":
                        GRE_V, GRE_Q, GRE_W = re.match(
                            r"(.+)\/(.+)\/(.+)", x[2:]).groups()
                    elif last_x == "GRE Subject":
                        GRE_sub = x[2:]
                    last_x = x

            ST = result.select_one('td[class*="tcol4"]').text
            Date_added = result.select_one('td[class*="tcol5"]').text
            notes = result.select_one('td[class*="tcol6"]').text

            yield {
                "institution": institution,
                "program": program,
                "degree": degree,
                "season": season,
                "admission_status": admission_status,
                "admission_via": admission_via,
                "admission_date": admission_date,
                "ST": ST,
                "Date_added": Date_added,
                "notes": notes,
                "Undergrad_GPA": float(Undergrad_GPA) if (grade and Undergrad_GPA != 'n/a') else None,
                "GRE_V": int(GRE_V) if (grade and GRE_V != 'n/a') else None,
                "GRE_Q": int(GRE_Q) if (grade and GRE_Q != 'n/a') else None,
                "GRE_W": float(GRE_W) if (grade and GRE_W != 'n/a') else None,
                "GRE_sub": int(GRE_sub) if (grade and GRE_sub != 'n/a') else None
            }


data = []
for page_num in range(40):
    adminssion_results = get_admission_result(page_num=page_num)
    for result in adminssion_results:
        data.append(result)

df = pd.DataFrame(data)
df
df.to_csv("gradcafe.csv")
