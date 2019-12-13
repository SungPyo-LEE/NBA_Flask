from flask import request, jsonify, render_template, Flask, send_file, make_response
from functools import wraps
from nba_api.stats.endpoints import BoxScorePlayerTrackV2
from nba_api.stats.static import teams
from nba_api.stats.endpoints import TeamGameLog


from service import TeamService
from view    import create_endpoints

class Services:
    pass

def create_app():
    app=Flask(__name__)
    services = Services
    services.team_service=TeamService()

    create_endpoints(app, services)
    return app

app=create_app()
if __name__ == '__main__':
    app.run()