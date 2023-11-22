import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sign-up',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    InputTextModule,
    ButtonModule
  ],
  templateUrl: './sign-up.component.html',
  styleUrl: './sign-up.component.scss'
})
export class SignUpComponent {
  message = '';
  name = '';
  lastname = '';
  username = '';
  password = '';
  loading = false;

  constructor(private router: Router) {}

  // Make a request to the auth service in the backend
  signUp(): void {
    this.loading = true;
  }

  // Navigate to the signup page
  navigateToSignIn(): void {
    this.router.navigate(['/signin']);
  }
}
