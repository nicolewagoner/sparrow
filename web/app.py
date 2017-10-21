from flask import Flask, render_template, request, jsonify, flash, url_for, \
    redirect
from config import BaseConfig
from raven.contrib.flask import Sentry
from werkzeug.exceptions import BadRequest
import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
# from random import choice
# from string import ascii_uppercase

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


@app.route('/authorize-spotify', methods=['POST', 'GET'])
def authorize_spotify():
    # TODO implement location checks
    # location = request.form['location']

    # TODO implement state & show_dialog
    # https://github.com/plamere/spotipy/issues/211
    # stateKey = 'spotify_auth_state'
    # state = ''.join(choice(ascii_uppercase) for i in range(16))
    # res.cookie(stateKey, state)

    oauth = oauth2.SpotifyOAuth(
        client_id=BaseConfig.SPOTIFY_CLIENT_ID,
        client_secret=BaseConfig.SPOTIFY_CLIENT_SECRET,
        redirect_uri=BaseConfig.SPOTIFY_REDIRECT_URL,
        scope='user-library-read')

    return redirect(oauth.get_authorize_url())


@app.route('/events')
def get_all_events():
    error = request.args.get('error')
    if error:
        return error

    auth_code = request.args.get('code')
    if not auth_code:
        return "Something went wrong"

    oauth = oauth2.SpotifyOAuth(
        client_id=BaseConfig.SPOTIFY_CLIENT_ID,
        client_secret=BaseConfig.SPOTIFY_CLIENT_SECRET,
        redirect_uri=BaseConfig.SPOTIFY_REDIRECT_URL,
        scope='user-library-read')
    token_info = oauth.get_access_token(auth_code)
    if not token_info:
        return "Couldn't get access token"

    access_token = token_info['access_token']
    sp = spotipy.Spotify(auth=access_token)
    results = sp.current_user_followed_artists()
    return jsonify({'result': results})


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'bad request!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
