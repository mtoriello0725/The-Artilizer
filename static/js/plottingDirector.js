function boxplot(artistName) {

	var boxplotURL = "/api/artist/boxplot/"+artistName;

	d3.json(boxplotURL).then(function(response) {
		var boxplotData = response;

		// Data comes through perfectly. For now, use plotly for a boxplot! 

		var trace1 = {
			y: boxplotData.map(row => row.acousticness),
			type: "box"
		};

		var trace2 = {
			y: boxplotData.map(row => row.danceability),
			type: "box"
		}

		var data = [trace1, trace2];

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

		console.log("got this far!");
		Plotly.newplot("boxplot", data, layout);
	})

}