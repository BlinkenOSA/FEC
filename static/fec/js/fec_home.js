//counter
$('.counter').waypoint(function () {
    $('.counter').countTo();
    this.destroy();
}, {offset: '100%'});