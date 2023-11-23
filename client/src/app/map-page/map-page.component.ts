import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../navbar/navbar.component';
import { GoogleMapComponent } from '../google-map/google-map.component';
import { PurchasesTableComponent } from '../purchases-table/purchases-table.component';

@Component({
  selector: 'app-map-page',
  standalone: true,
  imports: [
    CommonModule,
    NavbarComponent,
    GoogleMapComponent,
    PurchasesTableComponent
  ],
  templateUrl: './map-page.component.html',
  styleUrl: './map-page.component.scss'
})
export class MapPageComponent {

}
