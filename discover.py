import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import os
import sys
import pprint
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

from sklearn.ensemble import GradientBoostingClassifier



username = 'a72ywbvjxxomn3u942brdawuc'
cid = '0096a62e94574d778211481e97bb734a'
secret = '29715e3e2d624a97884160d3bdc3441c'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'user-library-read playlist-read-private'

token = util.prompt_for_user_token(username,scope,client_id='0096a62e94574d778211481e97bb734a',client_secret='29715e3e2d624a97884160d3bdc3441c',redirect_uri='https://example.com/callback/')

if token:
	sp = spotipy.Spotify(auth=token)
else:
	print ("Can't get token for", username)




playlist_id = "3m48a4IETZ8UKRsDl6XJQ2"

results = sp.user_playlist(username, playlist_id,
                                    fields='tracks,next,name')
tracks = results['tracks']

good_ids = [val['track']['id'] for val in tracks['items']]

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
