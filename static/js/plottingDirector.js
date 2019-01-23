function topTracks(artistName) {

	var displayName = artistName.replace(/_/g, " ");

	var topTracksURL = "/api/artist/topTracks/"+artistName;

	d3.json(topTracksURL).then(function(response) {
		var artistTracks = response["tracks"];

		var ul = d3.select(".top-tracks");

		ul.selectAll("li")
			.data(artistTracks)
			.enter()
			.append("li")
			.attr("class", "list-group-item")
			.html(String);

	})
}

function albumArtwork(artistName) {

	var displayName = artistName.replace(/_/g, " ");

	var albumArtworkURL = "/api/artist/albumArtwork/"+artistName;

	d3.json(albumArtworkURL).then(function(response) {
		var artwork  = response["artwork"];

		var album_list = d3.select(".thumbnail-section");

		album_list.selectAll("a")
			.data(artwork, function(d) { return d; })
			.enter()
			.append("a")
			.attr("class", "col-lg-3 thumbnail")
			.attr("href", function(d) { return d; })
			.append("img")
			.attr("src", function(d) { return d; });
	})
}

function boxplot(artistName) {

	var displayName = artistName.replace(/_/g, " ");

	var boxplotURL = "/api/artist/boxplot/"+artistName;

	d3.json(boxplotURL).then(function(response) {
		var boxplotData = response;

		// Data comes through perfectly. For now, use plotly for a boxplot! 

		var acousticness = {
			y: boxplotData.map(row => row.acousticness),
			type: "box",
			name: "acousticness"
		};

		var danceability = {
			y: boxplotData.map(row => row.danceability),
			type: "box",
			name: "danceability"
		};

		var energy = {
			y: boxplotData.map(row => row.energy),
			type: "box",
			name: "energy"
		};

		var instrumentalness = {
			y: boxplotData.map(row => row.instrumentalness),
			type: "box",
			name: "instrumentalness"
		};

		var liveness = {
			y: boxplotData.map(row => row.liveness),
			type: "box",
			name: "liveness"
		};

		var speechiness = {
			y: boxplotData.map(row => row.speechiness),
			type: "box",
			name: "speechiness"
		};

		var valence = {
			y: boxplotData.map(row => row.valence),
			type: "box",
			name: "valence"
		};	

		var data = [acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence];

		var layout = {
			title: "<b>Discography Attributes for "+displayName,
			titlefont: {
				size: 20
			},
			xaxis: {
				title: "Attributes"
			},
			yaxis: {
				title: "Scale"
			},
			width: 700,
			height: 950
		};

		Plotly.newPlot("boxplot", data, layout);
	});

}

function keyBarchart(artistName) {

	var keyCountURL = "/api/artist/keyBarchart/"+artistName;

	d3.json(keyCountURL).then(function(response) {

		keyCount = response;

		var data = [{
			x: Object.keys(keyCount),
			y: Object.values(keyCount),
			type: "bar"
		}];

		var layout = {
			title: "Key Signature",
			font: {
				family: "Raleway, sans-serif"
			},
			showlegend: false,
			xaxis: {
				tickangle: -45
			},
			yaxis: {
				zeroline: false,
				gridwidth: 2
			},
			bargap: 0.05
		};

		Plotly.newPlot("keyplot", data, layout);

	});

}

function tempoHistogram(artistName) {

	var tempoURL = "/api/artist/tempoHistogram/"+artistName;

	d3.json(tempoURL).then(function(response) {

		tempoList = response;

		data = [{
			x: tempoList,
			type: "histogram",
		}];

		layout = {
			title: "Tempo Histogram",
			bargap: 0.05,
		}

		Plotly.newPlot("tempoplot", data, layout);
	})
} 

function modeBarchart(artistName) {

	var modeCountURL = "/api/artist/modeBarchart/"+artistName;

	d3.json(modeCountURL).then(function(response) {

		modeCount = response;

		var data = [{
			x: Object.keys(modeCount),
			y: Object.values(modeCount),
			type: "bar"
		}];

		var layout = {
			title: "Mode",
			font: {
				family: "Raleway, sans-serif"
			},
			showlegend: false,
			xaxis: {
				tickangle: -45
			},
			yaxis: {
				zeroline: false,
				gridwidth: 2
			},
			bargap: 0.05
		};

		Plotly.newPlot("modeplot", data, layout);

	});

}

function durationHistogram(artistName) {

	var durationURL = "/api/artist/durationHistogram/"+artistName;

	d3.json(durationURL).then(function(response) {

		durationList = response;

		data = [{
			x: durationList,
			type: "histogram",
		}];

		layout = {
			title: "Duration Histogram in Minutes",
			bargap: 0.05
		}

		Plotly.newPlot("durationplot", data, layout);
	})
} 