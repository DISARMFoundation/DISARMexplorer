
// Code that creates the framework grid visualisations seen on the front page, in the
// techniques and counters pages etc. 
//
// SJ Terp, 2021


function wrap(text, width) {
	// "wraps" a line of text by splitting it across several lines
  text.each(function() {
    var text = d3.select(this),
        words = text.text().split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 0,
        lineHeight = 1.1, // ems
        y = text.attr("y"),
        dy = parseFloat(text.attr("dy")),
        tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em")
    while (word = words.pop()) {
      line.push(word)
      tspan.text(line.join(" "))
      if (tspan.node().getComputedTextLength() > width) {
        line.pop()
        tspan.text(line.join(" "))
        line = [word]
        tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", `${++lineNumber * lineHeight + dy}em`).text(word)
      }
    }
  })
}


function populatedata(object_grid, object_names, numrows, numcols, topcolor, boxwidth, boxheight, boxoncolor, boxoffcolor) {

  // Creates the javascript object "data" that's used by the rest of the code

	var data = new Array();
	var xpos = 1; //starting xpos and ypos at 1 so grid edges are visible
	var ypos = 1;
	var boxstate = 0;
	var maxlen = 16;

	// set position, width/height/text/number of clicks per box
	for (var row = 0; row < numrows; row++) {
		for (var col = 0; col < numcols; col++) {
			var disarmid = object_grid[row][col];
			var disarmname = disarmid + ": " + object_names[disarmid];
			var labellength = disarmname.length;

			if (labellength < maxlen)
			{
				var disarmname1 = disarmname;
				var disarmname2 = '';
				var disarmname3 = '';
				var disarmname4 = '';
			}
			else if (labellength < 2*maxlen)
			{
				var disarmname1 = disarmname.substr(1, maxlen);
				var disarmname2 = disarmname.substr(maxlen+1);
				var disarmname3 = '';
				var disarmname4 = '';
			}
			else if (labellength < 3*maxlen)
			{
				var disarmname1 = disarmname.substr(1, maxlen);
				var disarmname2 = disarmname.substr(maxlen+1, maxlen);
				var disarmname3 = disarmname.substr(2*maxlen+1);
				var disarmname4 = '';				
			}
			else
			{
				var disarmname1 = disarmname.substr(1, maxlen);
				var disarmname2 = disarmname.substr(maxlen+1, maxlen);
				var disarmname3 = disarmname.substr(2*maxlen+1, maxlen);
				var disarmname4 = disarmname.substr(3*maxlen+1, Math.min(maxlen, labellength-3*maxlen));			
			}

			var color = (row == 0) ? topcolor : '#D0D3D4';
            if (disarmid != '') {
				data.push({
					x: xpos,
					y: ypos,
					width: boxwidth,
					height: boxheight,
					disarmid: disarmid,
					disarmname: disarmname,
					disarmname1: disarmname1,
					disarmname2: disarmname2,
					disarmname3: disarmname3,
					disarmname4: disarmname4,
					oncolor: boxoncolor,
					offcolor: (row == 0) ? topcolor : boxoffcolor,
					state: boxstate
				})
		  }
			xpos += boxwidth;
		}
		xpos = 1;
		ypos += boxheight;	
	}

	return data

}



function fillHtmlTable(params) {
	// Creates the table with clickable text 
	// used in textgrid

	// grab dataset from input parameters
	var grid_div = params[0]; 
	var topcolor = params[1];
	var object_grid = params[2]; 
	var object_names = params[3]; 
	var object_urls = params[4]; 
	var tableheading = params[5];
	// console.log(object_names);

	var numrows = object_grid.length;
	var numcols = object_grid[0].length;

	var boxwidth = 75;
	var boxheight = 50;
	var boxoffcolor = '#D0D3D4';
	var boxoncolor = "#50C878";
	var boxstates = {};
	for (var key in object_names){
		boxstates[key] = 0;
	}
	

	// grab dataset
	var data = new Array();
	data = populatedata(object_grid, object_names, numrows, numcols, topcolor, boxwidth, boxheight, boxoncolor, boxoffcolor);
  // console.log(data)

  var table = d3.select(grid_div).append('table'),
		thead = table.append('thead'),
		tbody = table.append('tbody');
  var columns = object_grid[0];

  var caption = thead.append("tr").append("td").attr("colspan", columns.length);
  caption.html("<b>" + tableheading + "</b>")
    .style('background-color', topcolor)
    .style("font-size", "20px");

  thead.append('tr')
    .selectAll('td')
    .data(columns).enter()
    .append('td')
    .html(function (column) { 
    	// return column + ": " + object_names[column]; 
  		return "<a href=" + object_urls[column] + ' target="_blank" rel="noopener noreferrer">' + column + ": " + object_names[column] + "</a>";
    });

		// create a row for each object in the data
		var rows = tbody.selectAll('tr')
		  .data(object_grid.slice(1))
		  .enter()
		  .append('tr');

		// create a cell in each row for each column
		var cells = rows.selectAll('td')
      .data(function(d) {return d; })
		  .enter()
		  .append('td')
		  .attr("class", function(d) { return d; })
		  .attr("id", function(d) { return d; })
		  .style('background-color', function(d) { if (d.length>0) return boxoffcolor; })
		  .html(function(d) {
		  	if (d.length>0){
  		  	return "<a href=" + object_urls[d] + ' target="_blank" rel="noopener noreferrer">' + d + ": " + object_names[d] + "</a>";
		  	}
		  	else {
          return "";
		  	}
		  });


			cells.on('click', function(d) {
				  console.log("state: "+ boxstates[d])
		       boxstates[d] = 1 - boxstates[d];
		       if (boxstates[d] == 0 ) { d3.select(this).style("background-color", boxoffcolor)}
 			     if (boxstates[d] == 1 ) { d3.select(this).style("background-color", boxoncolor)}
		  })

		  function toggle(d, i){
		  	x = d3.select(this);
		  	x.style("background-color", this.oncolor);
		  };

		  function mouse(d, i){		  	
		  };

	  return table;

}


