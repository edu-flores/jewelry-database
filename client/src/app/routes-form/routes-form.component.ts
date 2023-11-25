import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { InputNumberModule } from 'primeng/inputnumber';
import { DropdownModule } from 'primeng/dropdown';
import { ButtonModule } from 'primeng/button';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';

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
  name = null;
  distance = null;
  time = null;
  speed = null;
  active = null;
  truck = null;
  message = '';
  loading = false;

  constructor(private http: HttpClient, private router: Router) {}
  trucks: any[] = [];
  headers = new HttpHeaders({
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  });

  ngOnInit() {
    // Call Trucks API service
    this.http.get('http://localhost:5004/retrieve-trucks', { headers: this.headers }).subscribe(
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
      .post('http://localhost:5003/add-route', {
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
