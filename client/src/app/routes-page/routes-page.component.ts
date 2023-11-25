import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../navbar/navbar.component';
import { MessagesModule } from 'primeng/messages';
import { Message } from 'primeng/api';
import { CrudTableComponent } from '../crud-table/crud-table.component';
import { HttpClient, HttpHeaders } from '@angular/common/http';

interface Route {
  id: number;
  name: string;
  distance: number;
  active: number;
  averageSpeed: number;
  time: string;
  truckName: string;
}

interface ResponseData {
  error: boolean;
  routes: Route[];
}

interface TableHeader {
  field: string;
  title: string;
  units: string;
}

@Component({
  selector: 'app-routes-page',
  standalone: true,
  imports: [
    CommonModule,
    NavbarComponent,
    MessagesModule,
    CrudTableComponent
  ],
  templateUrl: './routes-page.component.html',
  styleUrl: './routes-page.component.scss',
})
export class RoutesPageComponent {
  constructor(private http: HttpClient) {}
  messages: Message[] = []
  headers = new HttpHeaders({
    Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
  });

  // Props passed to CrudTable
  responseData: ResponseData = {
    error: false,
    routes: [],
  };
  tableHeaders: TableHeader[] = [
    { field: 'id', title: 'ID', units: '' },
    { field: 'name', title: 'Nombre', units: '' },
    { field: 'distance', title: 'Distancia', units: 'km' },
    { field: 'active', title: 'Estado', units: '' },
    { field: 'averageSpeed', title: 'Velocidad (x̅)', units: 'km/h' },
    { field: 'time', title: 'Tiempo', units: 'min' },
    { field: 'truckName', title: 'Camión', units: '' },
  ];

  // Call Routes API service
  ngOnInit() {
    this.getRoutes();
  }

  // Handle CRUD actions
  onAddClick() {
    console.log('Add clicked');
  }
  onEditClick(route: Route) {
    console.log('Edit clicked for route:', route);
  }
  onDeleteClick(route: Route) {
    this.http.post('http://localhost:5003/delete-route', { id: route.id }, { headers: this.headers }).subscribe(
      (response: any) => {
        console.log('Data from API:', response);
        this.getRoutes();
        this.messages = [{
          severity: 'success',
          summary: 'Éxito',
          detail: 'Ruta eliminada',
        }];
      },
      (error) => {
        console.error('Error:', error);
        this.messages = [{
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudo eliminar la ruta',
        }]
      }
    );
  }
  onJsonClick(route: Route) {
    window.open(`http://localhost:5003/retrieve-json?id=${route.id}`, '_blank');
  }
  onXmlClick(route: Route) {
    window.open(`http://localhost:5003/retrieve-xml?id=${route.id}`, '_blank');
  }

  // API
  private getRoutes() {
    this.http.get('http://localhost:5003/retrieve-routes', { headers: this.headers }).subscribe(
      (response: any) => {
        console.log('Data from API:', response);
        this.responseData = response;
      },
      (error) => {
        console.error('Error fetching data:', error);
      }
    );
  }
}
