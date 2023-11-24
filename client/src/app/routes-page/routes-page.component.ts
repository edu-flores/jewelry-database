import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../navbar/navbar.component';
import { CrudTableComponent } from '../crud-table/crud-table.component';

@Component({
  selector: 'app-routes-page',
  standalone: true,
  imports: [
    CommonModule,
    NavbarComponent,
    CrudTableComponent
  ],
  templateUrl: './routes-page.component.html',
  styleUrl: './routes-page.component.scss'
})
export class RoutesPageComponent {

}
