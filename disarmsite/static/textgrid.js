
function fillGrid(params) {

	// grab dataset from input parameters
	var grid_div = params[0]; 
	var topcolor = params[1];
	var object_grid = params[2]; 
	var object_names = params[3]; 
	console.log(object_names);
	var numrows = object_grid.length;
	var numcols = object_grid[0].length;

	var data = new Array();
	var xpos = 1; //starting xpos and ypos at 1 so grid edges are visible
	var ypos = 1;
	var boxwidth = 60;
	var boxheight = 25;
	var boxstate = 0;
	var boxoffcolor = '#D0D3D4';
	var boxoncolor = "#50C878";
	
	// set position, width/height/text/number of clicks per box
	for (var row = 0; row < numrows; row++) {
		for (var col = 0; col < numcols; col++) {
			var disarmid = object_grid[row][col];
			var disarmname = object_names[disarmid];
			// console.log(disarmname);
			// FIXIT: add names for tactic stages too
			var color = (row == 0) ? topcolor : '#D0D3D4';
            if (disarmid != '') {
				data.push({
					x: xpos,
					y: ypos,
					width: boxwidth,
					height: boxheight,
					disarmid: disarmid,
					disarmname: disarmname,
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


	// grab dataset
	console.log(data);

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
		.style("font-size", "10px")
		.on('click', function(d) {
	       d.state = 1 - d.state;
	       if (d.state == 0 ) { d3.select(this).style("fill",function(d) { return d.offcolor;}); }
		   if (d.state == 1 ) { d3.select(this).style("fill",function(d) { return d.oncolor;}); }
	  });

	box.append("text")
		.attr("x", function(d) { return d.x + 3; })
		.attr("y", function(d) { return d.y + boxheight/2; })
		.attr("dy", ".35em")
		.text(function(d) { return d.disarmid; });

}




