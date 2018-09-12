import numpy as np
import pandas as pd
import matplotlib as plt
import seaborn as sns

import json
import spotipy
import spotipy.util as util
import webbrowser
from json.decoder import JSONDecodeError

def artilyzer(artist_id, token):

	sp = spotipy.Spotify(auth=token)

	#For now use sp.artist_top_tracks
	top_tracks = sp.artist_top_tracks(artist_id)
	tracklist = []

	for song in top_tracks['tracks']:
		tracklist.append(song['id'])

	tracklist_features = sp.audio_features(tracklist)

	df_tracklist_features = pd.DataFrame(tracklist_features)

	# from here, need to set the index and drop unnecessary columns (see jupyter notebook)
	# Also should consider adding more columns based on 'id'
	# song popularity and song name is something missing, that can be added with 'id'
	# maybe find the max value for each category, inform user of song to check out.


	# Remember the goal here is to see if there is high variance, or std in the tracklist
	# This ultimately can determine if an artist explores, or sticks to a formula

	# for now use the top_tracks, but if this program runs quickly, explore entire discogrophy
	# discover similar artists as well, and compare analysis... do they vary from their competitors.




	return print(df_tracklist_features.head())















	