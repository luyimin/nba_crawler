import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date

year = 2016
teams = pd.read_csv('team.csv')
BASE_URL = 'http://www.espn.com/nba/team/schedule/_/name/{0}/year/{1}'

match_id = []
dates = []
home_team = []
home_team_score = []
visit_team = []
visit_team_score = []

for index, row in teams.iterrows():
    team = row['team']
    
    # 檢查隊伍
    print(team)
    
    r = requests.get(BASE_URL.format(row['abbr_1'], year))
    content = r.text
    table = BeautifulSoup(content, 'html.parser').table
    rows =  table.find_all('tr')[2:]
    
    
    for row in rows: 
        cols = row.find_all('td')

        
        try:
            match_id.append(cols[2].find('a').get('href').split('/id/')[1])
            
            # 決定主客隊
            home = True if cols[1].li.text == 'vs' else False
            other_team = cols[1].find_all('a')[1].text
            
            won = True if cols[2].span.text == 'W' else False
            score = cols[2].a.text.split(' ')[0].split('-')
            # 決定主客隊分數
            if home:
                if won:
                    home_team_score.append(score[0])
                    visit_team_score.append(score[1])
                else:
                    home_team_score.append(score[1])
                    visit_team_score.append(score[0])
            else:
                if won:
                    home_team_score.append(score[1])
                    visit_team_score.append(score[0])
                else:
                    home_team_score.append(score[0])
                    visit_team_score.append(score[1])


            home_team.append(team if home else other_team)
            visit_team.append(team if not home else other_team)
            d = datetime.strptime(cols[0].text, '%a, %b %d')
            dates.append(date(year, d.month, d.day))

            
                    
        except Exception as e:
            pass # Not all columns row are a game, is OK
            print(e)
        

            
            
dic = {'id': match_id, 'date': dates, 'home_team': home_team, 'visit_team': visit_team,
        'home_team_score': home_team_score, 'visit_team_score': visit_team_score}

games = pd.DataFrame(dic).drop_duplicates(cols='id').set_index('id')
print(games)

games.to_csv('game.csv')
