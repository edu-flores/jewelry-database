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
  message = "";
  username = '';
  password = '';
  loading = false;

  constructor(private authService: AuthService, private router: Router) {}

  // Make a request to the auth service in the backend
  signIn(): void {
    this.loading = true;

    this.authService.signIn(this.username, this.password).subscribe(
      (response) => {
        localStorage.setItem('accessToken', response.token);
        this.router.navigate(['/map']);
      },
      (error) => {
        console.log("pensdf");
        
        console.error('Authentication failed', error);
        this.loading = false;
      }
    );
  }
}
