import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sign-in',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    InputTextModule,
    ButtonModule
  ],
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.scss'
})
export class SignInComponent {
  message = '';
  username = '';
  password = '';
  loading = false;

  constructor(private authService: AuthService, private router: Router) {}

  // Make a request to the auth service in the backend
  signIn(): void {
    this.loading = true;

    this.authService.signIn(this.username, this.password).subscribe(
      (response) => {
        // Set user data
        localStorage.setItem('accessToken', response.token);
        localStorage.setItem('name', response.name);
        localStorage.setItem('last', response.last);
        localStorage.setItem('admin', response.admin == 1 ? 'true' : 'false');

        this.router.navigate(['/map']);
      },
      (error) => {
        console.error('Authentication failed', error);
        this.loading = false;

        if (error.status === 401) {
          this.message = 'Credenciales incorrectas';
        } else {
          this.message = 'Error de autenticación';
        }
      }
    );
  }

  // Navigate to the signup page
  navigateToSignUp(): void {
    this.router.navigate(['/signup']);
  }
}
