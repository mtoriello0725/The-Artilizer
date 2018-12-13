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

## Configure mongodb:
conn = f"mongodb://{dbuser}:{dbpassword}@ds035014.mlab.com:35014/spotify_artists"
mongoClient = pymongo.MongoClient(conn)
db = mongoClient.spotify_artists

################################################
# Configure Routes:
################################################

# home route will render standard home page:
@app.route("/")
def homePage():

	return render_template("home.html")

# about route will render description about the app, and why it was created
@app.route("/about")
def aboutPage():

	return render_template("about.html")

# Contact page that has a link to the repo, as well as a card with my name, number, email, linkedin, github, and website url 
@app.route("/contact")
def contactPage():

	return render_template("contact.html")


# display route will be seen as artist followed by actual artist name:
@app.route("/artist/display", methods=["GET", "POST"])
def artistDisplay():

	artistCollected = request.args.get("artist_name")

	return render_template("display.html")

# Collect Artist information based on search tag (artist-input)
@app.route("/collect", methods=["GET", "POST"])
def collect():
	if request.method == "POST":
		# Use the user input and run in the artistCollection function
		queriedArtist = request.form["artist-input"]
		artistCollected = artistCollection(artist=queriedArtist, db=db)

		# If function succeeds, redirect to display page with artistCollected as the arg. 
		if artistCollected != "Failed":
			return redirect(f"/artist/display?artist_name={artistCollected}", code=302)
		else:
			return redirect(f"/#", code=302)

	return render_template("home.html")

# Folowing routes pull data from sqlite for each attribute collected
@app.route("/api/artist/boxplot/<artistInput>")
def artistAttrToJson(artistInput):

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


@app.route("/api/artist/keyBarchart/<artistInput>")
def artistKeyToJson(artistInput):

	# assign artistCollection to the desired artist!
	artistCollection = db[artistInput]

	attrDict = {
		"_id": False,
		"key": True
	}

	keyCount = {
	    "C": 0,
	    "C#/Db": 0,
	    "D": 0,
	    "D#/Eb": 0,
	    "E": 0,
	    "F": 0,
	    "F#/Gb": 0,
	    "G": 0,
	    "G#/Ab": 0,
	    "A": 0,
	    "A#/Bb": 0,
	    "B": 0,
	}
	# iterate through collection and pull all records, but only for above columns:
	for i in artistCollection.find({}, attrDict):
		keyCount[i["key"]]+=1

	return jsonify(keyCount)
	
@app.route("/api/artist/tempoHistogram/<artistInput>")
def artistTempoToJson(artistInput):

	# assign artistCollection to the desired artist!
	artistCollection = db[artistInput]

	attrDict = {
		"_id": False,
		"tempo": True
	}

	histogramData = []
	# iterate through collection and pull all records, but only for above columns:
	for i in artistCollection.find({}, attrDict):
		histogramData.append(i["tempo"])

	return jsonify(histogramData)
	
@app.route("/api/artist/modeBarchart/<artistInput>")
def artistModeToJson(artistInput):

	# assign artistCollection to the desired artist!
	artistCollection = db[artistInput]

	attrDict = {
		"_id": False,
		"mode": True
	}

	modeCount = {
	    "Minor": 0,
	    "Major": 0,
	}

	# iterate through collection and pull all records, but only for above columns:
	for i in artistCollection.find({}, attrDict):
		modeCount[i["mode"]]+=1

	return jsonify(modeCount)
	
@app.route("/api/artist/durationHistogram/<artistInput>")
def artistDurationToJson(artistInput):

	# assign artistCollection to the desired artist!
	artistCollection = db[artistInput]

	attrDict = {
		"_id": False,
		"duration_ms": True
	}
# Run the applicatio
	histogramData = []
	# iterate through collection and pull all records, but only for above columns:
	for i in artistCollection.find({}, attrDict):
		histogramData.append(i["duration_ms"])

	histogramData = [i/60000 for i in histogramData]

	return jsonify(histogramData)


# if file is called interactively.
if __name__ == "__main__":
	app.run()