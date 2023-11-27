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
  data: any;
  options: any;
  constructor(private messageService: MessageService) {
    setTimeout(() => {
      this.messageService.add({
        severity: 'warn',
        summary: 'Alerta',
        detail: 'Emisiones altas de CO2'
      });
      this.messageService.add({
        severity: 'info',
        summary: 'Aviso',
        detail: 'Es necesario reducir la producción de CO2'
      });
    }, 300);


    this.data = {
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [
        {
          label: 'First Dataset',
          data: [65, 59, 80, 81, 56, 55, 40],
        },
        {
          label: 'Second Dataset',
          data: [28, 48, 40, 19, 86, 27, 90],
        },
      ],
    };
  }
}
