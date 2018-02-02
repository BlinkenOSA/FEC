$(function() {

    var $UV = $('#uv');

    window.addEventListener('uvLoaded', function(e) {

        urlDataProvider = new UV.URLDataProvider(true);
        var formattedLocales;
        var locales = urlDataProvider.get('locales', '');

        if (locales) {
            var names = locales.split(',');
            formattedLocales = [];

            for (var i in names) {
                var nameparts = String(names[i]).split(':');
                formattedLocales[i] = {name: nameparts[0], label: nameparts[1]};
            }

        } else {
            formattedLocales = [
                {
                    name: 'en-GB'
                }
            ]
        }

        uv = createUV('#uv', {
            root: '.',
            iiifResourceUri: urlDataProvider.get('manifest'),
            collectionIndex: Number(urlDataProvider.get('c', 0)),
            manifestIndex: Number(urlDataProvider.get('m', 0)),
            sequenceIndex: Number(urlDataProvider.get('s', 0)),
            canvasIndex: Number(urlDataProvider.get('cv', 0)),
            rotation: Number(urlDataProvider.get('r', 0)),
            xywh: urlDataProvider.get('xywh', ''),
            embedded: true,
            locales: formattedLocales
        }, urlDataProvider);

    }, false);

    function resize() {
        var windowWidth = window.innerWidth;
        var windowHeight = window.innerHeight;
        $UV.width(windowWidth);
        $UV.height(windowHeight);
    }

    $(window).on('resize' ,function() {
        resize();
    });

    resize();
});


