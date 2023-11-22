import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { HttpClient } from '@angular/common/http';
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

  constructor(private http: HttpClient, private router: Router) {}

  // Make a request to the auth service in the backend
  signUp(): void {
    this.loading = true;

    const userData = {
      name: this.name,
      lastname: this.lastname,
      username: this.username,
      password: this.password
    };

    this.http.post('http://localhost:5001/new-user', userData).subscribe(
      (response) => {
        this.message = "Cuenta creada con éxito, inicie sesión";
        this.loading = false;
      },
      (error) => {
        console.error('Error creating user', error);
        this.loading = false;
        if (error.status === 409) {
          this.message = 'El usuario ya existe';
        } else {
          this.message = 'Error al crear el usuario';
        }
      }
    );
  }

  // Navigate to the signin page
  navigateToSignIn(): void {
    this.router.navigate(['/signin']);
  }
}
