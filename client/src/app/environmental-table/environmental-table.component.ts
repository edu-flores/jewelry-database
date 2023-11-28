import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TableModule } from 'primeng/table';

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
  @Input() data: any[] = [];
  months: string[] = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
}
