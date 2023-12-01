import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';

interface Purchase {
  id: string;
  truck: string;
  status: string;
}

@Component({
  selector: 'app-purchases-table',
  standalone: true,
  imports: [
    CommonModule,
    TableModule,
    TagModule
  ],
  templateUrl: './purchases-table.component.html',
  styleUrl: './purchases-table.component.scss'
})
export class PurchasesTableComponent {
  constructor(private http: HttpClient) {}
  purchases: Purchase[] = [];
  loading = true;

  ngOnInit() {
    // Call GPS API service
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
    });

    this.http.get<any>('http://127.0.0.1:5002/get-purchases', { headers }).subscribe(
      (response) => {
        console.log('Data from API:', response);
        this.purchases = response.purchases;
        this.loading = false;
      },
      (error) => {
        console.error('Error fetching data:', error);
        this.loading = false;
      }
    );
  }
}
