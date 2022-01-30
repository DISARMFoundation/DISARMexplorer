function makemap(arrayvals) {
    var width = d3.select('#map').node().getBoundingClientRect().width,
            height = d3.select('#map').node().getBoundingClientRect().height;

    var center = [width / 2, height / 2];

    var projection = d3.geo.mercator()
            .center([0, 10]);
    
    var svg = d3.select("#map")
            .append("svg")
            .attr("width", width)
            .attr("height", height);

    var path = d3.geo.path()
            .projection(projection);

    var g = svg.append("g");

    d3.json("world-110m2.json", function (error, topology) {
        g.selectAll("path")
                .data(topojson.object(topology, topology.objects.countries).geometries)
                .enter()
                .append("path")
                .attr("d", path);

        d3.csv("cities.csv", function (error, cities) {

            svg.selectAll("circle")
                    .data(cities)
                    .enter()
                    .append("circle")
                    .attr("cx", function (d) {
                        return projection([d.lon, d.lat])[0];
                    })
                    .attr("cy", function (d) {
                        return projection([d.lon, d.lat])[1];
                    })
                    .attr("r", 5)
                    .style("fill", "red");
        });
    });

    var zoom = d3.behavior.zoom()
            .scaleExtent([1, 8])
            .on("zoom", function () {
                g.attr("transform", "translate(" + d3.event.translate.join(",") + ") scale(" + d3.event.scale + ")");
                g.selectAll("path")
                        .attr("d", path.projection(projection));
                
                svg.selectAll("circle")
                        .attr("transform", "translate(" + d3.event.translate.join(",") + ") scale(" + d3.event.scale + ")")
                        .transition()
                        .attr("r", 5 / d3.event.scale);
                d3.select("#map-zoomer").node().value = zoom.scale();
            });
    svg.call(zoom);

    d3.select('#zoom-in').on('click', function () {
        var scale = zoom.scale(), extent = zoom.scaleExtent(), translate = zoom.translate();
        var x = translate[0], y = translate[1];
        var factor = 1.2;

        var target_scale = scale * factor;

        if (scale === extent[1]) {
            return false;
        }
        var clamped_target_scale = Math.max(extent[0], Math.min(extent[1], target_scale));
        if (clamped_target_scale != target_scale) {
            target_scale = clamped_target_scale;
            factor = target_scale / scale;
        }
        x = (x - center[0]) * factor + center[0];
        y = (y - center[1]) * factor + center[1];

        zoom.scale(target_scale).translate([x, y]);

        g.transition().attr("transform", "translate(" + zoom.translate().join(",") + ") scale(" + zoom.scale() + ")");
        g.selectAll("path")
                .attr("d", path.projection(projection));

        svg.selectAll("circle")
                .transition()
                .attr("transform", "translate(" + zoom.translate().join(",") + ") scale(" + zoom.scale() + ")")
                .attr("r", 5 / zoom.scale());

        d3.select("#map-zoomer").node().value = zoom.scale();
    });

    d3.select('#zoom-out').on('click', function () {
        var scale = zoom.scale(), extent = zoom.scaleExtent(), translate = zoom.translate();
        var x = translate[0], y = translate[1];
        var factor = 1 / 1.2;

        var target_scale = scale * factor;

        if (scale === extent[0]) {
            return false;
        }
        var clamped_target_scale = Math.max(extent[0], Math.min(extent[1], target_scale));
        if (clamped_target_scale != target_scale) {
            target_scale = clamped_target_scale;
            factor = target_scale / scale;
        }
        x = (x - center[0]) * factor + center[0];
        y = (y - center[1]) * factor + center[1];

        zoom.scale(target_scale).translate([x, y]);

        g.transition()
                .attr("transform", "translate(" + zoom.translate().join(",") + ") scale(" + zoom.scale() + ")");
        g.selectAll("path")
                .attr("d", path.projection(projection));

        svg.selectAll("circle")
                .transition()
                .attr("transform", "translate(" + zoom.translate().join(",") + ") scale(" + zoom.scale() + ")")
                .attr("r", 5 / zoom.scale());
        d3.select("#map-zoomer").node().value = zoom.scale();
    });

    d3.select('#reset').on('click', function () {
        zoom.translate([0, 0]);
        zoom.scale(1);
        g.transition().attr("transform", "translate(" + zoom.translate().join(",") + ") scale(" + zoom.scale() + ")");
        g.selectAll("path")
                .attr("d", path.projection(projection))

        svg.selectAll("circle")
                .transition()
                .attr("transform", "translate(" + zoom.translate().join(",") + ") scale(" + zoom.scale() + ")")
                .transition()
                .attr("r", 5 / zoom.scale());
        d3.select("#map-zoomer").node().value = zoom.scale();
    });

    d3.select('#map-zoomer').on("change", function () {
        var scale = zoom.scale(), extent = zoom.scaleExtent(), translate = zoom.translate();
        var x = translate[0], y = translate[1];
        var target_scale = +this.value;
        var factor = target_scale / scale;

        var clamped_target_scale = Math.max(extent[0], Math.min(extent[1], target_scale));
        if (clamped_target_scale != target_scale) {
            target_scale = clamped_target_scale;
            factor = target_scale / scale;
        }
        x = (x - center[0]) * factor + center[0];
        y = (y - center[1]) * factor + center[1];

        zoom.scale(target_scale).translate([x, y]);

        g.transition()
                .attr("transform", "translate(" + zoom.translate().join(",") + ") scale(" + zoom.scale() + ")");
        g.selectAll("path")
                .attr("d", path.projection(projection));

        svg.selectAll("circle")
                .transition()
                .attr("transform", "translate(" + zoom.translate().join(",") + ") scale(" + zoom.scale() + ")")
                .attr("r", 5 / zoom.scale());
    });
}
