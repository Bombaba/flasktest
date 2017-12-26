"use strict";

function initialize() {
    let marker;
    const mapOptions = {
        center: {lat: -33.30578381949298, lng: 26.523442268371582},
        zoom: 15
    };
    const map = new google.maps.Map(
        document.getElementById("map-canvas"), mapOptions
    );
    google.maps.event.addListener(map, 'click',
        (event) => {
            if (marker) {
                marker.setPosition(event.latLng);
            } else {
                marker = new google.maps.Marker({
                    position: event.latLng,
                    map: map
                });
            }
            document.getElementById('latitude').value = event.latLng.lat();
            document.getElementById('longitude').value = event.latLng.lng();
        }
    )
}

function placeCrimes(crimes) {
    for (const [i, c] of crimes.entries()) {
        const crime = new google.maps.Marker({
            position: {lat: c.latitude, lng: c.longitude},
            map: map,
            title: `${c.date}\n${c.category}\n${c.description}`
        });
    }
}