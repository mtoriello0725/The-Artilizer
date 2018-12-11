function boxplot(artistName) {

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
			title: "<b>Discography Attributes for "+artistName,
			titlefont: {
				size: 20
			},
			xaxis: {
				title: "Attributes"
			},
			yaxis: {
				title: "Scale"
			}
		};

		Plotly.newPlot("boxplot", data, layout);
	})

}