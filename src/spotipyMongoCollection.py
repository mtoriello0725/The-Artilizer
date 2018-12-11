import os
import json

import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth

from config import *

import numpy as np
import pandas as pd

import pymongo
"""
###################################################################

This function will collect all necessary attributes to an artist's discography and store into the artist table in mongodb.

It will be called once the user inputs an artist name in search. 

Function will run from the route("/api/artist/<artist>")

If the spotify search function does not find an artist? will need to relay message back to user.

If spotify token times out, should be seemless for user as this function will refresh token.

###################################################################
"""

def artistCollection(artist): 

	# Create Scope List:
	scope_list = ['user-read-currently-playing','user-read-playback-state',\
	              'user-follow-read','user-library-read','user-top-read','user-read-recently-played']

	# Throw all permissions from the list into a string for token function:
	scope = ' '.join(scope_list)

	# Create Spotipy token
	token = util.prompt_for_user_token(
		username=username,
		scope=scope,
	    client_id=client_id,
	    client_secret=client_secret,
	    redirect_uri=redirect_uri
	    )

	# Authorize spotipy object as sp
	sp = spotipy.Spotify(auth=token)

	# # create keyMap and modeMap
	# keyMap = {
	#     0:"C",
	#     1:"C#/Db",
	#     2:"D",
	#     3:"D#/Eb",
	#     4:"E",
	#     5:"F",
	#     6:"F#/Gb",
	#     7:"G",
	#     8:"G#/Ab",
	#     9:"A",
	#     10:"A#/Bb",
	#     11:"B",
	# }
	# modeMap = {
	#     0:"minor",
	#     1:"major",
	# }

	# query for artist
	searchResults = sp.search(
		q=artist,
		limit=1,
		offset=0,
		type="artist"
		)

	# Discover if the search was successful:
	if searchResults["artists"]["items"] == []:
		return "Failed"
	else:
		targetArtist = searchResults["artists"]["items"][0]

	# Extract Artist ID
	targetArtistID = targetArtist["id"]
	# Artist Name to be referenced later 
	targetArtistName = targetArtist["name"].replace(" ", "_")
	# Extract other parameters in search if needed (name,genres,images[0]["url"],popularity)

	# Extract all albums by targetArtist
	albums = sp.artist_albums(artist_id=targetArtistID, album_type="album")

	# Collect ids, names, and total tracks
	albumIDs = [album["id"] for album in albums["items"]]
	albumNames = [album["name"] for album in albums["items"]]
	albumTotalTracks = [album["total_tracks"] for album in albums["items"]]

	# Collect all tracks from each album. Tracks will be stored in lists per album
	# ex. 5 albums means tracksByAlbum will contain 5 lists.
	tracksByAlbum = [sp.album_tracks(albumID) for albumID in albumIDs]

	# Will need to extract IDs names, and track numbers for each list in tracksByAlbum
	trackIDs = []
	trackNames = []
	trackNumbers = []
	albumNamesPerTrack = []

	# APpend albumNames for each track:
	for i in range(0,len(tracksByAlbum)):
		for track in tracksByAlbum[i]["items"]:
			# append empty track lists. 
			trackIDs.append(track["id"])
			trackNames.append(track["name"])
			trackNumbers.append(track["track_number"])
			# Append album to the row according to the first forloop:
			albumNamesPerTrack.append(albumNames[i])

	# Use track IDs to find all audio features in the list
	trackFeatures = [sp.audio_features(trackIDs[i:i+50]) for i in range(0,len(trackIDs),50)]

	# Merge output lists of dictionaries within trackFeatures list
	allTrackFeatures = []
	for i in trackFeatures:
		allTrackFeatures = allTrackFeatures + i

	# append artist name to the list:
	for song in range(0,len(allTrackFeatures)):
		allTrackFeatures[song]["artist_name"] = targetArtistName
		allTrackFeatures[song]["track_name"] = trackNames[song]
		allTrackFeatures[song]["track_number"] = trackNumbers[song]
		allTrackFeatures[song]["album_name"] = albumNamesPerTrack[song]

	# Drop any unnecessary columns:


	# Map df_trackFeatures key and mode: (Will modify when needed.)
	# df_trackFeatures["key"] = df_trackFeatures["key"].map(keyMap)
	# df_trackFeatures["mode"] = df_trackFeatures["mode"].map(modeMap)


	# In artist_collection, append new artist to the table:
	# insert into mongoDB as individual collection:
	# if collection exists? replace
	try:
		# create the mongodb connection:
		conn = f"mongodb://{dbuser}:{dbpassword}@ds035014.mlab.com:35014/spotify_artists"
		mongoClient = pymongo.MongoClient(conn)
		db = mongoClient.spotify_artists

		# Check to see if collection exists, if so replace. Otherwise create.
		collectionList = db.list_collection_names()
		if targetArtistName in collectionList:
			# drop collection (for testing purposes)
			db[targetArtistName].drop()

		# upload new collection	
		artistCollection = db[targetArtistName]
		uploadAttr = artistCollection.insert_many(allTrackFeatures)

		return targetArtistName

	except:
		return "Failed"

