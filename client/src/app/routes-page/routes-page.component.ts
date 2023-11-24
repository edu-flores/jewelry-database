import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../navbar/navbar.component';
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
}

@Component({
  selector: 'app-routes-page',
  standalone: true,
  imports: [CommonModule, NavbarComponent, CrudTableComponent],
  templateUrl: './routes-page.component.html',
  styleUrl: './routes-page.component.scss',
})
export class RoutesPageComponent {
  constructor(private http: HttpClient) {}

  // Props passed to CrudTable
  responseData: ResponseData = {
    error: false,
    routes: [],
  };
  tableHeaders: TableHeader[] = [
    {
      field: 'id',
      title: 'ID',
    },
    {
      field: 'name',
      title: 'Nombre',
    },
    {
      field: 'distance',
      title: 'Distancia',
    },
    {
      field: 'active',
      title: 'Estado',
    },
    {
      field: 'averageSpeed',
      title: 'Velocidad (x̅)',
    },
    {
      field: 'time',
      title: 'Tiempo',
    },
    {
      field: 'truckName',
      title: 'Camión',
    },
  ];

  ngOnInit() {
    // Call Routes API service
    const headers = new HttpHeaders({
      Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
    });

    this.http
      .get('http://localhost:5003/retrieve-routes', { headers })
      .subscribe(
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
