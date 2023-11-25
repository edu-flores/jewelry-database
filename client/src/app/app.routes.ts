import { Routes } from '@angular/router';
import { MapPageComponent } from './map-page/map-page.component';
import { RoutesPageComponent } from './routes-page/routes-page.component';
import { RoutesFormComponent } from './routes-form/routes-form.component';
import { TrucksPageComponent } from './trucks-page/trucks-page.component';
import { TrucksFormComponent } from './trucks-form/trucks-form.component';
import { DataPageComponent } from './data-page/data-page.component';
import { SignInComponent } from './sign-in/sign-in.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { AuthGuard } from './auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: '/map', pathMatch: 'full' },
  { path: 'map', component: MapPageComponent, canActivate: [AuthGuard] },
  { path: 'routes', component: RoutesPageComponent, canActivate: [AuthGuard] },
  { path: 'routes-form', component: RoutesFormComponent, canActivate: [AuthGuard] },
  { path: 'trucks', component: TrucksPageComponent, canActivate: [AuthGuard] },
  { path: 'trucks-form', component: TrucksFormComponent, canActivate: [AuthGuard] },
  { path: 'data', component: DataPageComponent, canActivate: [AuthGuard] },
  { path: 'signin', component: SignInComponent },
  { path: 'signup', component: SignUpComponent },
  { path: '**', redirectTo: '/map' }
];
