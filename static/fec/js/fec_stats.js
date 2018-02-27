var total_num_trace;
var country_trace;
var csvdata = [];

Plotly.d3.csv('/static/fec/stat/fec_number_of_reports.csv', function(err, csv_number_of_reports) {
    Plotly.d3.csv('/static/fec/stat/fec_number_of_countries.csv', function(err, csv_number_of_countries) {
        Plotly.d3.csv('/static/fec/stat/fec_number_of_people.csv', function(err, csv_number_of_people) {
            var trace1, trace2, trace3;

            $('.countrydata').select2({
                theme: "bootstrap"
            }).on("change", function (e) {
                updateCountry();
            });

            $('.persondata').select2({
                theme: "bootstrap"
            }).on("change", function (e) {
                updatePerson();
            });

            function unpack(rows, key) {
                return rows.map(function(row) { return row[key]; });
            }

            var allWeeksD1 = unpack(csv_number_of_reports, 'week');
            var totalNumberOfMessages = unpack(csv_number_of_reports, 'number_of_messages');

            trace1 = {
                x: allWeeksD1,
                y: totalNumberOfMessages,
                mode: 'lines+markers',
                name: 'Total number of messages'
            };

            // Arrange countries
            var allWeeksD2 = unpack(csv_number_of_countries, 'week');
            var allCountries = unpack(csv_number_of_countries, 'country');
            var allCountryTotals = unpack(csv_number_of_countries, 'number_of_messages');
            var listofCountries = [];
            var currentCountryTotal = [];
            var currentCountryWeek = [];

            for (var i = 0; i < allCountries.length; i++ ){
                if (listofCountries.indexOf(allCountries[i]) === -1 ){
                    listofCountries.push(allCountries[i]);
                }
            }

            function getCountryData(chosenCountry) {
                currentCountryTotal = [];
                currentCountryWeek = [];
                for (var i = 0 ; i < allCountries.length ; i++){
                    if ( allCountries[i] === chosenCountry ) {
                        currentCountryTotal.push(allCountryTotals[i]);
                        currentCountryWeek.push(allWeeksD2[i]);
                    }
                }
            }

            function setCountryBubblePlot(chosenCountry) {
                getCountryData(chosenCountry);

                trace2 = {
                    x: currentCountryWeek,
                    y: currentCountryTotal,
                    mode: 'lines+markers',
                    name: chosenCountry
                };
            }

            var countrySelector = document.querySelector('.countrydata');

            // Arrange people
            var allWeeksD3 = unpack(csv_number_of_people, 'week');
            var allPeople = unpack(csv_number_of_people, 'person');
            var allPeopleTotals = unpack(csv_number_of_people, 'number_of_messages');
            var listOfPeople = [];
            var currentPersonTotal = [];
            var currentPersonWeek = [];

            for (var i = 0; i < allPeople.length; i++ ){
                if (listOfPeople.indexOf(allPeople[i]) === -1 ){
                    listOfPeople.push(allPeople[i]);
                }
            }

            function getPersonData(chosenPerson) {
                currentPersonTotal = [];
                currentPersonWeek = [];
                for (var i = 0 ; i < allPeople.length ; i++){
                    if ( allPeople[i] === chosenPerson ) {
                        currentPersonTotal.push(allPeopleTotals[i]);
                        currentPersonWeek.push(allWeeksD3[i]);
                    }
                }
            }

            function setPersonBubblePlot(chosenPerson) {
                getPersonData(chosenPerson);

                trace3 = {
                    x: currentPersonWeek,
                    y: currentPersonTotal,
                    mode: 'lines+markers',
                    name: chosenPerson
                };
            }

            var personSelector = document.querySelector('.persondata');

            function assignOptions(textArray, selector) {
                textArray = textArray.sort();
                for (var i = 0; i < textArray.length;  i++) {
                    var currentOption = document.createElement('option');
                    currentOption.text = textArray[i];
                    selector.appendChild(currentOption);
                }
            }

            assignOptions(listofCountries, countrySelector);
            assignOptions(listOfPeople, personSelector);

            function updateCountry(){
                setCountryBubblePlot(countrySelector.value);
                draw();
            }

            function updatePerson(){
                setPersonBubblePlot(personSelector.value);
                draw();
            }

            countrySelector.addEventListener('change', updateCountry, false);
            personSelector.addEventListener('change', updatePerson, false);

            // Default Country Data
            setCountryBubblePlot('USA');

            // Default Person Data
            setPersonBubblePlot('Brown');

            $('.countrydata').val('USA');
            $('.countrydata').trigger('change');

            $('.persondata').val('Brown');
            $('.persondata').trigger('change');

            draw();

            function draw() {
                // Global additions
                var layout = { title: "Free Europe Committee Statistics" };
                var data = [trace1, trace2, trace3];

                Plotly.newPlot('plotdiv', data, layout);
            }
        });
    });
});