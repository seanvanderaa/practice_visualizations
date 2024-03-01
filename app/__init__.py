from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import functions

app = Flask(__name__)
app.secret_key = 'MoreGarlic420#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/songs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

global id_key, id_secret

def update_key_internal():
    global id_key
    global id_secret
    functions.update_key()
    id_key, id_secret = functions.get_credentials()

""" def refresh_spotify_token():
    try:
        oauth = SpotifyOAuth(
            client_id='your_client_id',  # Replace with your client ID
            client_secret='your_client_secret',  # Replace with your client secret
            redirect_uri='your_redirect_uri',  # Replace with your redirect URI
            scope='your_scopes'  # Replace with your scopes
        )
        token_info = oauth.refresh_access_token(session['token_info']['refresh_token'])
        return token_info
    except Exception as e:
        print(f"Error refreshing token: {e}")
        return None """


id_key, id_secret = functions.get_keys()

db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()

# Spotipy Configuration
id_key, id_secret = functions.get_keys()
scope = 'user-library-read user-read-private user-read-email user-top-read'
redirect_uri = 'https://127.0.0.1:5000/authorized'  # Change to your actual redirect URI

sp_oauth = SpotifyOAuth(client_id=id_key, client_secret=id_secret, redirect_uri=redirect_uri, scope=scope)

from app import views
