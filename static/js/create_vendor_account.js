window.addEventListener('load', function() {
    const autocomplete = new google.maps.places.Autocomplete(document.getElementById('address'));

    autocomplete.addListener('place_changed', function() {
        const place = autocomplete.getPlace();
        if (!place.geometry) {
            console.log('No details available for input: ' + place.name);
            return;
        }
        const address = place.formatted_address;
        document.getElementById('address').value = address;

    });

    //converting address to coordinates
    const form = document.getElementById('vendor-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // prevent form submission

        const apiKey = 'AIzaSyD_6bTYpouO3j8eJSzy_Fx61zyZ9SknsXo';
        const address = document.getElementById('address').value;

        fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(address)}&key=${apiKey}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'OK') {
                    const location = data.results[0].geometry.location;
                    const coordinates = [location.lat, location.lng];
                    document.getElementById('coordinates').value = coordinates.join(',');
                    form.submit(); // submit the form after getting the coordinates
                } else {
                    console.log(`Error: ${data.status}`);
                }
            })
            .catch(error => console.log('Error:', error));
    });
});


