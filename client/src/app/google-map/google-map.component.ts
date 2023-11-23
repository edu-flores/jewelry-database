import { Component, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';

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
  @ViewChild('mapContainer', { static: false }) gmap!: ElementRef;
  map: google.maps.Map | undefined;

  ngAfterViewInit() {
    this.map = new google.maps.Map(this.gmap.nativeElement, {
      center: { lat: 25.687, lng: -100.318 },
      zoom: 11
    });
  }
}
