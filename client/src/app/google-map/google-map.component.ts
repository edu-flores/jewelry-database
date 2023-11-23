import { Component, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { WebsocketService } from '../websocket.service';

interface Truck {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
}

interface Record {
  id: number;
  latitude: number;
  longitude: number;
  quality: number;
  contaminants: number;
}

@Component({
  selector: 'app-google-map',
  standalone: true,
  imports: [
    CommonModule
  ],
  templateUrl: './google-map.component.html',
  styleUrl: './google-map.component.scss'
})
export class GoogleMapComponent implements AfterViewInit {
  constructor(private http: HttpClient, private websocketService: WebsocketService) { }

  @ViewChild('mapContainer', { static: false }) gmap!: ElementRef;
  map: google.maps.Map | undefined;
  truckMarkers: { [key: number]: google.maps.Marker } = {};
  airCircles: google.maps.Circle[] = [];
  timer: any;

  ngAfterViewInit() {
    // Set up the map
    this.map = new google.maps.Map(this.gmap.nativeElement, {
      center: { lat: 25.687, lng: -100.318 },
      zoom: 11
    });

    // Call GPS API service
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
    });

    this.http.get<any>('http://localhost:5002/get-locations', { headers }).subscribe(
      (response) => {
        console.log('Data from API:', response);
        this.placeLocations(response);
      },
      (error) => {
        console.error('Error fetching data:', error);
      }
    );

    // Send update signals every 3 seconds
    this.timer = setInterval(() => {
      this.websocketService.sendUpdate();
    }, 3000)

    // Update markers in real time
    this.websocketService.getUpdates().subscribe(({ trucks, air }) => {
      trucks.forEach((truck: Truck) => {
        const marker = this.truckMarkers[truck.id];
        const newPosition = new google.maps.LatLng(truck.latitude, truck.longitude);
        marker.setPosition(newPosition);
      });
      this.removeCircles();
      air.forEach((record: Record) => {
        const circle = new google.maps.Circle({
          map: this.map,
          fillColor: this.getColorForQuality(record.quality),
          fillOpacity: 0.15,
          strokeOpacity: 0,
          center: { lat: record.latitude, lng: record.longitude },
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
          infowindow.open(this.map);
        });
        this.airCircles.push(circle);
      })
    });
  }

  // Place locations on the map
  private placeLocations = (response: any) => {
    // Company trucks
    response.trucks.forEach((truck: Truck) => {
      const marker = new google.maps.Marker({
        position: { lat: truck.latitude, lng: truck.longitude },
        map: this.map,
        title: `Ubicación del Camión: ${truck.name}`
      });
      const infowindow = new google.maps.InfoWindow({
        content: `
          <div style="font-size: 14px; color: #333;">
            <strong>Camión:</strong> ${truck.name}<br>
          </div>
        `
      });
      marker.addListener("click", () => {
        infowindow.open(this.map, marker);
      });
      this.truckMarkers[truck.id] = marker;
    });

    // Air quality
    response.air.forEach((record: Record) => {
      const circle = new google.maps.Circle({
        map: this.map,
        fillColor: this.getColorForQuality(record.quality),
        fillOpacity: 0.15,
        strokeOpacity: 0,
        center: { lat: record.latitude, lng: record.longitude },
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
        infowindow.open(this.map);
      });
      this.airCircles.push(circle);
    })
  }

  // Function to get color based on quality
  private getColorForQuality = (quality: number) => {
    const hue = (1 - quality / 500) * 120;
    return `hsl(${hue}, 100%, 50%)`;
  }

  // Function to remove all circles from the map
  private removeCircles = () => {
    this.airCircles.forEach(circle => {
      circle.setMap(null);
    });
    this.airCircles.length = 0;
  }
}
