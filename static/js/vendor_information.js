var map;
const coordinate = document.getElementById("coord").innerHTML.split(","); 
const hr = document.getElementById("hr").innerHTML; 
const rating = document.getElementById("rating").innerHTML;
const business_type = document.getElementById("taco-icon").innerHTML;
const business_name = document.getElementById("business-name").innerHTML;



function initMap() {

  var coords = document.getElementById('coord').innerHTML.split(',');
  var latLng = { lat: parseFloat(coords[0]), lng: parseFloat(coords[1]) };

  map = new google.maps.Map(document.getElementById('map'), {
    center: latLng,
    zoom: 13
  });
   
  if( business_type=== 'taco truck'){
      var icon_image ="https://img.icons8.com/color/25/null/food-truck.png";
    }
  else if(business_type === 'taco stand'){
      var icon_image ="https://img.icons8.com/officexs/25/null/taco.png";
    }

  var marker = new google.maps.Marker({
    position: latLng,
    map: map,
    icon:{
        url: icon_image,
      },
      animation: google.maps.Animation.DROP
  });

  var infoWindow = new google.maps.InfoWindow({
      content:`<a href="#"><h2>${business_name}</h2></a><h2>Hours:${hr}<h2><h2>Rating:${rating}</h2>`
    });
    marker.addListener('click',function(){
      infoWindow.open(map,marker)
      map.setZoom(14);
      // map.setCenter(marker.getPosition());
    });


}


function calculateRoute() {

  var origin = document.getElementById('origin').value;
  var destination = document.getElementById('destination').value;

  var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer({ 
    // draggable:true,   //i commented this  so the route wont be draggable.
    panel: document.getElementById("panel"),
  });

  // Added this line so it can flex row map and direction
  document.getElementById('panel').removeAttribute('style');
  document.getElementById("container-map-output").classList.add("directions-map-flex-row");
  

  directionsRenderer.addListener("directions_changed", ()=>{
    const directions = directionsRenderer.getDirections();

  });

  displayRoute(origin,destination,directionsService,directionsRenderer);


  directionsRenderer.setMap(map);

  directionsService.route(
    {
      origin: origin,
      destination: destination,
      travelMode: google.maps.TravelMode.DRIVING
    },
    function(response, status) {
      if (status === 'OK') {
        const output = document.querySelector('#output');
        output.innerHTML = "<div class='alert-info'> From: " + document.getElementById("origin").value + ".<br>To: " + document.getElementById("destination").value + ".<br>Driving distance <i class='fa-solid fa-road' style='color:rgb(240,120,68);' ></i>:" + response.routes[0].legs[0].distance.text + ".<br>Duration <i class='fa-solid fa-hourglass-half' style='color:rgb(240,120,68);'></i> : " + response.routes[0].legs[0].duration.text + ". </div>" ;
        directionsRenderer.setDirections(response);
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    });
    
  }
   
function displayRoute(origin, destination,service,display){
  service.route({
    origin:origin,
    destination:destination,
    travelMode:google.maps.TravelMode.DRIVING,
    avoidTolls: true,
  })
  .then(function(result){
    display.setDirections(result);
  })
  .catch(function(e) {
    alert("Could not display directions due to: " + e)
  });
}