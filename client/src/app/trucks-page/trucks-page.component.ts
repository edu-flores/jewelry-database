import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-trucks-page',
  standalone: true,
  imports: [
    CommonModule,
    NavbarComponent
  ],
  templateUrl: './trucks-page.component.html',
  styleUrl: './trucks-page.component.scss'
})
export class TrucksPageComponent {

}
