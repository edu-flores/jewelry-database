import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TableModule } from 'primeng/table';

interface Record {
  time: string;
  temperature: number;
  humidity: number;
  precipitation: number;
  windSpeed: number;
  pressure: number;
}

@Component({
  selector: 'app-environmental-table',
  standalone: true,
  imports: [
    CommonModule,
    TableModule
  ],
  templateUrl: './environmental-table.component.html',
  styleUrl: './environmental-table.component.scss'
})
export class EnvironmentalTableComponent {
  @Input() data: Record[] = [];
  months: string[] = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
}
