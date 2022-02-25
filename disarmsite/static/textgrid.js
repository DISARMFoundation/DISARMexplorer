
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



function fillGrid(params) {
	// Used in technique index, counters index

	// grab dataset from input parameters
	var grid_div = params[0]; 
	var topcolor = params[1];
	var object_grid = params[2]; 
	var object_names = params[3]; 
	//console.log(object_names);

	var numrows = object_grid.length;
	var numcols = object_grid[0].length;

	var boxwidth = 75;
	var boxheight = 50;
	var boxoffcolor = '#D0D3D4';
	var boxoncolor = "#50C878";
	

	// grab dataset
	var data = new Array();
	data = populatedata(object_grid, object_names, numrows, numcols, topcolor, boxwidth, boxheight, boxoncolor, boxoffcolor);
  //console.log(data)

	//Create the grid
	var grid = d3.select(grid_div)
		.append("svg")
		.attr("width",boxwidth*numcols+10+"px")
		.attr("height",boxheight*numrows+10+"px");
	
	// Fill the grid
	var box = grid.selectAll("g")
		.data(data)
		.enter().append("g")
		.attr("class", "box");
		
	box.append("rect")
		.attr("class","square")
		.attr("x", function(d) { return d.x; })
		.attr("y", function(d) { return d.y; })
		.attr("disarmid", function(d) { return d.disarmid; })
		.attr("width", function(d) { return d.width; })
		.attr("height", function(d) { return d.height; })
		.style("fill", function(d) { return d.offcolor; })
		.style("stroke", "#222")
		.style("font-size", "9px")
		.on('click', function(d) {
	       d.state = 1 - d.state;
	       if (d.state == 0 ) { d3.select(this).style("fill",function(d) { return d.offcolor;}); }
		   if (d.state == 1 ) { d3.select(this).style("fill",function(d) { return d.oncolor;}); }
	  });

  // Tech debt: brute forcing the line spacing here - is going to be an issue if we change the box heights. 
	box.append("text")
		.attr("x", function(d) { return d.x + 3; })
		.attr("y", function(d) { return d.y + 10; })
		.attr("dy", ".20em")
		.attr("font-size", "8px")
		.text(function(d) { return d.disarmname1; });

	box.append("text")
		.attr("x", function(d) { return d.x + 3; })
		.attr("y", function(d) { return d.y + 20; })
		.attr("dy", ".20em")
		.attr("font-size", "8px")
		.text(function(d) { return d.disarmname2; });

	box.append("text")
		.attr("x", function(d) { return d.x + 3; })
		.attr("y", function(d) { return d.y + 30; })
		.attr("dy", ".20em")
		.attr("font-size", "8px")
		.text(function(d) { return d.disarmname3; });

	box.append("text")
		.attr("x", function(d) { return d.x + 3; })
		.attr("y", function(d) { return d.y + 40; })
		.attr("dy", ".20em")
		.attr("font-size", "8px")
		.text(function(d) { return d.disarmname4; });

	//d3.selectAll('.wrapme').call(wrap);

}

function fillTable(params) {
	// Creates the array of buttons 
	// used on the front page

	// grab dataset from input parameters
	var grid_div = params[0]; 
	var topcolor = params[1];
	var object_grid = params[2]; 
	var object_names = params[3]; 
	//console.log(object_names);

	var numrows = object_grid.length;
	var numcols = object_grid[0].length;

	var boxwidth = 75;
	var boxheight = 50;
	var boxoffcolor = '#D0D3D4';
	var boxoncolor = "#50C878";
	

	// grab dataset
	var data = new Array();
	data = populatedata(object_grid, object_names, numrows, numcols, topcolor, boxwidth, boxheight, boxoncolor, boxoffcolor);
  //console.log(data)

	//Create the grid
	var grid = d3.select(grid_div)
		.append("svg")
		.attr("width",boxwidth*numcols+10+"px")
		.attr("height",boxheight*numrows+10+"px");
	
	// Fill the grid
	var box = grid.selectAll("g")
		.data(data)
		.enter().append("g")
		.attr("class", "box");
		
	box.append("rect")
		.attr("class","square")
		.attr("x", function(d) { return d.x; })
		.attr("y", function(d) { return d.y; })
		.attr("disarmid", function(d) { return d.disarmid; })
		.attr("width", function(d) { return d.width; })
		.attr("height", function(d) { return d.height; })
		.style("fill", function(d) { return d.offcolor; })
		.style("stroke", "#222")
		.style("font-size", "9px")
		.on('click', function(d) {
	       d.state = 1 - d.state;
	       if (d.state == 0 ) { d3.select(this).style("fill",function(d) { return d.offcolor;}); }
		   if (d.state == 1 ) { d3.select(this).style("fill",function(d) { return d.oncolor;}); }
	  });

  // Tech debt: brute forcing the line spacing here - is going to be an issue if we change the box heights. 
	box.append("text")
		.attr("x", function(d) { return d.x + 3; })
		.attr("y", function(d) { return d.y + 10; })
		.attr("dy", ".20em")
		.attr("font-size", "8px")
		.text(function(d) { return d.disarmname1; });

	box.append("text")
		.attr("x", function(d) { return d.x + 3; })
		.attr("y", function(d) { return d.y + 20; })
		.attr("dy", ".20em")
		.attr("font-size", "8px")
		.text(function(d) { return d.disarmname2; });

	box.append("text")
		.attr("x", function(d) { return d.x + 3; })
		.attr("y", function(d) { return d.y + 30; })
		.attr("dy", ".20em")
		.attr("font-size", "8px")
		.text(function(d) { return d.disarmname3; });

	box.append("text")
		.attr("x", function(d) { return d.x + 3; })
		.attr("y", function(d) { return d.y + 40; })
		.attr("dy", ".20em")
		.attr("font-size", "8px")
		.text(function(d) { return d.disarmname4; });

	//d3.selectAll('.wrapme').call(wrap);

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
    caption = table.append("caption"),
		thead = table.append('thead'),
		tbody = table.append('tbody');
  var columns = object_grid[0];

  var caption = thead.append("tr").append("th").attr("colspan", columns.length);
  caption.html("<b>" + tableheading + "</b>")
    .style('background-color', topcolor)
    .style("font-size", "20px");

  thead.append('tr')
    .selectAll('th')
    .data(columns).enter()
    .append('th')
		// .html(function(d) {
  // 		  return "<a href=" + object_urls[d] + ">" + d + ": " + object_names[d] + "</a>";
  // 	};
    .text(function (column) { return column + ": " + object_names[column]; });

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
		  // .on('click', toggle)
			// .on('click', function(d, i) {
		 //       d.state = 1 - d.state;
		 //       if (d.state == 0 ) { d3.select(d).style("background-color",function(d) { return d.offcolor;}); }
			//    if (d.state == 1 ) { d3.select(d).style("background-color",function(d) { return d.oncolor;}); }
		 //  })
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
		  // .text(function (d) { return })
		  // .on("click",function(d,i) { alert("Clicked on the text");})
		  // .append("a")
		  // .attr("href", function(d) {
		  // 	return "example.com"
		  });


			cells.on('click', function(d) {
				  console.log("state: "+ boxstates[d])
		       boxstates[d] = 1 - boxstates[d];
		       if (boxstates[d] == 0 ) { d3.select(this).style("background-color", boxoffcolor)}
 			     if (boxstates[d] == 1 ) { d3.select(this).style("background-color", boxoncolor)}
		  })

		  // cells.on("click", toggle)
		  //   .on("mouseover", mouse);

		  function toggle(d, i){
		  	x = d3.select(this);
		  	x.style("background-color", this.oncolor);
		  	// x.style("background-color", "blue");
		  	// d.state = 1 - d.state;
		   //  if (d.state == 0 ) { x.style("fill",function(d) { return d.offcolor;}); }
			  // if (d.state == 1 ) { x.style("fill",function(d) { return d.oncolor;}); }

		  	console.log('toggled '+ i + ":" + d);
		  };

		  function mouse(d, i){		  	
		  };

	  return table;

}


