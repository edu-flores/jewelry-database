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
  truck: Truck;
  navigationId: number;
}

interface Truck {
  id: number;
  name: string;
  totalDistance: number;
  averageTripDistance: number;
  latitude: number;
  longitude: number;
}

@Component({
  selector: 'app-trucks-form',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    InputTextModule,
    InputNumberModule,
    DropdownModule,
    ButtonModule,
  ],
  templateUrl: './trucks-form.component.html',
  styleUrl: './trucks-form.component.scss'
})
export class TrucksFormComponent {
  id: number | null = null;
  name: string | null = null;
  totalDistance: number | null = null;
  averageTripDistance: number | null = null;
  latitude: number | null = null;
  longitude: number | null = null;
  message = '';
  loading = false;

  // Determine if editing or adding
  constructor(private http: HttpClient, private router: Router, private location: Location) {
    console.log(location.getState());
    if ((location.getState() as State).truck) {
      this.edit = true;
      const { truck } = (location.getState() as State);
      this.id = truck.id;
      this.name = truck.name;
      this.totalDistance = truck.totalDistance;
      this.averageTripDistance = truck.averageTripDistance;
      this.latitude = truck.latitude;
      this.longitude = truck.longitude;
    }
  }
  edit = false;
  headers = new HttpHeaders({
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  });

  // Add new truck
  addTruck() {
    this.loading = true;
    this.http
      .post('http://localhost:5004/add-truck', {
        name: this.name,
        totalDistance: this.totalDistance,
        averageTripDistance: this.averageTripDistance,
        latitude: this.latitude,
        longitude: this.longitude,
      }, { headers: this.headers }).subscribe(
        (response: any) => {
          console.log('Data from API:', response);
          this.message = response.message;
          this.loading = false;
          this.clearFields();
        },
        (error) => {
          console.error('Error:', error);
          this.message = 'Error al crear el camión';
          this.loading = false;
        });
  }

  // Edit existing routtruck
  editTruck() {
    this.loading = true;
    this.http
      .post('http://localhost:5004/edit-truck', {
        id: this.id,
        name: this.name,
        totalDistance: this.totalDistance,
        averageTripDistance: this.averageTripDistance,
        latitude: this.latitude,
        longitude: this.longitude,
      }, { headers: this.headers }).subscribe(
        (response: any) => {
          console.log('Data from API:', response);
          this.message = response.message;
          this.loading = false;
        },
        (error) => {
          console.error('Error:', error);
          this.message = 'Error al editar el camión';
          this.loading = false;
        });
  }

  // Reset all form fields
  private clearFields() {
    this.name = null;
    this.totalDistance = null;
    this.averageTripDistance = null;
    this.latitude = null;
    this.longitude = null;
  }

  // Return to CRUD table page
  navigateToTrucks() {
    this.router.navigate(['/trucks']);
  }
}
