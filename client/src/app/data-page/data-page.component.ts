import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../navbar/navbar.component';
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

  constructor(private messageService: MessageService) {
    // Warnings
    setTimeout(() => {
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
    }, 300);

    // Chart settings
    this.doughnutData = {
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [
        {
          data: [65, 59, 80, 81, 56, 55, 40],
        },
      ],
    }
    this.linesData = {
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [
        {
          label: 'First Dataset',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
        },
        {
          label: 'Second Dataset',
          data: [28, 48, 40, 19, 86, 27, 90],
          fill: false,
          borderDash: [5, 5],
        },
        {
          label: 'Third Dataset',
          data: [12, 51, 62, 33, 21, 62, 45],
          fill: true,
        }
      ]
    }
    this.barsData = {
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [
        {
          label: 'My First dataset',
          backgroundColor: '#42A5F5',
          data: [65, 59, 80, 81, 56, 55, 40]
        },
        {
          label: 'My Second dataset',
          backgroundColor: '#9CCC65',
          data: [28, 48, 40, 19, 86, 27, 90]
        }
      ]
    }
  }
}
