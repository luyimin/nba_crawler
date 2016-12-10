import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup


url = 'http://espn.go.com/nba/teams'
r = requests.get(url)

f = open('team.csv', 'w')

soup = BeautifulSoup(r.text)
tables = soup.find_all('ul', class_='medium-logos')

teams = []
abbr_1 = []
abbr_2 = []
teams_urls = []
for table in tables:
    lis = table.find_all('li')
    for li in lis:
        info = li.h5.a
        teams.append(info.text)
        url = info['href']
        teams_urls.append(url)
        abbr_1.append(url.split('/')[-2])
        abbr_2.append(url.split('/')[-1])


dic = {'url': teams_urls, 'abbr_1': abbr_1, 'abbr_2': abbr_2}

teams = pd.DataFrame(dic, index=teams)
teams.index.name = 'team'
print(teams)

teams.to_csv('team.csv')

f.close()