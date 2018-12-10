/*
function submitQuery(input_id) {
	//send input value to route of python script

	// Assign input variable to text in appropriate search bar
	var inputArtist = d3.select(input_id);

	// Pull artist name from search bar
	var artistValue = inputArtist.property("value");

	// Create route name to send to flask app. 
	var query_url = "/api/artist/"+artistValue;

	// Access route with artist name as the input. Return with "Success" or "Failed" response.
	d3.json(query_url).then(function(response) {
		console.log(response);

		// If response "success", send to plotting functions with artist as input.
		if (response == "Success") {
			window.location.replace("artist/display");
			return plotManager(artistValue);
		} else {
			return response;
		}
	});
}

// select the submit buttons
var submit_nav = d3.select('#submit_nav');
var submit_home = d3.select('#submit_home');

// when a name appears in either search bar, run submitQuery function.
submit_nav.on("click", function() {

	d3.event.preventDefault();
	submitQuery("#artist-input-nav");

});

submit_home.on("click", function() {

	d3.event.preventDefault();
	submitQuery("#artist-input-home");

});
*/