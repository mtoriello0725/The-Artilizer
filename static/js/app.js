/* 
This file will trigger all of the plotting functions and return
outputs to the proper html tags on the display page. Will need to make calls for:

- Mean values of each attribute

- all album names (possibly album images) to visualize attributes by album

- attributes by album (album names above will be trigger for album charts)

- top popular songs 

*/

// Use the window parameters to tell javascript what the queried artist was.
if (window.location.pathname == "/artist/display") {

	var url = new URL(window.location.href);
	searchArtist = url.searchParams.get("artist_name");
	console.log(searchArtist);

	// show the boxplot:
	boxplot(searchArtist);
	// show other bar charts:
	keyBarchart(searchArtist);
}