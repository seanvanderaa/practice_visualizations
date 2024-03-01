from app import db, visualizations as v, views as main, spotify as s

class mainbase_songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.String(255))
    tempo = db.Column(db.Float)          # Tempo of the song
    danceability = db.Column(db.Float)   # Danceability measure
    valence = db.Column(db.Float)        # Valence measure
    loudness = db.Column(db.Float)       # Loudness in decibels
    energy = db.Column(db.Float)         # Energy measure
    speechiness = db.Column(db.Float)    # Speechiness measure
    acousticness = db.Column(db.Float)   # Acousticness measure
    name = db.Column(db.String(255))  # Field for the song name
    artist = db.Column(db.String(255))  # Field for the artist name
    album_cover = db.Column(db.String(255))
    album = db.Column(db.String(255))
    popularity = db.Column(db.Float)
    preview_url = db.Column(db.String(255))
    uri = db.Column(db.String(255))
    external_url_web = db.Column(db.String(255))
    external_url_app = db.Column(db.String(255))

class cache_playlists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    num_tracks = db.Column(db.Float)
    image_url = db.Column(db.String(255))
    uri = db.Column(db.String(255))

class profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255))
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    genres = db.Column(db.Text)
    artists = db.Column(db.Text)
    tempo = db.Column(db.Float) 
    danceability = db.Column(db.Float)
    valence = db.Column(db.Float)
    loudness = db.Column(db.Float) 
    energy = db.Column(db.Float) 
    speechiness = db.Column(db.Float) 
    acousticness = db.Column(db.Float)   
    popularity = db.Column(db.Float)
    variance = db.Column(db.Float)  
    x = db.Column(db.Float)  
    y = db.Column(db.Float)  


def load_songs(tracks):
    song_data = []
    for track in tracks:
        track_id = track.get('id')
        print(track_id)
        existing_song = mainbase_songs.query.filter_by(song_id=track_id).first()
        # Check if song exists in mainbase_songs
        if existing_song:
            # If song exists, create a new playlist_songs entry with existing data
            song_attributes = {
                'song_id': existing_song.song_id,
                'name': existing_song.name,
                'artist': existing_song.artist,
                'album_cover': existing_song.album_cover,
                'tempo': existing_song.tempo,
                'danceability': existing_song.danceability,
                'valence': existing_song.valence,
                'loudness': existing_song.loudness,
                'energy': existing_song.energy,
                'speechiness': existing_song.speechiness,
                'acousticness': existing_song.acousticness,
                'uri': existing_song.uri,
                'popularity': existing_song.popularity
            }
        else:
            print("Song not in .db")
            artist_info = track.get('artists', [{}])
            artist_name = artist_info[0].get('name') if artist_info else None
            song_name = track.get('name')
            album_info = track.get('album', {})
            album_name = album_info.get('name')
            album_images = album_info.get('images', [{}])
            album_cover_url = album_images[0].get('url') if album_images else 'default_image_url'
            popularity = track.get('popularity')
            preview_url = track.get('preview_url')
            uri = track.get('uri')
            external_urls = track.get('external_urls', {})
            external_url_web = external_urls.get('spotify')
            audio_features = s.get_audio_features(track_id)
            new_mainbase_song = mainbase_songs(
                song_id=track_id,
                name=song_name,
                artist=artist_name,
                album_cover=album_cover_url,
                album=album_name,
                tempo=audio_features.get('tempo'),
                danceability=audio_features.get('danceability'),
                valence=audio_features.get('valence'),
                loudness=audio_features.get('loudness'),
                energy=audio_features.get('energy'),
                speechiness=audio_features.get('speechiness'),
                acousticness=audio_features.get('acousticness'),
                popularity=popularity,
                preview_url=preview_url,
                uri=uri,
                external_url_web=external_url_web,
                external_url_app=external_urls
            )
            song_attributes = {
                'song_id': track_id,
                'name': song_name,
                'artist': artist_name,
                'album_cover': album_cover_url,
                'tempo': audio_features.get('tempo'),
                'danceability': audio_features.get('danceability'),
                'valence': audio_features.get('valence'),
                'loudness': audio_features.get('loudness'),
                'energy': audio_features.get('energy'),
                'speechiness': audio_features.get('speechiness'),
                'acousticness': audio_features.get('acousticness'),
                'uri': uri,
                'popularity': popularity
            }
            db.session.add(new_mainbase_song)

        db.session.commit()
        song_data.append(song_attributes)
    return song_data

def load_playlists(playlist_details):
    for detail in playlist_details:
        new_playlist = cache_playlists(
            name=detail['name'],
            num_tracks=detail['total_tracks'],
            image_url=detail['image_url'],
            uri=detail['uri']
        )
        db.session.add(new_playlist)
    db.session.commit()

def get_playlists():
    return cache_playlists.query.all()

def clear_cache_playlists():
    try:
        cache_playlists.query.delete()
        db.session.commit()
    except Exception as e:
        print(f"Error clearing cache_playlists: {e}")
        db.session.rollback()
        raise

def add_profile(user_id, name, email, image_url, genres, artists, features, variance, x, y):
    tempo = features["tempo"]
    acousticness = features["acousticness"]
    danceability = features["danceability"]
    valence = features["valence"]
    energy = features['energy']
    speechiness = features['speechiness']
    popularity = features['popularity']
    loudness = features['loudness']
    new_profile = profiles(
        user_id = user_id,
        name = name,
        email = email,
        image_url = image_url,
        genres = genres,
        artists = artists,
        tempo = tempo,
        loudness=loudness,
        acousticness = acousticness,
        danceability = danceability,
        valence = valence,
        energy = energy,
        speechiness = speechiness,
        popularity = popularity,
        variance = variance,
        x = x,
        y = y,
    )
    db.session.add(new_profile)
    db.session.commit()

def gather_profile_data(user_id):
    profile = profiles.query.filter_by(user_id=user_id).first()

    if profile:
        profile_info = {
            "user_id": profile.user_id,
            "name": profile.name,
            "email": profile.email,
            "image_url": profile.image_url,
            "genres": profile.genres,
            "artists": profile.artists,
            "tempo": profile.tempo,
            "acousticness": profile.acousticness,
            "danceability": profile.danceability,
            "valence": profile.valence,
            "energy": profile.energy,
            "speechiness": profile.speechiness,
            "popularity": profile.popularity,
            "variance": profile.variance,
            "x": profile.x,
            "y": profile.y
        }
        return profile_info
    else:
        return None  # or handle the case where no profile is found

def profile_exists(user_id):
    return profiles.query.filter_by(user_id=user_id).first() is not None

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sqlalchemy import func

def song_recommender(tracks):
    print("Here")

    tracks_df = pd.DataFrame(tracks)

    pca = PCA(n_components=3)
    tracks_reduced = pca.fit_transform(tracks_df[['tempo', 'danceability', 'valence', 'loudness', 'energy', 'speechiness', 'acousticness', 'popularity']])

    kmeans = KMeans(n_clusters=4) 
    clusters = kmeans.fit_predict(tracks_reduced)

    recommended_songs = []

    for cluster in set(clusters):
        cluster_center = kmeans.cluster_centers_[cluster]
        original_center = pca.inverse_transform(cluster_center)

        query = db.session.query(mainbase_songs)
        for i, attr in enumerate(['tempo', 'danceability', 'valence', 'loudness', 'energy', 'speechiness', 'acousticness', 'popularity']):
            tolerance = 10 if attr in ['tempo', 'popularity'] else 0.3
            query = query.filter(func.abs(getattr(mainbase_songs, attr) - original_center[i]) < tolerance)

        cluster_songs = query.all()
        recommended_songs.extend(cluster_songs)

    result = format_songs(recommended_songs)

    return result

def format_songs(songs):
    # Format the songs into the desired structure
    return [{
        'song_id': song.song_id,
        'name': song.name,
        'artist': song.artist,
        'album_cover': song.album_cover,
        'tempo': song.tempo,
        'danceability': song.danceability,
        'valence': song.valence,
        'loudness': song.loudness,
        'energy': song.energy,
        'speechiness': song.speechiness,
        'acousticness': song.acousticness,
        'uri': song.uri,
    } for song in songs]

# Usage example:
# recommended_songs = song_recommender(your_input_tracks, db, mainbase_songs)

def gather_users():
    profiles_list = profiles.query.all()
    return profiles_list