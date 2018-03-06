Promise.all([
  fetch('/static/fec/stat/fec_graph.json', {mode: 'no-cors'})
    .then(function(res) {
       return res.json()
    })
])
    .then(function(dataArray){
      var cy = cytoscape({
        container: document.getElementById('cy'), // container to render in
        elements: dataArray[0],

        layout: {
          name: 'cose',
          idealEdgeLength: 100,
          nodeOverlap: 20,
          refresh: 20,
          fit: true,
          padding: 30,
          randomize: false,
          componentSpacing: 100,
          nodeRepulsion: 400000,
          edgeElasticity: 100,
          nestingFactor: 5,
          gravity: 80,
          numIter: 1000,
          initialTemp: 200,
          coolingFactor: 0.95,
          minTemp: 1.0
        },

        style: [
          {
            "selector": "core",
            "style": {
              "selection-box-color": "#AAD8FF",
              "selection-box-border-color": "#8BB0D0",
              "selection-box-opacity": "0.5"
            }
          }, {
            "selector": "node",
            "style": {
              "width": "mapData(score, 0, 0.006769776522008331, 20, 60)",
              "height": "mapData(score, 0, 0.006769776522008331, 20, 60)",
              "content": "data(label)",
              "font-size": "12px",
              "text-valign": "center",
              "text-halign": "center",
              "background-color": "#555",
              "text-outline-color": "#555",
              "text-outline-width": "2px",
              "color": "#fff",
              "overlay-padding": "6px",
              "z-index": "10"
            }
          },{
              "selector": "node:selected",
              "style": {
                "border-width": "6px",
                "border-color": "#AAD8FF",
                "border-opacity": "0.5",
                "background-color": "#77828C",
                "text-outline-color": "#77828C"
              }
          },{
            "selector": "edge",
            "style": {
              "curve-style": "haystack",
              "haystack-radius": "0.5",
              "opacity": "0.4",
              "line-color": "#bbb",
              "width": "mapData(weight, 0, 1, 1, 8)",
              "overlay-padding": "3px"
            }
          },
        ],
        selectionType: 'single'
      });
    });




