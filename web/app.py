from flask import Flask, render_template, request, jsonify, flash, url_for, \
    redirect
from config import BaseConfig
from raven.contrib.flask import Sentry
from werkzeug.exceptions import BadRequest
import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util

app = Flask(__name__)
app.config.from_object(BaseConfig)
sentry = Sentry(
    app,
    dsn=BaseConfig.SENTRY_DSN
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    credentials = oauth2.SpotifyClientCredentials(
        client_id=BaseConfig.SPOTIFY_CLIENT_ID,
        client_secret=BaseConfig.SPOTIFY_CLIENT_SECRET)

    token = credentials.get_access_token()
    sp = spotipy.Spotify(auth=token)

    output = []
    results = sp.search(q='weezer', limit=5)
    for i, t in enumerate(results['tracks']['items']):
        output.append({
            'i': i,
            'name': t['name']
        })
    return jsonify({'result': output})


@app.route('/test-authorize-spotify')
def test_authorize_spotify():
    scope = 'user-library-read'
    username = "rattlenhumn"
    credentials = oauth2.SpotifyClientCredentials(
        client_id=BaseConfig.SPOTIFY_CLIENT_ID,
        client_secret=BaseConfig.SPOTIFY_CLIENT_SECRET)

    token = util.prompt_for_user_token(
        username,
        scope,
        client_id=BaseConfig.SPOTIFY_CLIENT_ID,
        client_secret=BaseConfig.SPOTIFY_CLIENT_SECRET,
        redirect_uri=BaseConfig.SPOTIFY_REDIRECT_URL)

    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks()
        return jsonify({'result': results})
    else:
        return "Can't get token for user", username

# @app.route('/user/', methods=['GET'])
# @app.route('/user/<first_name>', methods=['GET'])
# def get_one_user(first_name=None):
#     user_db = client.test.user
#
#     if first_name is not None:
#         user = user_db.find_one({'first_name': first_name})
#         if user:
#             output = {
#                 'first_name': user['first_name'],
#                 'last_name': user['last_name']
#             }
#             return jsonify({'result': output})
#
#     return render_template('user.html', first_name=first_name)


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'bad request!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
