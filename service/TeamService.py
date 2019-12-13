
from nba_api.stats.endpoints import BoxScorePlayerTrackV2
from nba_api.stats.static import teams
from nba_api.stats.endpoints import TeamGameLog

import json
import pandas as pd
class TeamService:
    #DB가 있으면 안 해도 됨
    def __init__(self):
        pass
    def team_roaster(self):
        all_team=teams.get_teams()
        all_teams=[]
        for i in range(len(all_team)):
            team={}
            team.update(
                {
            'team_id':all_team[i]['id'],
            'team_name':all_team[i]['full_name'],
            'abbrev':all_team[i]['abbreviation'],
            'nickname':all_team[i]['nickname'],
            'city':all_team[i]['city']
                }
            )
            all_team.append(team)
        return [teams for teams in all_team]

    def get_team_id(team_abbrev):
    	all_team=teams.get_teams()
    	for team in all_team:
        	for key, value in team.items():
        		if key=='abbreviation':
        			if value==team_abbrev:
        				return team['id']
##DB에 게임 로그를 안 넣어둘 경우
    def get_gamelist(self,team_abbrev):
        team_id=TeamService.get_team_id(team_abbrev)
        r= TeamGameLog(season='2019-20', season_type_all_star='Regular Season',team_id=team_id)
        career=r.get_json()
        career=json.loads(career)
        game_log=career['resultSets'][0]['rowSet']
        games_list=[]
        for i in range(len(game_log)):
            game_set={}
            game_set={
            'game_id':game_log[i][1],
            'game_date':game_log[i][2],
            'game_team':game_log[i][3]
            }
            games_list.append(game_set)
        return [game for game in games_list]

    def get_game_log(self,game_id):
    	tracker_dict={}
    	r=BoxScorePlayerTrackV2(game_id=game_id)
    	player_tracker=r.get_json()
    	player_tracker=json.loads(player_tracker)
    	tracker_result=player_tracker["resultSets"][0]
    	for j in range(0,len(tracker_result['headers'])):
    		tracker_dict[tracker_result['headers'][j]]=[]
    	for k in range(0,len(tracker_result["rowSet"])):
    		for j in range(0,len(tracker_result['headers'])):
    			tracker_dict[tracker_result['headers'][j]].append(tracker_result["rowSet"][k][j])
    	last_game_tracker=pd.DataFrame(tracker_dict)
    	return last_game_tracker