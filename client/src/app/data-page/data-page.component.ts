import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../navbar/navbar.component';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MessageService } from 'primeng/api';
import { ToastModule } from 'primeng/toast';
import { ChartModule } from 'primeng/chart';

@Component({
  selector: 'app-data-page',
  standalone: true,
  imports: [
    CommonModule,
    NavbarComponent,
    ToastModule,
    ChartModule
  ],
  templateUrl: './data-page.component.html',
  styleUrl: './data-page.component.scss'
})
export class DataPageComponent {
  // Charts
  doughnutData: any;
  linesData: any;
  barsData: any;

  constructor(private http: HttpClient, private messageService: MessageService) {}

  // Get all the data from the API
  ngOnInit() {
    const headers = new HttpHeaders({
      Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
    });
    this.http.get('http://localhost:5004/get-conditions', { headers: headers }).subscribe(
      (response: any) => {
        console.log('Data from API:', response);

        // Warnings
        if (response.warning) {
          this.showWarnings();
        }

        // Charts
        this.setDoughnutData(response.ambient.trucksCO2);
        this.setLinesData(response.ambient.samplesData);
        this.setBarsData({ short: response.ambient.shortLongStops.short, long: response.ambient.shortLongStops.long });
      },
      (error) => {
        console.error('Error fetching data:', error);
      }
    );
  }

  // Show warnings
  private showWarnings() {
    this.messageService.add({
      severity: 'warn',
      summary: 'Alerta',
      detail: 'Emisiones altas de CO2',
      sticky: true
    });
    this.messageService.add({
      severity: 'info',
      summary: 'Aviso',
      detail: 'Es necesario reducir la producción de CO2',
      sticky: true
    });
  }

  // Charts data
  private setDoughnutData(data: any) {
    this.doughnutData = {
      labels: data.map((truck: any) => truck.name),
      datasets: [
        {
          data: data.map((truck: any) => truck.totalCO2),
        },
      ],
    }
  }
  private setLinesData(data: any) {
    console.log(data);
    this.linesData = {
      labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
      datasets: [
        {
          label: 'Distancia (Cientos de Km)',
          data: data.map((record: any) => record.distance / 100),
          fill: true,
          borderDash: [3, 3],
        },
        {
          label: 'Velocidad Promedio',
          data: data.map((record: any) => record.speed),
          fill: false
        }
      ]
    }
  }
  private setBarsData({ short, long }: any) {
    this.barsData = {
      labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
      datasets: [
        {
          label: 'Paradas Cortas',
          backgroundColor: '#42A5F5',
          data: short.map((record: any) => record.count)
        },
        {
          label: 'Paradas largas',
          backgroundColor: '#9CCC65',
          data: long.map((record: any) => record.count)
        }
      ]
    }
  }
}
