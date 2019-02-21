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

		// // Now using Highcharts:

		// var acousticnessData = Object.values(boxplotData.map(row => row.acousticness)).sort(function(a, b){return a - b});

		// Highcharts.chart("boxplot", {

		// 	chart: {
		// 		type: "boxplot"
		// 	},

		// 	title: {
		// 		text: "Highchart Boxplot"
		// 	},

		// 	legend: {
		// 		enabled: false
		// 	},

		// 	xAxis: {
		// 		categories: ['Acousticness', '2'],
		// 		title: {
		// 			text: "Musical Attribute"
		// 		}
		// 	},

		// 	yAxis: {
		// 		title: {
		// 			text: "Attribute Level"
		// 		}
		// 	},

		// 	series: [{
		// 		name: "Attribute",
		// 		data: [
		// 			acousticnessData,
  //           		[.5, .8, .6, .2, .3],
		// 			// Object.values(boxplotData.map(row => row.acousticness)),
		// 			// Object.values(boxplotData.map(row => row.danceability)),
		// 			// Object.values(boxplotData.map(row => row.energy)),
		// 			// Object.values(boxplotData.map(row => row.instrumentalness)),
		// 			// Object.values(boxplotData.map(row => row.liveness)),
		// 			// Object.values(boxplotData.map(row => row.speechiness)),
		// 			// Object.values(boxplotData.map(row => row.valence)),
		// 		],
		// 		tooltip: {
		// 			headerFormat: "<em>Attribute {point.key}</em><br/>"
		// 		}

		// 	}]

		// })


	});

}

function percentileChart(artistName) {

	var percentileURL = "/api/artist/attrcompare/"+artistName;

	d3.json(percentileURL).then(function(response) {

		console.log(response);

		console.log(response["acousticness"])

	})
}


function keyBarchart(artistName) {

	var keyCountURL = "/api/artist/keyBarchart/"+artistName;

	d3.json(keyCountURL).then(function(response) {

		keyCount = response;

		console.log(keyCount);

		var trace1 = {
			x: Object.keys(keyCount[0]),
			y: Object.values(keyCount[0]),
			name: "Major",
			type: "bar"
		};

		var trace2 = {
			x: Object.keys(keyCount[1]),
			y: Object.values(keyCount[1]),
			name: "Minor",
			type: "bar"
		};

		var data = [trace1, trace2]

		var layout = {
			barmode: "stack",
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