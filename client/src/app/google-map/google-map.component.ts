import { Component, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';

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
  constructor(private http: HttpClient) { }

  @ViewChild('mapContainer', { static: false }) gmap!: ElementRef;
  map: google.maps.Map | undefined;

  // Get truck's locations and air quality data from the GPS service
  ngOnInit() {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
    });

    this.http.get<any>('http://localhost:5002/get-locations', { headers }).subscribe(
      (response) => {
        console.log('Data from API:', response);
      },
      (error) => {
        console.error('Error fetching data:', error);
      }
    );
  }

  ngAfterViewInit() {
    this.map = new google.maps.Map(this.gmap.nativeElement, {
      center: { lat: 25.687, lng: -100.318 },
      zoom: 11
    });
  }
}
