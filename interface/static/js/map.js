// Global variables
const truckMarkers = {};
const airCircles = [];
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
socket.on("updated", ({ trucks, air }) => {
  trucks.forEach(truck => {
    const marker = truckMarkers[truck.id];
    const newPosition = new google.maps.LatLng(truck.latitude, truck.longitude);
    marker.setPosition(newPosition);
  });

  removeCircles();
  placeCircles(air);

  console.log("Map updated!")
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

    truckMarkers[truck.id] = marker;
  });

  // Air quality
  placeCircles(air);
}

// Function to place circles on the map
const placeCircles = data => {
  data.forEach(record => {
    const circle = new google.maps.Circle({
      map: map,
      fillColor: getColorForQuality(record.quality),
      fillOpacity: 0.15,
      strokeOpacity: 0,
      center: { lat: parseFloat(record.latitude), lng: parseFloat(record.longitude) },
      radius: 5000
    });

    const infowindow = new google.maps.InfoWindow({
      content: `
        <div style="font-size: 14px; color: #333;">
          <strong>Quality:</strong> ${record.quality} ICA<br>
          <strong>Has Contaminants:</strong> ${record.contaminants ? "Yes" : "No"}
        </div>
      `
    });

    google.maps.event.addListener(circle, "click", event => {
      infowindow.setPosition(event.latLng);
      infowindow.open(map);
    });

    airCircles.push(circle);
  })
}

// Function to get color based on quality
const getColorForQuality = quality => {
  const hue = (1 - quality / 500) * 120;
  return `hsl(${hue}, 100%, 50%)`;
}

// Function to remove all circles from the map
const removeCircles = () => {
  airCircles.forEach(circle => {
    circle.setMap(null);
  });
  airCircles.length = 0;
}
