function setfacets() {
    var collected_facets = {};

    selected_facets.forEach(function (element) {
        var facet = element.split(':');
        var facet_name = facet[0];
        var facet_value = facet[1];

        if(facet_name in collected_facets) {
            collected_facets[facet_name].push(facet_value);
        } else {
            collected_facets[facet_name] = [facet_value];
        }
    });

    for(key in collected_facets) {
        $('#'+key+'_facet').val(collected_facets[key]);
        $('#'+key+'_facet').trigger("change");
    }
}

setfacets();