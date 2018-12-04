// query_artist_nav : input field for search in nav bar
// query_artist_home : input field for search on home page

// submit_nav
// submit_home

function submitQuery(input_id) {
	/* send input value to route of python script */

	var inputArtist = d3.select(input_id);

	var artistValue = inputArtist.property("value");

	console.log(artistValue);

	var query_url = "/api/artist/"+artistValue;

	d3.json(query_url).then(function(response) {
		console.log(response);
	});

	// If response says successful, begin plotting functions.

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