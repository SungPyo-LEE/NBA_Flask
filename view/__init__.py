from flask import request, jsonify, render_template, Flask, send_file, make_response
from functools import wraps
from nba_api.stats.endpoints import BoxScorePlayerTrackV2
from nba_api.stats.static import teams
from nba_api.stats.endpoints import TeamGameLog
import json
import pandas as pd

#get_graph_view
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO, StringIO

from functools import wraps, update_wrapper
from datetime import datetime
app = Flask(__name__)
def nocache(view):
  @wraps(view)
  def no_cache(*args, **kwargs):
    response = make_response(view(*args, **kwargs))
    response.headers['Last-Modified'] = datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response      
  return update_wrapper(no_cache, view)





def create_endpoints(app,services):
    team_service = services.team_service

    @app.route("/",methods=['GET'])
    def home():
        return render_template('home.html')

    @app.route("/game_log",methods=['GET'])
    def game_log():
        results=team_service.team_roaster()
        return render_template('team_list.html', results=results)

        ###게임아이디 가져오기
    @app.route("/game_log/<string:abbrev>",methods=['GET'])
    def team_game_list(abbrev):
        games_list=team_service.get_gamelist(abbrev)
        return render_template('OKC_game_id.html', results=games_list, abbrev=abbrev)

    @app.route('/game_log/<string:abbrev>/<string:game_id>', methods=['GET'])
    def team_game_log(abbrev,game_id):
        tracker=team_service.get_game_log(game_id)
        tables=[tracker.to_html(classes='female')]
        return render_template('last_game_dataframe.html',title='Last game ON Portland', tables=tables, titles='saxycow')

    ##view_function
    @app.route('/game_log/<string:abbrev>/<string:game_id>/pass')
    @nocache
    def fig(abbrev,game_id):
        last_game_tracker=team_service.get_game_log(game_id)
        plt.rcParams["figure.figsize"] = (10,4)
        plt.rcParams['lines.linewidth'] = 2
        plt.rcParams['lines.color'] = 'r'
        plt.rcParams['axes.grid'] = True
        y=list(last_game_tracker["PASS"])
        x=list(last_game_tracker["PLAYER_NAME"])
        plt.bar(x, y,  color="blue")
        img = BytesIO()
        plt.savefig(img, format='png', dpi=300)
        img.seek(0)## object를 읽었기 때문에 처음으로 돌아가줌
        return send_file(img, mimetype='image/png')

