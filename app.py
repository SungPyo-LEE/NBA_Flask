from flask import request, jsonify, render_template, Flask
from functools import wraps
from nba_api.stats.endpoints import BoxScorePlayerTrackV2
from nba_api.stats.static import teams
import json
import pandas as pd
app = Flask(__name__)

tracker_dict={}

r=BoxScorePlayerTrackV2(game_id='0021900247')
player_tracker=r.get_json()
player_tracker=json.loads(player_tracker)
tracker_result=player_tracker["resultSets"][0]
for j in range(0,len(tracker_result['headers'])):
    tracker_dict[tracker_result['headers'][j]]=[]
for k in range(0,len(tracker_result["rowSet"])):
    for j in range(0,len(tracker_result['headers'])):
        tracker_dict[tracker_result['headers'][j]].append(tracker_result["rowSet"][k][j])
last_game_tracker=pd.DataFrame(tracker_dict)

all_team=teams.get_teams()
teams_list=[]
team_set={}
for i in range(len(all_team)):
    team_set={
    'team_id':all_team[i]['id'],
    'team_name':all_team[i]['full_name'],
    'abbrev':all_team[i]['abbreviation'],
    'nickname':all_team[i]['nickname'],
    'city':all_team[i]['city']
        }
    
    teams=team_set.copy()
    teams_list.append(teams)
    team_set.clear()

@app.route("/",methods=['GET'])
def home():
    return render_template('home.html')

@app.route("/last_game_log",methods=['GET'])
def log_team_list():
    return render_template('last_game.html', results=teams_list)

@app.route("/last_game_log/<int:team_id>",methods=['GET'])
def team_log(team_id):
    return render_template('last_game.html', results=team_id)

#@app.route("/team", methods=['GET'])
#def teams():
#    return render_template('index.html',results=teams_list)\

#@app.route("/team/test", methods=['GET'])
#def roaster():
#    return "hi"

#@app.route("/Portland",methods=['GET'])
#def portland():
#    tables=[last_game_tracker.to_html(classes='female')]
#    return render_template('portland.html',title='Last game ON Portland', tables=tables,
#    titles = ['Portland_LAST_GAME'])

#@app.route("/Portland/test",methods=['GET'])
#def ping():
#    return 'Pong'



if __name__=="__main__":
	app.run(debug=True)