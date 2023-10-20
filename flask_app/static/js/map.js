const markers = {};
let map;

// WebSocket
const socket = io();

socket.on("connect", () => {
  console.log("Server is listening...");
});

socket.on("disconnect", () => {
  console.log("Server has disconnected");
});

// Update or add a truck location
socket.on("location", truckData => {
  const data = truckData.map(str => parseFloat(str));
  const marker = markers[String(data[0])];

  if (marker) {  // Update
    const newPosition = new google.maps.LatLng(data[2], data[3]);
    marker.setPosition(newPosition);
  } else {  // Add
    const newMarker = new google.maps.Marker({
      position: { lat: data[2], lng: data[3] },
      map: map,
      title: "Ubicación del Camión: " + String(data[1])
    });

    const infowindow = new google.maps.InfoWindow({
      content: "Camión: " + String(data[1])
    });

    newMarker.addListener("click", () => {
      infowindow.open(map, newMarker);
    });

    markers[truckData[0]] = newMarker;
  }
});

// Google Maps
function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 25.687, lng: -100.318 },
    zoom: 11
  });

  // Get coords
  google.maps.event.addListener(map, "rightclick", function(event) {
    const lat = event.latLng.lat();
    const lng = event.latLng.lng();

    alert("Latitud = " + lat + "\nLongitud = " + lng);
  });

  // Add markers to the map
  const locations = JSON.parse(document.getElementById("locations-container").dataset.locations);
  locations.forEach(location => {
    const marker = new google.maps.Marker({
      position: { lat: parseFloat(location[2]), lng: parseFloat(location[3]) },
      map: map,
      title: "Ubicación del Camión: " + String(location[1])
    });

    const infowindow = new google.maps.InfoWindow({
      content: "Camión: " + String(location[1])
    });

    marker.addListener("click", () => {
      infowindow.open(map, marker);
    });

    markers[String(location[0])] = marker;
  });
}
