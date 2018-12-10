import os
import sys
############################
# Import functions from src
from src.spotipyDataCollection import artistCollection
# from config import *
############################
# Import spotipy
# import spotipy
# import spotipy.util as util
# import spotipy.oauth2 as oauth
############################
#Import SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
############################
# Import Flask
from flask import Flask, jsonify, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
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

	queriedArtist = request.args.get("artist_name")

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
		queriedArtist = request.form["artist-input"]
		artistCollection(queriedArtist)
		return redirect(f"/artist/display?artist_name={queriedArtist}", code=302)

	return render_template("home.html")

# Folowing routes pull data from sqlite for each attribute collected
@app.route("/api/artist/boxplot/<artistInput>")
def artistAttrToJson(artistInput):

	## SQLALCHEMY CODE TO PULL EACH ATTRIBUTE FROM ARTIST'S TABLE

	## Configure sqlalchemy:
	DATABASE = "/Resources/artists.sqlite"
	engine = create_engine(f"sqlite://{DATABASE}", echo=False)
	conn = engine.connect()

	# Pull data from sqlite connection.
	attr_list = "acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence"
	boxplot_df = pd.read_sql_query(f"SELECT {attr_list} FROM {artistInput}", con=conn)

	conn.close()

	# attrData = (data for js. Will need one for each attribute plotted.)

	# Data should be in the form of 2 columns[attr, attr_count]
		# ex: key_sig, mode

	# ScatterPlot data should be in form of [attr1, attr2]


	return jsonify(boxplot_df.to_json(orient="records"))



# Run the application if file is called interactively.
if __name__ == "__main__":
	app.run()