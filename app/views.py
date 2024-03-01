from app import app, sp_oauth, db, update_key_internal, database as d, spotify as s
from flask import redirect, url_for, session, request, render_template, jsonify

db.create_all()
d.clear_cache_playlists()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/logout')
def logout():
    session.pop('spotify_token', None)
    return redirect(url_for('index'))

@app.route('/authorized')
def authorized():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('landing'))

@app.route('/landing')
def landing():
    profile_info = s.gather_user_data()
    session['user_id'] = profile_info.get('user_id')
    print(profile_info)

    if profile_info:
        # Extracting individual pieces of data
        name = profile_info.get('name')
        email = profile_info.get('email')
        profile_image = profile_info.get('image_url')
        genres = profile_info.get('genres', [])  # Assuming genres is a list

        return render_template('landing.html', 
                               name=name,
                               email=email, 
                               profile_image=profile_image, 
                               top_genres=genres)

@app.route('/get_user_playlists')
def get_user_playlists():
    cached_playlists = d.get_playlists()
    if cached_playlists:
        print('Pulling playlists.')
        playlist_details = [
            {
                'name': playlist.name,
                'image_url': playlist.image_url,
                'total_tracks': playlist.num_tracks,
                'uri': playlist.uri
            } for playlist in cached_playlists
        ]
        return render_template('playlists.html', playlists=playlist_details)
    else:
        playlists = []
        next_url = 'me/playlists?limit=50'

        while next_url:
            response = s.get_spotify_data(next_url)
            if response == "Retry":
                continue
            if response == "Unauthorized":
                return redirect(url_for('index'))
            if isinstance(response, str) and response.startswith("Error"):
                error_message = response
                print(error_message)
                return jsonify({"error": error_message})

            if isinstance(response, dict):
                playlists_data = response.get('items', [])
                playlists.extend(playlists_data)
                next_url = response.get('next')
                if next_url:
                    next_url = next_url.replace('https://api.spotify.com/v1/', '')
            else:
                return jsonify({"error": "Unexpected response type"})

        playlist_details = []
        for playlist in playlists:
            image_url = playlist['images'][0]['url'] if playlist['images'] else 'default_image_url'  # Replace 'default_image_url' with a URL or a placeholder image
            detail = {
                'name': playlist['name'],
                'image_url': image_url,
                'total_tracks': playlist['tracks']['total'],
                'uri': playlist['uri']
            }
            playlist_details.append(detail)
        d.load_playlists(playlist_details)
        return render_template('playlists.html', playlists=playlist_details)


@app.route('/visualize_playlist/<playlist_uri>')
def visualize_playlist(playlist_uri):
    from . import visualizations as v
    tracks = s.get_playlist_tracks(playlist_uri)
    song_data = d.load_songs(tracks)
    recommended_tracks = d.song_recommender(song_data)
    plot_json = v.generate_plot_playlist(song_data, recommended_tracks)
    return render_template('visualization.html', plot_json=plot_json)

@app.route('/explore')
def explore():
    from . import visualizations as v
    users = d.gather_users()
    json = v.plot_profiles(users)
    return render_template('visualization.html', plot_json=json)

