
// function success(pos) {
//     var crd = pos.coords;
//     lat = crd.latitude;
//     lng = crd.longitude;
//     $('#lat').val(lat);
//     $('#lng').val(lng);
//     LatLng = new google.maps.LatLng(crd.latitude, crd.longitude);
//     map.setCenter(LatLng);
// };

// function error(err) {
//     console.warn('ERROR(' + err.code + '): ' + err.message);
// };

// var options = {
//     enableHighAccuracy: true,
//     timeout: 5000,
//     maximumAge: 0
// };



var map;
function initMap() {
    myLatLng = { lat: 1.37, lng: 103.8 }; //first position
    map = new google.maps.Map(document.getElementById('basicMap'), {
        center: myLatLng,
        zoom: 14
    });
    map.addListener('center_changed', function () {
        lat = map.getCenter().lat();
        lng = map.getCenter().lng();
        $("#lat").val(lat);
        $("#lng").val(lng);
    });
}