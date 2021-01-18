from flask import Flask, jsonify, make_response, request, render_template
from pprint import pprint
from json import loads
import threading
from time import sleep
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth, is_token_expired
import spotipy

q = ['bill']

app = Flask(__name__)

scope = "app-remote-control streaming user-read-playback-state user-modify-playback-state user-read-currently-playing"
auth_manager=SpotifyOAuth(scope=scope)

#auth = 'BQAHnyo5e0V5H9ATiXnsRbhNnze5iuL0wM1blOYHZdFOYV767HA2kctcfMUR4mh0o7Ez7VQOZfx5fj7ffdnXOLEIqmdPmK8WyOSeat3nEnrWWTjBY9zhqBxeIRp8H2IxApZQJ6umggGVV-ATRlcsE7tlzhlTv18'
#auth_manager = SpotifyClientCredentials()
#sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
#code = auth_manager.get_access_token(as_dict=False)

token_info = auth_manager.get_cached_token()
if not token_info:
    auth_url = auth_manager.get_authorize_url()
    resp = auth_manager.parse_response_code(input("Enter the url: "))
    token_info = auth_manager.get_access_token(resp)

token = token_info['access_token']
print(auth_manager.is_token_expired(token_info))

sp = spotipy.Spotify(auth=token, auth_manager=auth_manager)


def refresh():
    global token_info, sp
    
    token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    token = token_info['access_token']
    sp = spotipy.Spotify(auth=token, auth_manager=auth_manager)

@app.route('/')
def intro():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index():
    text = request.form['text']
    print("Song Request Received:", text)
    result = sp.search(text)
    #pprint(result['tracks']['items'][0])
    q.append(result['tracks']['items'][0]['external_urls']['spotify'])
    return 'Song \"' + text + '\" has been queued!'



if __name__ == '__main__':
    #app.run('127.0.0.1', 5000, True)
    t1 = threading.Thread(target = app.run, args=('127.0.0.1', 5000, False))
    t1.start()
    
    init = False
    
    while True: #main loop
        if not init:
            sleep(5)
        else:
            sleep(90)
            
        if (auth_manager.is_token_expired(token_info)):
            refresh()
        
        if q != []:
            init = True
            song = q.pop()
            try:
                sp.add_to_queue(song)
                print(song)
            except spotipy.exceptions.SpotifyException:
                print('Error, invalid request received. Please try entering your song again.')
        else:
            init = False

    
    
