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
      { label: 'Mapa en Tiempo Real', icon: 'pi pi-fw pi-map', command: () => { this.router.navigate(['/map']) } },
      { label: 'Rutas de la Empresa', icon: 'pi pi-fw pi-arrows-h', command: () => { this.router.navigate(['/routes']) } },
      { label: 'Camiones de la Empresa', icon: 'pi pi-fw pi-truck', command: () => { this.router.navigate(['/trucks']) } },
      { label: 'Análisis de Datos', icon: 'pi pi-fw pi-chart-bar', command: () => { this.router.navigate(['/data']) } },
      { label: 'Cerrar Sesión', icon: 'pi pi-fw pi-sign-out', command: () => { this.authService.signOut() } }
    ];
  }
}
