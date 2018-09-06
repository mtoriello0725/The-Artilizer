### Artilyzer

import os
import sys
import numpy as np
import pandas as pd
import matplotlib as plt
import seaborn as sns

import json
import spotipy
import spotipy.util as util
import webbrowser
from json.decoder import JSONDecodeError

username = sys.argv[1]

# Ask User for API credentials
#-------------------------------------------------------------
client_id = input('Please enter client_id from Spotify_Dev Page: ')
client_secret = input('Please enter client_secret from Spotify_Dev Page: ')
redirect_uri = input('Please enter redirect_uri you will use: ')

# Spotipy Permissions to access
#-------------------------------------------------------------
scope_list = ['user-read-currently-playing','user-read-playback-state',\
              'user-follow-read','user-library-read','user-top-read','user-read-recently-played']

# Throw all permissions from the list into a string for token function:
#-------------------------------------------------------------
scope = ' '.join(scope_list)

try: 
	token = util.prompt_for_user_token(username,scope=scope,\
		client_id=client_id,\
		client_secret=client_secret,\
		redirect_uri=redirect_uri)
except: 
	os.remove(f'.cache-{username}')
	token = util.prompt_for_user_token(username,scope=scope,\
		client_id=client_id,\
		client_secret=client_secret,\
		redirect_uri=redirect_uri)

# assign spotify object as sp
sp = spotipy.Spotify(auth=token)

# ------------------------------------------------------------------------------------
# Define Function here: 

def artilyzer(artist_id):

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















	

# -------------------------------------------------------------------------------------

user = sp.current_user()

displayName = user['display_name']
followers = user['followers']['total']

print()
print(f'Welcome to the Artilyzer {displayName}!')
print()
print('The Artilyzer is a data driven tool to determine how creative and unique your artist is.')
print()
print('This tool looks at BPMs, key_signatures, lyrics, album genres, and compares traits to similar artists')
print()

'''
--------------------------------------------------------------------------------
Run through a series of questions to analyze the correct artist: 
----------------------------------------------------------------------------------
'''

while True:

	print('Would you like to analyze the artist you are currently listening to?')

	current_choice = input('Please enter (Yes) or (No): ')

	if current_choice == "No":
		print()
		searchQuery = input('Okay, What artist would you like to analyze?: ')
		print()

		search_results = sp.search(\
			searchQuery,\
			limit=1,\
			offset=0,\
			type="artist"\
			)

		artist_proposed = search_results['artists']['items'][0]

	elif current_choice == "Yes":

		play_current = sp.currently_playing()
		artist_proposed = play_current['item']['artists'][0]

	else:
		print("Okay, Let's try this again!\n\n")
		continue

	confirm = input(f'Just to be sure you want to analyze {artist_proposed["name"]}, correct? (Yes): ')

	if confirm == 'Yes':

		# set function input to artist_id
		artist_id = artist_proposed['id']

		print(artilyzer(artist_id))
		print(f'Analysis should have appeared on your machine using {artist_id}')

	else:

		print("Okay, Let's try this again!\n\n")
		continue

	again = input('Would you like to analyze another artist? (Yes) or (No): ')

	if again == 'Yes':
		continue
	else: 
		break





			



