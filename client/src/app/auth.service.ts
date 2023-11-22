import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = 'http://localhost:5001';
  private accessToken = 'authToken';

  constructor(private http: HttpClient) {}

  signIn(username: string, password: string): Observable<any> {
    const credentials = { username, password };
    return this.http.post<any>(`${this.apiUrl}/check-auth`, credentials);
  }

  signOut(): void {
    localStorage.removeItem(this.accessToken);
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem(this.accessToken);
  }
}
