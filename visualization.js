document.addEventListener("DOMContentLoaded", function() {
    // Load the graph data
    d3.json("{{ graph_data|tojson|safe }}", function(error, graph) {
        if (error) throw error;

        // Create the NetworkX graph
        var G = window.networkx.fromJSON(graph);

        // Clear the container
        var container = document.getElementById("visualization");
        container.innerHTML = "";

        // Set up the SVG container
        var svg = d3.select(container).append("svg")
            .attr("width", "100%")
            .attr("height", "100%");

        // Set up the force simulation
        var simulation = window.networkx.forceSimulation(G)
            .force("link", window.networkx.forceLink().id(function(d) { return d.id; }))
            .force("charge", window.networkx.forceManyBody())
            .force("center", window.networkx.forceCenter(container.clientWidth / 2, container.clientHeight / 2));

        // Draw the edges
        var link = svg.selectAll(".link")
            .data(G.edges())
            .enter().append("line")
            .attr("class", "link");

        // Draw the nodes
        var node = svg.selectAll(".node")
            .data(G.nodes())
            .enter().append("circle")
            .attr("class", "node")
            .attr("r", 5)
            .call(window.networkx.drag(simulation));

        // Update node and edge positions on each tick
        simulation.on("tick", function() {
            link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node.attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });
        });
    });
});
