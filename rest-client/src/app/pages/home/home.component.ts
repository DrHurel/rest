import { ChangeDetectionStrategy, Component, HostListener, OnInit, inject, signal } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormControl } from '@angular/forms';
import { RoomService } from '../../services/room.service'; // Import the RoomService

// Material Imports
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule, provideNativeDateAdapter } from '@angular/material/core';
import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { Room } from '../../models/room';



interface RoomFilters {
  startDate?: string;
  endDate?: string;
  minsize?: number;
  minprize?: number;
  maxprice?: number;
  beds?: number;
}

@Component({
  selector: 'app-home',
  standalone: true,
  providers: [provideNativeDateAdapter(), DatePipe],
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
    MatProgressSpinnerModule,
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  private roomService = inject(RoomService);
  private datePipe = inject(DatePipe);

  searchForm = new FormGroup({
    search: new FormControl(''),
    beds: new FormControl<number | null>(null),
    checkin: new FormControl<Date | null>(null),
    checkout: new FormControl<Date | null>(null),
    minPrice: new FormControl<number | null>(null),
    maxPrice: new FormControl<number | null>(null),
    minSize: new FormControl<number | null>(null)
  });

  rooms = signal<Room[]>([]);
  isLoading = signal<boolean>(false);
  error: string | null = null;

  totalRooms = signal<number>(0);
  pageSize = 8;
  cols = 4;

  ngOnInit() {
    this.adjustColumns(window.innerWidth);
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
        this.rooms.update(() => response);
        this.totalRooms.update(() => response.length);
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

  private formatDate(date: Date | null): string | undefined {
    if (!date) return undefined;
    return this.datePipe.transform(date, 'yyyy-MM-dd') || undefined;
  }

  onPageChange(event: PageEvent) {
    this.pageSize = event.pageSize;
    this.fetchRooms();
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: any) {
    this.adjustColumns(event.target.innerWidth);
  }

  private adjustColumns(width: number) {
    if (width <= 600) {
      this.cols = 1;
    } else if (width <= 960) {
      this.cols = 2;
    } else {
      this.cols = 4;
    }
  }
}
