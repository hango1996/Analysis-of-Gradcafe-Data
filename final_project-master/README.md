# Gradcafe: Who Got Accepted by My Dream School?

### Group member: Han Chen, Zhixuan Shao, Haoning Xue, Yidong Zhou

[Gradcafe](https://www.thegradcafe.com/) is a platform where grad school applicants share admission status and communicate updates. One thing all applicants need is information - when to expect an interview, whether being put in a waiting list or receiving an email starting with Congratulations. The uncertainty that comes with these questions can be relieved to certain degree with information from other applicants.

As freshly admitted grad students, we are curious about what we can know about application in Statistics over the last decade from [Gradcafe](https://www.thegradcafe.com/), where we have access to 10,000 application results from 2010 to 2020 with information on the program, year, applicant undergrad GPA, GRE result, admission status, etc.

We also incorporate two major university rankings in Statistics: [US News](https://www.usnews.com/best-colleges/rankings/national-universities) and [QS World University Rankings](https://www.topuniversities.com/university-rankings/world-university-rankings/2020) as these rankings are reliable indicators of academic reputation of a particular university and program, which can affect decisions of both applicants and programs significantly. Besides, these two rankings are selected to represent the major domestic and international evaluation of universities.

With three datasets on admission result and ranking scraped, we are able to answer two major questions below.
1. What kind of programs are popular among the applicants in Statistics?
2. What kind of applicants are usually preferred by Statistics graduate programs?

# Dataset Description
### [gradcafe.csv](data/gradcafe.csv)

| Institution | Program | Degree | Season | Admission Status | Admission Via | Status | Data Added | Notes |
|    :---:    |  :---:  |  :---: |  :---: |      :---:       |     :---:     |  :---: |    :---:   | :---: |

### [USnew_overall_rank.csv](data/USnew_overall_rank.csv)

| Rank | Name | Score | Country | District |
|:---: |:---: | :---: |  :---:  |  :---:   |

### [USnew_stat_rank.csv](data/USnew_stat_rank.csv)

| Rank | Name | Score| District |
|:---: |:---: | :---:|  :---:   |

### [qs_rank.csv](data/qs_rank.csv)

| Institution | Location | Year | Rank | Overall Score | Academic Reputation | Employer Reputation | Citation per Paper | H-index citation |
|    :---:    |  :---:   |:---: | :---:|   :---:       |        :---:        |       :---:         |       :---:        |      :---:       |

# Repository Description
### [/code](code)
[clean.py](/code/clean.py): data cleaning of Gradcafe dataset

[crawler.py](/code/crawler.py): scraper of Gradcafe

[crawler_usnews.py](/code/crawler_usnews.py): scraper of US News overall ranking

[crawler_usnews2.py](/code/crawler_usnews2.py): scraper of US News ranking in Statistics

[plot_functions.py](/code/describe.py): contain functions for generating plots in jupyter notebooks

[qs_ranking_scraper.py](/code/qs_ranking_scraper.py): scraper of QS ranking in Statistics

### [/data](data)
[USnew_overall_rank.csv](/data/USnew_overall_rank.csv): US News overall ranking

[USnew_stat_rank.csv](/data/USnew_stat_rank.csv): US News ranking in Statistics

[gradcafe.csv](/data/gradcafe.csv): Gradcafe dataset

[qs_rank.csv](/data/qs_rank.csv): QS ranking in Statistics

### [/notebook](notebook)
[EDA.ipynb](/notebook/EDA.ipynb): analysis and report
