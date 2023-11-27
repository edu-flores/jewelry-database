import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../navbar/navbar.component';
import { MessagesModule } from 'primeng/messages';
import { Message } from 'primeng/api';
import { CrudTableComponent } from '../crud-table/crud-table.component';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';

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

interface ResponseData {
  error: boolean;
  trucks: Truck[];
}

interface TableHeader {
  field: string;
  title: string;
  units: string;
}

@Component({
  selector: 'app-trucks-page',
  standalone: true,
  imports: [
    CommonModule,
    NavbarComponent,
    MessagesModule,
    CrudTableComponent
  ],
  templateUrl: './trucks-page.component.html',
  styleUrl: './trucks-page.component.scss'
})
export class TrucksPageComponent {
  constructor(private http: HttpClient, private router: Router) {}
  messages: Message[] = []
  headers = new HttpHeaders({
    Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
  });
  loading = true;

  // Props passed to CrudTable
  responseData: ResponseData = {
    error: false,
    trucks: [],
  };
  tableHeaders: TableHeader[] = [
    { field: 'id', title: 'ID', units: '' },
    { field: 'name', title: 'Nombre', units: '' },
    { field: 'totalDistance', title: 'Distancia Total', units: 'km' },
    { field: 'averageTripDistance', title: 'Distancia (x̅)', units: 'km' },
    { field: 'totalCO2', title: 'CO2 Total', units: 'g' },
    { field: 'averageCO2', title: 'CO2 (x̅)', units: 'g' },
    { field: 'latitude', title: 'Latitud', units: '' },
    { field: 'longitude', title: 'Longitud', units: '' },
  ];

  // Call Routes API service
  ngOnInit() {
    this.getTrucks();
  }

  // Handle CRUD actions
  onAddClick() {
    this.router.navigate(['trucks-form'], { state: { route: null } });
  }
  onEditClick(truck: Truck) {
    this.router.navigate(['trucks-form'], { state: { route: truck } });
  }
  onDeleteClick(truck: Truck) {
    this.http.post('http://localhost:5004/delete-truck', { id: truck.id }, { headers: this.headers }).subscribe(
      (response: any) => {
        console.log('Data from API:', response);
        this.getTrucks();
        this.messages = [{
          severity: 'success',
          summary: 'Éxito',
          detail: 'Camión eliminada',
        }];
      },
      (error) => {
        console.error('Error:', error);
        this.messages = [{
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudo eliminar el camión',
        }]
      }
    );
  }
  onJsonClick(truck: Truck) {
    window.open(`http://localhost:5004/retrieve-json?id=${truck.id}`, '_blank');
  }
  onXmlClick(truck: Truck) {
    window.open(`http://localhost:5004/retrieve-xml?id=${truck.id}`, '_blank');
  }

  // API
  private getTrucks() {
    this.loading = true;
    this.http.get('http://localhost:5004/retrieve-trucks', { headers: this.headers }).subscribe(
      (response: any) => {
        console.log('Data from API:', response);
        this.responseData = response;
        this.loading = false;
      },
      (error) => {
        console.error('Error fetching data:', error);
        this.loading = false;
      }
    );
  }
}
