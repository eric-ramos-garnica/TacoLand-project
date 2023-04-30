 // converting strings into arrays
const str = document.getElementById("k").innerHTML;
const arr = JSON.parse(str.replace(/'/g, "\"")).map(coord => {
  const [lat, long] = coord.split(",");
  return { lat, long };
});

const business_title = document.getElementById("business_name").innerHTML;
var business_title_array=JSON.parse(business_title.replace(/'/g, "\""))

const vendor_ids = document.getElementById("vendor_id").innerHTML;
var vendor_ids_array=JSON.parse(vendor_ids.replace(/'/g, "\""))

const hours = document.getElementById("hours").innerHTML;
var hours_array=JSON.parse(hours.replace(/'/g, "\""))

const taco_icons = document.getElementById("business_type").innerHTML;
var taco_icons_array=JSON.parse(taco_icons.replace(/'/g, "\""))

// function for google maps
function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 10,
    center: { lat: 37.3387, lng:  -121.8853 },
  });
  
  "https://img.icons8.com/officexs/15/null/taco.png"
  
  arr.forEach((coord,i) => {
    if( taco_icons_array[i] === 'taco truck'){
      var icon_image ="https://img.icons8.com/color/25/null/food-truck.png";
    }
    else if(taco_icons_array[i] === 'taco stand'){
      var icon_image ="https://img.icons8.com/officexs/25/null/taco.png";
    }

    const marker = new google.maps.Marker({
      position: { lat: Number(coord.lat), lng: Number(coord.long) },
      map,
      icon: {
        url: icon_image,
      },
      animation: google.maps.Animation.DROP
    });
    
    const infoWindow = new google.maps.InfoWindow({
      content: `<a href="/tacovendors/${vendor_ids_array[i]}"><h2>${business_title_array[i]}</h2></a><h2>Hours:${hours_array[i]}</h2>`
    });
    
    marker.addListener('click', () => {
      infoWindow.open(map, marker);
      map.setZoom(14);
      map.setCenter(marker.getPosition());
    }); 
  });
  
  return map;
}

window.initMap = initMap;
initMap();

