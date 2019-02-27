function topTracks(artistName) {

	var displayName = artistName.replace(/_/g, " ");

	var topTracksURL = "/api/artist/topTracks/"+artistName;

	$.getJSON(topTracksURL).done(function(response) {

		// All this needs to change when topTracks API changes
		var artistTracks = response["tracks"].map(row => row.name);

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

	$.getJSON(albumArtworkURL).done(function(response) {
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

	$.getJSON(boxplotURL).done(function(response) {
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

function percentileChart(artistName) {

	var percentileURL = "/api/artist/attrcompare/"+artistName;

	$.getJSON(percentileURL).done(function(response) {

		// Highcharts display! 
		// FOr now, just plot acousticness. Later will try to make it dynamic
		var attrChart = Highcharts.chart("percentile", {

			title: {
				text: "Acousticness"
			},

			xAxis: {
				type: "year"
			},

			yAxis: {
				title: {
					text: "Acousticness"
				},
				min: 0,
				max: 1
			},

			tooltip: {
				crosshairs: true,
				shared: true
			},

			legend: {

			},

			series: [{
				name: "Median Acousticness",
				data: response["acousticness"].map(row => [row.year, row.percentile_50]),
				zIndex: 1,
				marker: {
					fillColor: "white",
					lineWidth: 2,
					lineColor: Highcharts.getOptions().colors[0]
				}
			}, {
				name: "Range",
				data: response["acousticness"].map(row => [row.year, row.percentile_25, row.percentile_75]),
				type: "arearange",
				lineWidth: 0,
				linkedTo: ":previous",
				color: Highcharts.getOptions().colors[0],
				fillOpacity: 0.3,
				zIndex: 0,
				marker: {
					enabled: false
				}

			}]
		});

		$("#acousticness").click(function() {
			attrChart.setTitle({text: "Acousticness"}),
			attrChart.yAxis[0].setTitle({text: "Acousticness"}),
			attrChart.series[0].setName("Median Acousticness"),
			attrChart.series[0].setData(response["acousticness"].map(row => [row.year, row.percentile_50])),
			attrChart.series[1].setData(response["acousticness"].map(row => [row.year, row.percentile_25, row.percentile_75]))
		});

		$("#danceability").click(function() {
			attrChart.setTitle({text: "Danceability"}),
			attrChart.yAxis[0].setTitle({text: "Danceability"}),
			attrChart.series[0].setName("Median Danceability"),
			attrChart.series[0].setData(response["danceability"].map(row => [row.year, row.percentile_50])),
			attrChart.series[1].setData(response["danceability"].map(row => [row.year, row.percentile_25, row.percentile_75]))
		});

		$("#valence").click(function() {
			attrChart.setTitle({text: "Valence"}),
			attrChart.yAxis[0].setTitle({text: "Valence"}),
			attrChart.series[0].setName("Median Valence"),
			attrChart.series[0].setData(response["valence"].map(row => [row.year, row.percentile_50])),
			attrChart.series[1].setData(response["valence"].map(row => [row.year, row.percentile_25, row.percentile_75]))
		});		

	})
}


function keyBarchart(artistName) {

	var keyCountURL = "/api/artist/keyBarchart/"+artistName;

	$.getJSON(keyCountURL).done(function(response) {

		keyCount = response;

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

	$.getJSON(tempoURL).done(function(response) {

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

	$.getJSON(modeCountURL).done(function(response) {

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

	$.getJSON(durationURL).done(function(response) {

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