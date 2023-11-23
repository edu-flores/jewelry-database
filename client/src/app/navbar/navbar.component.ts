import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TabMenuModule } from 'primeng/tabmenu';
import { Router } from '@angular/router';
import { MenuItem } from 'primeng/api';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    CommonModule,
    TabMenuModule
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {
  items: MenuItem[];

  constructor(private authService: AuthService, private router: Router) {
    this.items = [
      {
        label: 'Mapa en Tiempo Real',
        icon: 'pi pi-fw pi-map',
        routerLink: '/map',
        command: () => {
          this.router.navigate(['/map']);
        },
      },
      {
        label: 'Rutas de la Empresa',
        icon: 'pi pi-fw pi-arrows-h',
        routerLink: '/routes',
        command: () => {
          this.router.navigate(['/routes']);
        },
      },
      {
        label: 'Camiones de la Empresa',
        icon: 'pi pi-fw pi-truck',
        routerLink: '/trucks',
        command: () => {
          this.router.navigate(['/trucks']);
        },
      },
      {
        label: 'Análisis de Datos',
        icon: 'pi pi-fw pi-chart-bar',
        routerLink: '/data',
        command: () => {
          this.router.navigate(['/data']);
        },
      },
      {
        label: `${localStorage.getItem('name')} ${localStorage.getItem('last')}`,
        style: { "margin-left": "auto" },
        icon: 'pi pi-fw pi-sign-out',
        routerLink: '/signin',
        command: () => {
          this.authService.signOut();
        },
      },
    ];
  }
}
