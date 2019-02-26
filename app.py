import os
import sys
import json
############################
# Import functions from src
from src.spotipyMongoCollection import artistCollection
from config import *
############################
#Import PyMongo
import pymongo
############################
# Import Flask
from flask import Flask, jsonify, render_template, redirect, request
############################
# Import data processing packages
import numpy as np
import pandas as pd

################################################
# Flask Application:
################################################

app = Flask(__name__)

## Configure MongoDB Connection:
try: 
	conn = os.getenv("MONGODB_URI")
	mongoClient = pymongo.MongoClient(conn)
	db = mongoClient.spotify_artists
except:
	conn = f"mongodb://{dbuser}:{dbpassword}@ds035014.mlab.com:35014/spotify_artists"
	mongoClient = pymongo.MongoClient(conn)
	db = mongoClient.spotify_artists

################################################
# Configure Routes:
################################################

##### home route will render standard home page:
@app.route("/")
def homePage():

	return render_template("home.html")

##### about route will render description about the app, and why it was created
@app.route("/about")
def aboutPage():

	return render_template("about.html")

##### Contact page that has a link to the repo, as well as a card with my name, number, email, linkedin, github, and website url 
@app.route("/contact")
def contactPage():

	return render_template("contact.html")

##### display route will be seen as artist followed by actual artist name:
@app.route("/artist/display", methods=["GET", "POST"])
def artistDisplay():

	artistCollected = request.args.get("artist_name")

	return render_template("display.html", artistCollected=artistCollected)

##### Collect Artist information based on search tag (artist-input)
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

##### Collect Top Tracks for selected artist
@app.route("/api/artist/topTracks/<artistInput>")
def artistTopTracks(artistInput):

	topTracksCollection = db["topTracks"]

	artistQuery = { "artist":artistInput }

	filterDict = {
		"_id":False
	}

	topTracksData = topTracksCollection.find_one(artistQuery,filterDict)

	return jsonify(topTracksData)

##### Collect album artwork for selected artist
@app.route("/api/artist/albumArtwork/<artistInput>")
def artistAlbumArtwork(artistInput):

	albumArtworkCollection = db["albumArtwork"]

	artistQuery = { "artist":artistInput }

	filterDict = {
		"_id":False
	}

	albumArtworkData = albumArtworkCollection.find_one(artistQuery, filterDict)

	return jsonify(albumArtworkData)

##### Create dataset to process avg attributes plot.
@app.route("/api/artist/attrcompare/<artistInput>")
def artistAttrToJson2(artistInput):

	""" Notes for new graph:
	Will need to import pandas

	step 1: Pull all necessary columns from MongoDB
		- acousticness, danceability, valence, release_date, popularity(when available)
	step 2: Convert Dataset to Pandas Dataframe
	step 3: Groupby album and calculate {Q1, median, Q3}
	step 4: Create new Dataframe for each calculation
	step 5: Combine results into one json collection

	Extra:
	step 6: Add top tracks as a scatter plot... Will probably use the topTracks API call above.
	"""

	# Function used to calculate percentile
	def percentile(n):
	    def percentile_(x):
	        return np.percentile(x, n)
	    percentile_.__name__ = 'percentile_%s' % n
	    return percentile_

		# Step 1:
	artistCollection = db[artistInput]

	attrDict = {
		"_id": False,
		"acousticness": True,
		"danceability": True,
		"valence": True,
		"album_name": True,
		"album_release_date": True
	}

	attrData = []

	for i in artistCollection.find({}, attrDict):
		attrData.append(i)

	# Step 2: attrData is now 5 columns
	attrDF = pd.DataFrame(attrData)

	attrDF["year"] = pd.to_datetime(attrDF["album_release_date"], infer_datetime_format=True).map(lambda x: x.year)

	# Step 3:
	album_groupby = attrDF.groupby(["year"])

	# Step 4 & Step 5:
	# attrPercentilesDF = album_groupby.agg([percentile(25), percentile(50), percentile(75)])

	attr_json = {
		"acousticness": json.loads(album_groupby["acousticness"].agg([percentile(25), percentile(50), percentile(75)]).reset_index().to_json(orient="records")),
		"danceability": json.loads(album_groupby["danceability"].agg([percentile(25), percentile(50), percentile(75)]).reset_index().to_json(orient="records")),
		"valence": json.loads(album_groupby["valence"].agg([percentile(25), percentile(50), percentile(75)]).reset_index().to_json(orient="records")),
	}

	return jsonify(attr_json)

##### Collect attributes for boxplot... TO be decommissioned
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

##### Create Major and Minor Keycount for stacked barchart
@app.route("/api/artist/keyBarchart/<artistInput>")
def artistKeyToJson(artistInput):

	# assign artistCollection to the desired artist!
	artistCollection = db[artistInput]

	attrDict = {
		"_id": False,
		"key": True,
		"mode": True
	}

	majorKeyMap = {
	    0:"C/Am",
	    1:"Db/Bbm",
	    2:"D/Bm",
	    3:"Eb/Cm",
	    4:"E/Dbm",
	    5:"F/Dm",
	    6:"Gb/Ebm",
	    7:"G/Em",
	    8:"Ab/Fm",
	    9:"A/Gbm",
	    10:"Bb/Gm",
	    11:"B/Abm",
	}

	minorKeyMap = {
	    0:"Eb/Cm",
	    1:"E/Dbm",
	    2:"F/Dm",
	    3:"Gb/Ebm",
	    4:"G/Em",
	    5:"Ab/Fm",
	    6:"A/Gbm",
	    7:"Bb/Gm",
	    8:"B/Abm",
	    9:"C/Am",
	    10:"Db/Bbm",
	    11:"D/Bm",    
	}	

	majorKeyCount = {
	    "C/Am": 0,
	    "Db/Bbm": 0,
	    "D/Bm": 0,
	    "Eb/Cm": 0,
	    "E/Dbm": 0,
	    "F/Dm": 0,
	    "Gb/Ebm": 0,
	    "G/Em": 0,
	    "Ab/Fm": 0,
	    "A/Gbm": 0,
	    "Bb/Gm": 0,
	    "B/Abm": 0,
	}

	minorKeyCount = {
	    "C/Am": 0,
	    "Db/Bbm": 0,
	    "D/Bm": 0,
	    "Eb/Cm": 0,
	    "E/Dbm": 0,
	    "F/Dm": 0,
	    "Gb/Ebm": 0,
	    "G/Em": 0,
	    "Ab/Fm": 0,
	    "A/Gbm": 0,
	    "Bb/Gm": 0,
	    "B/Abm": 0,
	}
	# iterate through collection and pull all records, but only for above columns:
	for i in artistCollection.find({}, attrDict):
		# If statements to seperate major and minor modes.
		if i["mode"] == "Major":
			majorKeyCount[majorKeyMap[i["key"]]]+=1
		elif i["mode"] == "Minor":
			minorKeyCount[minorKeyMap[i["key"]]]+=1
		else:
			continue

	return jsonify([majorKeyCount,minorKeyCount])

##### Tempo Histogram... TO be modified	
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

##### Removed Mode Bar Chart... Now Incorporated in KeyChart

##### Duration Histogram... TO be modified
@app.route("/api/artist/durationHistogram/<artistInput>")
def artistDurationToJson(artistInput):

	# assign artistCollection to the desired artist!
	artistCollection = db[artistInput]

	attrDict = {
		"_id": False,
		"duration_ms": True
	}

	histogramData = []
	# iterate through collection and pull all records, but only for above columns:
	for i in artistCollection.find({}, attrDict):
		histogramData.append(i["duration_ms"])

	histogramData = [i/60000 for i in histogramData]

	return jsonify(histogramData)

##### Run the Application if file is called interactively.
if __name__ == "__main__":
	app.run(debug=False)