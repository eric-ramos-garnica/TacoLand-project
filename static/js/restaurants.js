// converting string to array objects
var mex_restaurants = document.getElementById("k").innerHTML;
var mex_restaurants_array=JSON.parse(mex_restaurants.replace(/'/g, "\""));

const business_title = document.getElementById("business_name").innerHTML;
var business_title_array=JSON.parse(business_title.replace(/'/g, "\""))

const phones = document.getElementById("phone").innerHTML;
var phones_array=JSON.parse(phones.replace(/'/g, "\""))

const reg = document.getElementById("regions").innerHTML;
var reg_obj=JSON.parse(reg.replace(/'/g, "\""))

const vendor_ids = document.getElementById("vendor_id").innerHTML;
var vendor_ids_array=JSON.parse(vendor_ids.replace(/'/g, "\""))


// function for google maps
function initMap() {
const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 10,
    center: { lat: reg_obj.latitude, lng:  reg_obj.longitude },
});

mex_restaurants_array.forEach((coord,i) => {
    
    const marker = new google.maps.Marker({
    position: { lat: coord.latitude, lng: coord.longitude},
    map,
    icon:"https://img.icons8.com/external-nawicon-outline-color-nawicon/16/null/external-taco-fast-food-nawicon-outline-color-nawicon.png",
    animation: google.maps.Animation.DROP
    });
    
    const infoWindow = new google.maps.InfoWindow({
    content: `<a href="/restaurantInfo/${vendor_ids_array[i]}"><h2>${business_title_array[i]}</h2></a><h2>Phone:${phones_array[i]}</h2>`
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