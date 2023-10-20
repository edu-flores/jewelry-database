// Global variables
const markers = {};
let map;
let timer;

// WebSocket
const socket = io.connect("http://localhost:5002");

socket.on("connect", () => {
  console.log("Server is listening...");
  timer = setInterval(() => {
    socket.emit("update");
  }, 3000);  // Every 3 seconds
});

socket.on("disconnect", () => {
  console.log("Server has disconnected");
  clearInterval(timer);
});

// Update markers in real time
socket.on("updated", trucks => {
  trucks.forEach(truck => {
    const marker = markers[String(truck[0])];
    const newPosition = new google.maps.LatLng(truck[2], truck[3]);
    marker.setPosition(newPosition);
  });

  console.log("Trucks' location updated!")
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
  const locations = JSON.parse(document.getElementById("dataset").dataset.locations);
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
