import os
import sys
############################
# Import functions from src
from src.spotipyMongoCollection import artistCollection
from config import *
############################
# Import spotipy
# import spotipy
# import spotipy.util as util
# import spotipy.oauth2 as oauth
############################
#Import PyMongo
import pymongo
############################
# Import Flask
from flask import Flask, jsonify, render_template, redirect, request
############################
# Import data processing packages.
import pandas as pd
import numpy as np

################################################
# Flask Application:
################################################

app = Flask(__name__)

# Could also append a tracks table with all songs ever collected, and sort by artist_id
	# This would allow for multiple users to use the application
		# do track numbers have a part in song attributes?
		# is there a coorelation between danceability and popularity?

################################################
# Configure Routes:
################################################


# home route will render standard home_page:
@app.route("/")
def homePage():

	return render_template("home.html")


# display route will be seen as artist followed by actual artist name:
@app.route("/artist/display", methods=["GET", "POST"])
def artistDisplay():

	artistCollected = request.args.get("artist_name")

	return render_template("display.html")

""" Do not need this function if /collect route works:
# sqlite artist collection route will lead to artist_collection.py
@app.route("/api/artist/<artistInput>")
def artistDataCollection(artistInput):

	# run artist_collection function(s) with artist input

	return jsonify(artistCollection(artistInput))
"""

@app.route("/collect", methods=["GET", "POST"])
def collect():
	if request.method == "POST":
		# Use the user input and run in the artistCollection function
		queriedArtist = request.form["artist-input"]
		artistCollected = artistCollection(queriedArtist)

		# If function succeeds, redirect to display page with artistCollected as the arg. 
		if artistCollected != "Failed":
			return redirect(f"/artist/display?artist_name={artistCollected}", code=302)
		else:
			return redirect(f"/#", code=302)

	return render_template("home.html")

# Folowing routes pull data from sqlite for each attribute collected
@app.route("/api/artist/boxplot/<artistInput>")
def artistAttrToJson(artistInput):

	## PYMONGO CODE TO PULL EACH ATTRIBUTE FROM ARTIST'S TABLE

	## Configure mongodb:
	conn = f"mongodb://{dbuser}:{dbpassword}@ds035014.mlab.com:35014/spotify_artists"
	mongoClient = pymongo.MongoClient(conn)
	db = mongoClient.spotify_artists

	# assign artistCollection to the desired artist!
	artistCollection = db[artistInput]

	# assign dictionary of column names to pull from collection
	attrDict = {
		"_id": False,
		"acousticness": True,
		"danceability": True,
		"energy": True,
		"instrumentalness": True,
		"liveness": True,
		"speechiness": True,
		"valence": True
		}

	boxplotData = []
	# iterate through collection and pull all records, but only specific columns
	for i in artistCollection.find({}, attrDict):
		boxplotData.append(i)

	return jsonify(boxplotData)



# Run the application if file is called interactively.
if __name__ == "__main__":
	app.run()