import os
import sys

############################
# Import functions from src
sys.path.insert(0, "/src")
from spotipyDataCollection import artistCollection
############################

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

import pandas as pd
import numpy as np

################################################
# Flask Application:
################################################

app = Flask(__name__)

## Configure sqlalchemy:

# Will need to test to see if configuration should be after data is collected.

# Lets use flask_sqlalchemy. set a config parameter to SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Resources/artists.sqlite"
db = SQLAlchemy(app.config)

# Reflect artist_populated database into a model. Allow Base to access tables.
Base = automap_base()
Base.prepare(db.engine, reflect=True)

# Option 1. store all collected data into artist table... replace table with new data if exists.
artistTable = Base.classes.artist

# Could also append a tracks table with all songs ever collected, and sort by artist_id
	# This would allow for future charts across many different artists.
		# do track numbers have a part in song attributes?
		# is there a coorelation between danceability and popularity?

################################################
# Configure Routes:
################################################


# home route will render standard home_page:
@app.route("/")
def home():

	return render_template("home.html")


# display route will be seen as artist followed by actual artist name:
@app.route("/artist/<artist>")
def artistDisplay():

	return render_template("display.html")


# sqlite artist collection route will lead to artist_collection.py
@app.route("/api/artist/<artist>")
def artistDataCollection(artist):

	# run artist_collection function(s) with artist input
	return artistCollection(artist)


# Folowing routes pull data from sqlite for each attribute collected
@app.route("/api/artist/<artist>/<attr>")
def artistAttrToJson(artist,attr):

	## SQLALCHEMY CODE TO PULL EACH ATTRIBUTE FROM ARTIST'S TABLE



	# Data should be in the form of 2 columns[attr, attr_count]
		# ex: key_sig, mode

	# ScatterPlot data should be in form of [attr1, attr2]


	return jsonify(attrData)



# Run the application if file is called interactively.
if __name__ == "__main__":
	app.run()