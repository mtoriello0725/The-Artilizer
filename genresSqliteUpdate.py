import os
import sys
import time
import spotipy
import spotipy.util as util

from config import *
import pandas as pd

from sqlalchemy import create_engine

# run sqlite update with username
username = sys.argv[1]

# Create sqlite connection to genres.sqlite
engine = create_engine("sqlite:///Resources/genres.sqlite", echo=False)
conn = engine.connect()

# import scopelist (will condense later)
scope_list = ['user-read-currently-playing','user-read-playback-state',\
              'user-follow-read','user-library-read','user-top-read','user-read-recently-played']

scope = ' '.join(scope_list)

# Create Spotipy connection:
token = util.prompt_for_user_token(username,scope=scope,\
    client_id=client_id,\
    client_secret=client_secret,\
    redirect_uri=redirect_uri)

# define spotipy instance as sp
sp = spotipy.Spotify(auth=token)

# Obtain list of genres allowed in recommendations function:
# should be 126 genres in this list (may be too many calls for one function)

genres = sp.recommendation_genre_seeds()
genres = genres["genres"]

# create keyMap and modeMap
keyMap = {
    0:"C",
    1:"C#/Db",
    2:"D",
    3:"D#/Eb",
    4:"E",
    5:"F",
    6:"F#/Gb",
    7:"G",
    8:"G#/Ab",
    9:"A",
    10:"A#/Bb",
    11:"B",
}
modeMap = {
    0:"minor",
    1:"major",
}

# START A FUNCTION THAT UPDATES GENRE DATABASE: will need to import time to run function slowly

def uploadGenre(genre):
	# run find recommended tracks for each genre
	recommendedTracks = sp.recommendations(seed_genres=[genre], limit=100)

	# Create lists for ids, names, popularity and artists
	genreTrackIDs = [track["id"] for track in recommendedTracks["tracks"]]
	genreTrackNames = [track["name"] for track in recommendedTracks["tracks"]]
	genreTrackPop = [track["popularity"] for track in recommendedTracks["tracks"]]
	genreTrackArtist = [track["artists"][0]["name"] for track in recommendedTracks["tracks"]]

	# find audio_features for each track. Since the max is 50 songs, must split into 2 lists
	trackFeatures = [sp.audio_features(genreTrackIDs[i:i+50]) for i in range(0,len(genreTrackIDs),50)]

	# merge output lists of dictionaries within trackFeatures list
	allTrackFeatures = []
	for i in trackFeatures:
		allTrackFeatures = allTrackFeatures + i

   	# Create a Dataframe for the genre
	df_genreFeatures = pd.DataFrame(allTrackFeatures)
	df_genreFeatures['popularity'] = genreTrackPop
	df_genreFeatures['name'] = genreTrackNames
	df_genreFeatures['artist'] = genreTrackArtist
	df_genreFeatures.drop(columns=['analysis_url','type','uri'], inplace=True)

	# Map the key and mode columns
	df_genreFeatures["key"] = df_genreFeatures["key"].map(keyMap)
	df_genreFeatures["mode"] = df_genreFeatures["mode"].map(modeMap)

	# Exporet dataframe to sqlite:
	# Note: use "replace" for now, but eventually will change to "append"
	df_genreFeatures.to_sql(name=genre,con=conn, if_exists="replace")

	# Need to incorporate a time feature: will exceed call limit without buffer
	# print "genre" sucessfully uploaded and waiting for next iteration: Wait 30 seconds in between each genre
	print(f"Genre {genre} was successfully uploaded to sqlite:")


# Try function, if error occurs, except will print error and put function to sleep for 5 minutes
# if the next iteration fails, sleep for 10 minutes: double until function runs again!

for g in genres:
	sleepMinutes = 5
	while True:
		try:
			uploadGenre(g)
			print()
			time.sleep(.1)

		except spotipy.client.SpotifyException:
			# We'll need to refresh the token!
			print("expired")


			continue
		break










