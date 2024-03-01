from spotipy import Spotify
from app import app, sp_oauth, views as v, db, functions as f, database as d
import time

def get_playlist_tracks(playlist_uri):
    playlist_id = playlist_uri.split(':')[-1]

    tracks = []
    next_url = f'playlists/{playlist_id}/tracks'
    while next_url:
        response = get_spotify_data(next_url)

        if response == "Retry":
            continue

        if isinstance(response, str):
            if response.startswith("Error"):
                error_message = response
                print(error_message)
                return []

        if isinstance(response, dict):
            tracks_data = response.get('items', [])
            tracks.extend(tracks_data)
            next_url = response.get('next')
            if next_url:
                next_url = next_url.replace('https://api.spotify.com/v1/', '')
        else:
            print("Unexpected response type")
            return []

    return tracks


def get_track_ids(tracks):
    return [track['track']['id'] for track in tracks if track['track']]

def get_audio_features(track_ids):
    features = []
    for track_id in track_ids:
        while True:
            response = get_spotify_data(f'audio-features/{track_id}')

            if response == "Retry":
                print(f"Retrying for track ID {track_id}")
                time.sleep(5)  
                continue

            elif isinstance(response, str) and response.startswith("Error"):
                error_message = response
                print(error_message)
                break 
            elif isinstance(response, dict):
                features.append(response)
                break 

            else:
                print(f"Unhandled response type: {response}")
                break

    return features


def print_oauth_response_attributes(oauth_response):
    for attribute in dir(oauth_response):
        attribute_value = getattr(oauth_response, attribute, None)
        print(f"{attribute}: {attribute_value}")
    print('\n Finished Response \n\n')

def get_spotify_oauth_token():
    return v.session.get('spotify_token')
    

def get_spotify_data(endpoint):
    try:
        token_info = v.session.get('token_info', None)
        if not token_info:
            return "Exception occurred: missing_token"

        spotify = Spotify(auth=token_info['access_token'])
        print("Get data 3!")
        return spotify._get(endpoint)
    except Exception as e:
        print(f"Exception occurred: {e}")
        return f"Exception occurred: {str(e)}"

def get_spotify_data_range(endpoint, timeframe):
    try:
        token_info = v.session.get('token_info', None)
        if not token_info:
            return "Exception occurred: missing_token"

        spotify = Spotify(auth=token_info['access_token'])
        if 'top/artists' in endpoint:
            endpoint += '?time_range=' + timeframe
        response = spotify._get(endpoint)
        return response
    except Exception as e:
        print(f"Exception occurred: {e}")
        return f"Exception occurred: {str(e)}"
    
def gather_user_data():
    user_profile = get_spotify_data('me')
    if isinstance(user_profile, str) and (user_profile == "Unauthorized" or user_profile == "Retry" or user_profile.startswith("Error")):
        error_message = user_profile
        return "Error"
    user_id = user_profile.get('id')
    
    if not d.profile_exists(user_id):
        print('Adding user')
        top_artists = get_spotify_data_range('me/top/artists', 'short_term')
        if top_artists== "Unauthorized" or top_artists == "Retry":
            return "Error"
        if isinstance(top_artists, str) and top_artists.startswith("Error"):
                    error_message = top_artists
                    print(error_message)
                    return "Error"
        artist_dict = {artist.get('name'): artist.get('id') for artist in top_artists.get('items', [])}
        artists = ', '.join(artist_dict)
        genre_counts = {}

        # Count the occurrences of each genre
        for artist in top_artists.get('items', []):
            for genre in artist.get('genres', []):
                if genre in genre_counts:
                    genre_counts[genre] += 1
                else:
                    genre_counts[genre] = 1

        # Sort genres by their occurrence count in descending order
        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)

        # Create a string of sorted genres by their frequency
        genres_str = ', '.join([genre[0] for genre in sorted_genres])
        print(genres_str)
        top_songs = get_spotify_data_range('me/top/tracks', 'short_term')
        if top_songs== "Unauthorized" or top_songs == "Retry":
            return "Error"
        if isinstance(top_songs, str) and top_songs.startswith("Error"):
                    error_message = top_songs
                    print(error_message)
                    return "Error"
        songs = d.load_songs(top_songs)
        x, y, averages, variance = f.generate_sonic_profile(songs)
        name = user_profile.get('display_name')
        email = user_profile.get('email')
        image_url = user_profile.get('images', [{}])[0].get('url')
        d.add_profile(user_id, name, email, image_url, genres_str, artists, averages, variance, x, y)
        profile_info = d.gather_profile_data(user_id)
        return profile_info
    else:
        print("retrieving user")
        profile_info = d.gather_profile_data(user_id)
        return profile_info