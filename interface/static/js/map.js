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
  google.maps.event.addListener(map, "rightclick", event => {
    const lat = event.latLng.lat();
    const lng = event.latLng.lng();

    alert("Latitud = " + lat + "\nLongitud = " + lng);
  });

  // Add markers to the map
  const locations = JSON.parse(document.getElementById("dataset").dataset.locations);
  const trucks = locations.trucks;
  const air = locations.air;

  // Truck's location
  trucks.forEach(truck => {
    const marker = new google.maps.Marker({
      position: { lat: parseFloat(truck.latitude), lng: parseFloat(truck.longitude) },
      map: map,
      title: `Ubicación del Camión: ${truck.name}`
    });

    const infowindow = new google.maps.InfoWindow({
      content: `
        <div style="font-size: 14px; color: #333;">
          <strong>Camión:</strong> ${truck.name} ICA<br>
        </div>
      `
    });

    marker.addListener("click", () => {
      infowindow.open(map, marker);
    });

    markers[String(truck.id)] = marker;
  });

  // Air quality
  air.forEach(record => {
    const circle = new google.maps.Circle({
      map: map,
      fillColor: getColorForQuality(record.quality),
      fillOpacity: 0.15,
      strokeOpacity: 0,
      center: { lat: parseFloat(record.latitude), lng: parseFloat(record.longitude) },
      radius: 3000
    });

    const infowindow = new google.maps.InfoWindow({
      content: `
        <div style="font-size: 14px; color: #333;">
          <strong>Quality:</strong> ${record.quality}<br>
          <strong>Has Contaminants:</strong> ${record.contaminants ? "Yes" : "No"}
        </div>
      `
    });

    google.maps.event.addListener(circle, "click", event => {
      infowindow.setPosition(event.latLng);
      infowindow.open(map);
    });
  });
}

// Function to get color based on quality
function getColorForQuality(quality) {
  const hue = (1 - quality / 500) * 120;
  return `hsl(${hue}, 100%, 50%)`;
}
