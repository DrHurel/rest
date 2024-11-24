import { CommonModule, DatePipe } from '@angular/common';
import { Component, EventEmitter, inject, Output, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatNativeDateModule } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { MatToolbarModule } from '@angular/material/toolbar';
import { Room, RoomFilters } from '../../models/room';
import { RoomService } from '../../services/room.service';

@Component({
  selector: 'app-search-bar',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatCardModule,
    MatGridListModule,
    MatPaginatorModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './search-bar.component.html',
  styleUrl: './search-bar.component.scss'
})
export class SearchBarComponent {
  searchForm = new FormGroup({
    search: new FormControl(''),
    beds: new FormControl<number | null>(null),
    checkin: new FormControl<Date | null>(null),
    checkout: new FormControl<Date | null>(null),
    minPrice: new FormControl<number | null>(null),
    maxPrice: new FormControl<number | null>(null),
    minSize: new FormControl<number | null>(null)
  });

  private roomService = inject(RoomService);

  @Output()
  rooms = new EventEmitter<Array<Room>>(); // EventEmitter to handle booking action


  isLoading = signal<boolean>(false);
  error: string | null = null;


  ngOnInit() {
    this.fetchRooms();
  }

  fetchRooms() {
    this.isLoading.update(() => true);
    this.error = null;

    const filters: RoomFilters = {
      beds: this.searchForm.get('beds')?.value || undefined,
      startDate: this.searchForm.get('checkin')?.value?.toISOString() || undefined,
      endDate: this.searchForm.get('checkout')?.value?.toISOString() || undefined,
      minprize: this.searchForm.get('minPrice')?.value || undefined,
      maxprice: this.searchForm.get('maxPrice')?.value || undefined,
      minsize: this.searchForm.get('minSize')?.value || undefined
    };

    // Fetch rooms using RoomService
    this.roomService.fetchRooms(filters).subscribe({
      next: (response) => {
        this.rooms.emit(response);

        this.isLoading.update(() => false);
      },
      error: (error) => {
        this.error = error;
        this.isLoading.update(() => false);
        console.error('Error fetching rooms:', error);
      }
    });
  }

  search() {
    this.isLoading.update(() => true);
    this.fetchRooms();
  }


}
