import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from secrets import CLIENT_ID, CLIENT_SECRET

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))