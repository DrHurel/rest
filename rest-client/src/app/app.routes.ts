import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { BookingComponent } from './pages/booking/booking.component';

export const routes: Routes = [
  { path: 'booking/:roomId/:agency', component: BookingComponent },
  { path: "", component: HomeComponent }
];
