import os
import json

import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth

from config import *

import numpy as np
import pandas as pd

###################################################################
""" 
This function will collect all necessary attributes to an artist's discography and store into the artist table in sqlite.

It will be called once the user inputs an artist name in search. 

Function will run from the route("/api/artist/<artist>")

If the spotify search function does not find an artist? will need to relay message back to user.

If spotify token times out, should be seemless for user as this function will refresh token.

"""
###################################################################

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

	# query for artist
	searchResults = sp.search(
		q=artist,
		limit=1,
		offset=0,
		type="artist"
		)

	# Discover if the search was successful:
	if searchResults["artists"]["items"] == []:
		return "Artist Not Found"
	else:
		targetArtist = searchResults["artists"]["items"][0]

	# Extract Artist ID
	targetArtistID = targetArtist["id"]
	# Extract other parameters in search if needed (name,genres,images[0]["url"],popularity)

	# Extract all albums by targetArtist
	albums = sp.artist_albums(artist_id=targetArtistID, album_type="album")

	# Collect ids, names, and total tracks
	albumIDs = [album["id"] for album in albums["items"]]
	albumNames = [album["name"] for album in albums["items"]]
	albumTotalTracks = [album["total_tracks"] for album in albums["items"]]

	# Collect all tracks from each album. Tracks will be stored in lists per album
	# ex. 5 albums means albumTracks will contain 5 lists.
	albumTracks = [sp.album_tracks(albumID) for albumID in albumIDs]

	# Will need to extract IDs names, and track numbers for each list in albumTracks
	trackIDs = []
	trackNames = []
	trackNumbers = []

	for albumOfTracks in albumTracks:
		for track in albumOfTracks:
			# append empty track lists. 
			trackIDs.append(track["id"])
			trackNames.append(track["name"])
			trackNumbers.append(track["track_number"])






