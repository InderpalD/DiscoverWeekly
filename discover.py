import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import config

import os
import sys
import pprint
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

from sklearn.ensemble import GradientBoostingClassifier


if __name__ == '__main__':


    # Login to my spotify account
    client_credentials_manager = SpotifyClientCredentials(client_id=config.client_id, client_secret=config.secret) 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    scope = 'user-library-read playlist-read-private'

    token = util.prompt_for_user_token(
        config.username, scope, client_id=config.client_id, client_secret=config.secret, redirect_uri='https://example.com/callback/')
    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print ("Can't get token for", config.username)


    good_playlist = sp.user_playlist(config.username, '3m48a4IETZ8UKRsDl6XJQ2')
    bad_playlist = sp.user_playlist(config.username, '1DG9P38IBmdgblrHms9pRx')


    good_tracks = good_playlist["tracks"]
    good_songs = good_tracks["items"] 
    while good_tracks['next']:
        good_tracks = sp.next(good_tracks)
        for item in good_tracks["items"]:
            good_songs.append(item)
    good_ids = [] 
    print(len(good_songs))
    for i in range(len(good_songs)):
        good_ids.append(good_songs[i]['track']['id'])

    bad_tracks = bad_playlist["tracks"]
    bad_songs = bad_tracks["items"] 
    while bad_tracks['next']:
        bad_tracks = sp.next(bad_tracks)
        for item in bad_tracks["items"]:
            bad_songs.append(item)
    bad_ids = [] 
    print(len(bad_songs))
    for i in range(len(bad_songs)):
        bad_ids.append(bad_songs[i]['track']['id'])
    
    


    '''
    playlist_id = "3m48a4IETZ8UKRsDl6XJQ2"
    #results = sp.user_playlist(config.username, playlist_id,fields='tracks,next,name')
    results = sp.user_playlist(config.username, playlist_id)
    tracks = results['tracks']
    good_ids = []
    for val in tracks['items']:
        good_ids.append(val['track']['id'])
    print(good_ids[0])

    '''


    '''

    
    # Extract features (50 songs at a time is all we are allowed to do)
    features = []
    for i in range(0,len(good_ids),50):
        audio_features = sp.audio_features(good_ids[i:i+50])
        for track in audio_features:
            features.append(track)
            features[-1]['target'] = 1


    
    trainingData = pd.DataFrame(features)
    train, test = train_test_split(trainingData, test_size = 0.15)


    features = ["danceability", "loudness", "valence", "energy", "instrumentalness", "acousticness", "key", "speechiness", "duration_ms"]

    x_train = train[features]
    y_train = train["target"]
    x_test = test[features]
    y_test = test["target"]

    c = DecisionTreeClassifier(min_samples_split=100)
    dt = c.fit(x_train, y_train)
    y_pred = c.predict(x_test)
    score = accuracy_score(y_test, y_pred) * 100

    print(score)
    '''

