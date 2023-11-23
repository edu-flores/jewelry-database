import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = 'http://localhost:5001';

  constructor(private http: HttpClient, private router: Router) {}

  signIn(username: string, password: string): Observable<any> {
    const credentials = { username, password };
    return this.http.post<any>(`${this.apiUrl}/check-auth`, credentials);
  }

  signOut(): void {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('name');
    localStorage.removeItem('last');
    localStorage.removeItem('admin');
    this.router.navigate(['/signin']);
  }

  isAuthenticated(): boolean {
    const accessToken = localStorage.getItem('accessToken');
    const expirationDate = localStorage.getItem('expires');

    if (!accessToken || !expirationDate) {
      return false;
    }

    return new Date() <= new Date(expirationDate);
  }
}
