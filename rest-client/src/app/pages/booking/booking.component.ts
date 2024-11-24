import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormControl, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { HttpClient } from '@angular/common/http';
import { AgencyService } from '../../services/agency.service';

@Component({
  selector: 'app-booking',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatDatepickerModule,
    MatNativeDateModule,
  ],
  templateUrl: './booking.component.html',
  styleUrls: ['./booking.component.scss'],
})
export class BookingComponent implements OnInit {
  roomId: string | null = null;
  agency: string | null = null;

  bookingForm = new FormGroup({
    startDate: new FormControl('', Validators.required),
    endDate: new FormControl('', Validators.required),
    name: new FormControl('', Validators.required),
  });

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private router: Router,
    private agencyService: AgencyService
  ) { }

  ngOnInit(): void {
    // Retrieve route parameters
    this.roomId = this.route.snapshot.paramMap.get('roomId');
    this.agency = this.route.snapshot.paramMap.get('agency');
  }

  submitBooking(): void {
    if (this.bookingForm.valid && this.roomId && this.agency) {
      const bookingData = {
        ...this.bookingForm.value,
        roomId: this.roomId,
      };

      const token = 'secret';

      this.http
        .post(
          `${this.agencyService.getAgencyUrl(this.agency)}/room/${this.roomId}/book`,
          bookingData,
          {
            params: { token },
          }
        )
        .subscribe({
          next: () => {
            alert('Booking successful!');
            this.router.navigate(['/']); // Redirect to the home page
          },
          error: (err) => {
            console.error('Booking failed', err);
            alert('Booking failed. Please try again.');
          },
        });
    }
  }
}
