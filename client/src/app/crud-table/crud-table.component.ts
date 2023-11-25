import { Component, ViewChild, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InputTextModule } from 'primeng/inputtext';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';
import { ButtonModule } from 'primeng/button';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ConfirmationService } from 'primeng/api';

interface Route {
  id: number;
  name: string;
  distance: number;
  active: number;
  averageSpeed: number;
  time: string;
  truckName: string;
}

interface TableHeader {
  field: string;
  title: string;
  units: string;
}

@Component({
  selector: 'app-crud-table',
  standalone: true,
  imports: [
    CommonModule,
    InputTextModule,
    TableModule,
    TagModule,
    ButtonModule,
    ConfirmDialogModule
  ],
  templateUrl: './crud-table.component.html',
  styleUrl: './crud-table.component.scss'
})
export class CrudTableComponent {
  constructor(private confirmationService: ConfirmationService) {}

  // Table
  @ViewChild('dt') dt: any;

  // Props
  @Input() filterFields: string[] = [];
  @Input() items: string = '';
  @Input() routes: Route[] = [];
  @Input() headers: TableHeader[] = [];

  // Events
  @Output() editClicked = new EventEmitter<any>();
  @Output() deleteClicked = new EventEmitter<any>();
  @Output() jsonClicked = new EventEmitter<any>();
  @Output() xmlClicked = new EventEmitter<any>();

  // Filtering table
  applyFilterGlobal($event: any, val: any) {
    this.dt!.filterGlobal(($event.target as HTMLInputElement).value, val);
  }

  // Handle CRUD actions
  onEditClick(item: any) {
    this.editClicked.emit(item);
  }
  onDeleteClick(item: any) {
    this.confirmationService.confirm({
      message: '¿Seguro que deseas eliminar este item?',
      accept: () => {
        this.deleteClicked.emit(item);
      }
    });
  }
  onJsonClick(item: any) {
    this.jsonClicked.emit(item);
  }
  onXmlClick(item: any) {
    this.xmlClicked.emit(item);
  }
}
