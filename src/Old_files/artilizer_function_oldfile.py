# Import all necessary packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError

def artilyzer(artist_id, token):

	sp = spotipy.Spotify(auth=token)

	#For now use sp.artist_top_tracks
	top_tracks = sp.artist_top_tracks(artist_id)
	tracklist = []
	track_name = []
	track_pop = []
	track_release = []

	for song in top_tracks['tracks']:
		tracklist.append(song['id'])
		track_name.append(song['name'])
		track_pop.append(song['popularity'])
		track_release.append(song['album']['release_date'])

	tracklist_features = sp.audio_features(tracklist)

	df_tracklist_features = pd.DataFrame(tracklist_features)
	df_tracklist_features['Name'] = track_name
	df_tracklist_features['Popularity'] = track_pop
	df_tracklist_features['Date'] = track_release

	df_tracklist_features.set_index('Name', inplace=True)
	df_tracklist_features.drop(columns=['analysis_url','track_href','type','uri'], inplace=True)

	# df_tracklist_features now holds usable information.
	# Plot all the data ranging from 0-1 to find average characteristics of top tracks.

	df_stats = df_tracklist_features.drop(columns=['id','key','mode','time_signature','Date', 'duration_ms', 'loudness','tempo','Popularity'])

	# Bar Graph
	sns.set(style='whitegrid')
	sns.set(font_scale=1.3) 

	fig = plt.figure(figsize=(15,5))
	ax = fig.add_axes([.1,.1,.8,.8])
	ax.set(ylim = (0,1))
	sns.barplot(x=df_stats.columns, y=df_stats.mean())
	
	ax.set_ylabel('Top Song Average', fontsize=14)
	ax.set_title('Average Song Characteristics for Artist')

	# Box plot
	sns.set(font_scale=1.3) 
	
	fig = plt.figure(figsize=(15,5))
	ax = fig.add_axes([.1,.1,.8,.8])
	ax.set(ylim = (0,1))
	sns.boxplot(x='variable', y='value', data=pd.melt(df_stats))
	
	ax.set_xlabel('')
	ax.set_ylabel('Top Song Average', fontsize=14)
	ax.set_title('Average Song Characteristics for Artist: Boxplot')
	plt.show()



	# from here, need to set the index and drop unnecessary columns (see jupyter notebook)
	# Also should consider adding more columns based on 'id'
	# song popularity and song name is something missing, that can be added with 'id'
	# maybe find the max value for each category, inform user of song to check out.


	# Remember the goal here is to see if there is high variance, or std in the tracklist
	# This ultimately can determine if an artist explores, or sticks to a formula

	# for now use the top_tracks, but if this program runs quickly, explore entire discogrophy
	# discover similar artists as well, and compare analysis... do they vary from their competitors.




	return print(df_tracklist_features.head())















	