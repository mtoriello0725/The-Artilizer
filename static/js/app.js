
// Use the window parameters to tell javascript what the queried artist was.
if (window.location.pathname == "/artist/display") {

	var url = new URL(window.location.href);
	searchArtist = url.searchParams.get("artist_name");
	console.log(searchArtist);

	var test = d3.select("#testing").append("p").text("Does this testing text appear on display page");
}