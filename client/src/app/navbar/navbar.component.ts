import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TabMenuModule } from 'primeng/tabmenu';

interface TabItem {
  label: string;
  icon: string;
}

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
  items: TabItem[];

  constructor() {
    this.items = [
      { label: 'Mapa en Tiempo Real', icon: 'pi pi-fw pi-map' },
      { label: 'Rutas de la Empresa', icon: 'pi pi-fw pi-arrows-h' },
      { label: 'Camiones de la Empresa', icon: 'pi pi-fw pi-truck' },
      { label: 'Análisis de Datos', icon: 'pi pi-fw pi-chart-bar' },
      { label: 'Cerrar sesión', icon: 'pi pi-fw pi-power-off' }
    ];
  }
}
