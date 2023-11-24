import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InputTextModule } from 'primeng/inputtext';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';
import { ButtonModule } from 'primeng/button';

interface Route {
  id: number;
  name: string;
  distance: number;
  active: number;
  averageSpeed: number;
  time: string;
  truckName: string;
}

@Component({
  selector: 'app-crud-table',
  standalone: true,
  imports: [
    CommonModule,
    InputTextModule,
    TableModule,
    TagModule,
    ButtonModule
  ],
  templateUrl: './crud-table.component.html',
  styleUrl: './crud-table.component.scss'
})
export class CrudTableComponent {
  @Input() routes: Route[] = [];
}
