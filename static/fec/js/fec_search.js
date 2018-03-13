var dateSlider = document.getElementById('slider');

// Create a new date from a string, return as a timestamp.
function timestamp(str){
    return new Date(str).getTime();
}

var noUiOpts = {
    range: {
        min: timestamp(global_start_date),
        max: timestamp(global_end_date)
    },

    // Steps of one day
    step: 24 * 60 * 60 * 1000,

    // Two more timestamps indicate the handle starting positions.
    start: [ timestamp(current_start_date), timestamp(current_end_date) ],

    connect: true,
    behaviour: 'drag',

    // No decimals
	format: wNumb({
		decimals: 0
	})
}

noUiSlider.create(dateSlider, noUiOpts);

var dateDisplayValues = [
	document.getElementById('date-start'),
	document.getElementById('date-end')
];

var dateValues = [
	$('#id_start_date'),
	$('#id_end_date')
]

dateSlider.noUiSlider.on('update', function( values, handle ) {
    dateDisplayValues[handle].innerHTML = formatDate(new Date(+values[handle]));
    dateValues[handle].val(formatDate(new Date(+values[handle])));
});

dateSlider.noUiSlider.on('end', function(){
    $( "#searchform" ).submit();
});

// Create a string representation of the date.
function formatDate ( date ) {
    return date.getFullYear() + '-' + ('0' + (date.getMonth()+1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2);
}

$('#associated_people_facet').select2({
    theme: "bootstrap",
    placeholder: "People as Contributors"
});

$('#subject_people_facet').select2({
    theme: "bootstrap",
    placeholder: "People as Subject"
});

$('#subject_corporations_facet').select2({
    theme: "bootstrap",
    placeholder: "Corporations as Subject"
});

$('#countries_facet').select2({
    theme: "bootstrap",
    placeholder: "Countries"
});

$('#place_facet').select2({
    theme: "bootstrap",
    placeholder: "Associated Places"
});

$('.facet-select2').on('change', function (e) {
    $( "#searchform" ).submit();
});
