import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { InputNumberModule } from 'primeng/inputnumber';
import { DropdownModule } from 'primeng/dropdown';
import { ButtonModule } from 'primeng/button';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

interface State {
  route: Route;
  navigationId: number;
}

interface Route {
  id: number;
  name: string;
  distance: number;
  active: number;
  averageSpeed: number;
  time: number;
  truckId: number;
  truckName: string;
}

interface Truck {
  id: number;
  name: string;
  totalDistance: number;
  totalCO2: number;
  averageTripDistance: number;
  averageCO2: number;
  latitude: number;
  longitude: number;
}

@Component({
  selector: 'app-routes-form',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    InputTextModule,
    InputNumberModule,
    DropdownModule,
    ButtonModule,
  ],
  templateUrl: './routes-form.component.html',
  styleUrl: './routes-form.component.scss',
})
export class RoutesFormComponent {
  id: number | null = null;
  name: string | null = null;
  distance: number | null = null;
  time: number | null = null;
  speed: number | null = null;
  active: number | null = null;
  truck: number | null = null;
  message = '';
  loading = false;

  // Determine if editing or adding
  constructor(private http: HttpClient, private router: Router, private location: Location) {
    console.log(location.getState());
    if ((location.getState() as State).route) {
      this.edit = true;
      const { route } = (location.getState() as State);
      this.id = route.id;
      this.name = route.name;
      this.distance = route.distance;
      this.time = route.time;
      this.speed = route.averageSpeed;
      this.active = route.active;
      this.truck = route.truckId;
    }
  }
  edit = false;
  trucks: Truck[] = [];
  headers = new HttpHeaders({
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  });

  ngOnInit() {
    // Call Trucks API service
    this.http.get('http://127.0.0.1:5004/retrieve-trucks', { headers: this.headers }).subscribe(
      (response: any) => {
        console.log('Data from API:', response);
        this.trucks = response.trucks;
      },
      (error) => {
        console.error('Error fetching data:', error);
      }
    )
  }

  // Add new route
  addRoute() {
    this.loading = true;
    this.http
      .post('http://127.0.0.1:5003/add-route', {
        name: this.name,
        distance: this.distance,
        time: this.time,
        averageSpeed: this.speed,
        active: this.active ?? 0,
        truckId: this.truck,
      }, { headers: this.headers }).subscribe(
        (response: any) => {
          console.log('Data from API:', response);
          this.message = response.message;
          this.loading = false;
          this.clearFields();
        },
        (error) => {
          console.error('Error:', error);
          this.message = 'Error al crear la ruta';
          this.loading = false;
        });
  }

  // Edit existing route
  editRoute() {
    this.loading = true;
    this.http
      .post('http://127.0.0.1:5003/edit-route', {
        id: this.id,
        name: this.name,
        distance: this.distance,
        time: this.time,
        averageSpeed: this.speed,
        active: this.active ?? 0,
        truckId: this.truck,
      }, { headers: this.headers }).subscribe(
        (response: any) => {
          console.log('Data from API:', response);
          this.message = response.message;
          this.loading = false;
        },
        (error) => {
          console.error('Error:', error);
          this.message = 'Error al editar la ruta';
          this.loading = false;
        });
  }

  // Reset all form fields
  private clearFields() {
    this.name = null;
    this.distance = null;
    this.time = null;
    this.speed = null;
    this.active = null;
    this.truck = null;
  }

  // Return to CRUD table page
  navigateToRoutes() {
    this.router.navigate(['/routes']);
  }
}
