

function wrap(text, width) {
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


function fillGridOld(params) {

	// grab dataset from input parameters
	var grid_div = params[0]; 
	var topcolor = params[1];
	var object_grid = params[2]; 
	var object_names = params[3]; 
	console.log(object_names);

	var numrows = object_grid.length;
	var numcols = object_grid[0].length;

	var boxwidth = 110;
	var boxheight = 50;
	var boxoffcolor = '#D0D3D4';
	var boxoncolor = "#50C878";
	

	// grab dataset
	var data = new Array();
	data = populatedata(object_grid, object_names, numrows, numcols, topcolor, boxwidth, boxheight, boxoncolor, boxoffcolor);

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

	box.append("text")
		.attr("x", function(d) { return d.x + 3; })
		.attr("y", function(d) { return d.y + boxheight/2; })
		.attr("class", "wrapme")
		.attr("dy", ".20em")
		.attr("font-size", "9px")
		.text(function(d) { return d.disarmname; });

	//d3.selectAll('.wrapme').call(wrap);

}



function fillGrid(params) {

	// grab dataset from input parameters
	var grid_div = params[0]; 
	var topcolor = params[1];
	var object_grid = params[2]; 
	var object_names = params[3]; 
	console.log(object_names);

	var numrows = object_grid.length;
	var numcols = object_grid[0].length;

	var boxwidth = 75;
	var boxheight = 50;
	var boxoffcolor = '#D0D3D4';
	var boxoncolor = "#50C878";
	

	// grab dataset
	var data = new Array();
	data = populatedata(object_grid, object_names, numrows, numcols, topcolor, boxwidth, boxheight, boxoncolor, boxoffcolor);
  console.log(data)

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

	// grab dataset from input parameters
	var grid_div = params[0]; 
	var topcolor = params[1];
	var object_grid = params[2]; 
	var object_names = params[3]; 
	console.log(object_names);

	var numrows = object_grid.length;
	var numcols = object_grid[0].length;

	var boxwidth = 75;
	var boxheight = 50;
	var boxoffcolor = '#D0D3D4';
	var boxoncolor = "#50C878";
	

	// grab dataset
	var data = new Array();
	data = populatedata(object_grid, object_names, numrows, numcols, topcolor, boxwidth, boxheight, boxoncolor, boxoffcolor);
  console.log(data)

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


function fillHtmlSimpleTable(params) {
	// useful for creating lists of e.g. techniques

	// grab dataset from input parameters
	var grid_div = params[0]; 
	var topcolor = params[1];
	var object_grid = params[2]; 
	var object_names = params[3]; 
	console.log(object_names);

	var numrows = object_grid.length;
	var numcols = object_grid[0].length;

	var boxwidth = 75;
	var boxheight = 50;
	var boxoffcolor = '#D0D3D4';
	var boxoncolor = "#50C878";
	

	// grab dataset
	var data = new Array();
	data = populatedata(object_grid, object_names, numrows, numcols, topcolor, boxwidth, boxheight, boxoncolor, boxoffcolor);
  console.log(data)

  var table = d3.select(grid_div).append('table');
  var thead = table.append('thead');
  var tbody = table.append('tbody');
  var columns = ['disarmid', 'disarmname'];

  thead.append('tr')
    .selectAll('th')
    .data(columns).enter()
    .append('th')
      .text(function (column) { return column; });

		// create a row for each object in the data
		var rows = tbody.selectAll('tr')
		  .data(data)
		  .enter()
		  .append('tr');

		// create a cell in each row for each column
		var cells = rows.selectAll('td')
		  .data(function (row) {
		    return columns.map(function (column) {
		      return {column: column, value: row[column]};
		    });
		  })
		  .enter()
		  .append('td')
		    .text(function (d) { return d.value; });

	  return table;

}

function fillHtmlTable(params) {

	// grab dataset from input parameters
	var grid_div = params[0]; 
	var topcolor = params[1];
	var object_grid = params[2]; 
	var object_names = params[3]; 
	var object_urls = params[4]; 
	console.log(object_names);

	var numrows = object_grid.length;
	var numcols = object_grid[0].length;

	var boxwidth = 75;
	var boxheight = 50;
	var boxoffcolor = '#D0D3D4';
	var boxoncolor = "#50C878";
	

	// grab dataset
	var data = new Array();
	data = populatedata(object_grid, object_names, numrows, numcols, topcolor, boxwidth, boxheight, boxoncolor, boxoffcolor);
  console.log(data)

  var table = d3.select(grid_div).append('table');
  var thead = table.append('thead');
  var tbody = table.append('tbody');
  var columns = object_grid[0];

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
		  .html(function(d) {
		  	if (d.length>0){
  		  	return "<a href=" + object_urls[d] + ">" + d + ": " + object_names[d] + "</a>";
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

	  return table;

}

