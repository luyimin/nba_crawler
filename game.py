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
    team, url = row['team'], row['url']
    print(team)
    
    r = requests.get(BASE_URL.format(row['abbr_1'], year))
    content = r.text
    table = BeautifulSoup(content, 'html.parser').table
    
    for row in table.find_all('tr')[2:]: 
        columns = row.find_all('td')
        
        print(columns[1].find_all('a'))
        
        match_id.append(columns[2].a['href'].split('/id/')[1])
        home = True if columns[1].li.text == 'vs' else False
        other_team = columns[1].find_all('a')[1].text
        score = columns[2].a.text.split(' ')[0].split('-')
        won = True if columns[2].span.text == 'W' else False

       
        home_team.append(team if home else other_team)
        visit_team.append(team if not home else other_team)
        d = datetime.strptime(columns[0].text, '%a, %b %d')
        dates.append(date(year, d.month, d.day))

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
        

            
            
dic = {'id': match_id, 'date': dates, 'home_team': home_team, 'visit_team': visit_team,
        'home_team_score': home_team_score, 'visit_team_score': visit_team_score}

games = pd.DataFrame(dic).drop_duplicates(cols='id').set_index('id')
print(games)

games.to_csv('game.csv')