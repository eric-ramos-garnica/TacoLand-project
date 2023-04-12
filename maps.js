
function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 10,
    center: { lat: 37.3387, lng:  -121.8853 },
  });    

  const marker = new google.maps.Marker({
    position: { lat:  37.43188, lng:  -121.87224 },
    map,
    icon:{
      url: "https://img.icons8.com/officexs/15/null/taco.png",
    },
    animation: google.maps.Animation.DROP
  });
  var infoWindow = new google.maps.InfoWindow({
    content:'<a href="www.soccer.com"><h2>Tacos el Gordo</h2></a>'
  });
  marker.addListener('click',function(){
    infoWindow.open(map,marker)
    map.setZoom(14);
    // map.setCenter(marker.getPosition());
  }); 
}


window.initMap = initMap;
initMap();