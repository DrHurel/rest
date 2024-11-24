import { ChangeDetectionStrategy, Component, HostListener, OnInit, inject, signal } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormControl } from '@angular/forms';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

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
import { state } from '@angular/animations';

interface Room {
  id: string;
  name: string;
  size: number;
  price: number;
  beds: number;
}

type RoomsResponse = Room[];


interface RoomFilters {
  startDate?: string;
  endDate?: string;
  minsize?: number;
  minprize?: number;
  maxprice?: number;
  beds?: number;
}

const API_URL = 'http://localhost:5555/api/v1';

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
  private http = inject(HttpClient);
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

  getRooms(filters: RoomFilters): Observable<RoomsResponse> {
    let params = new HttpParams();

    if (filters.startDate) {
      params = params.set('start-date', filters.startDate);
    }
    if (filters.endDate) {
      params = params.set('end-date', filters.endDate);
    }
    if (filters.minsize) {
      params = params.set('minsize', filters.minsize.toString());
    }
    if (filters.minprize) {
      params = params.set('minprize', filters.minprize.toString());
    }
    if (filters.maxprice) {
      params = params.set('maxprice', filters.maxprice.toString());
    }
    if (filters.beds) {
      params = params.set('beds', filters.beds.toString());
    }

    let res;

    res = this.http.get<RoomsResponse>(`${API_URL}/rooms`, { params });
    console.log(res)
    return res;
  }

  fetchRooms() {

    this.error = null;

    const filters: RoomFilters = {
      beds: this.searchForm.get('beds')?.value || undefined,
      startDate: this.searchForm.get('checkin')?.value?.toISOString() || undefined,
      endDate: this.searchForm.get('checkout')?.value?.toISOString() || undefined,
      minprize: this.searchForm.get('minPrice')?.value || undefined,
      maxprice: this.searchForm.get('maxPrice')?.value || undefined,
      minsize: this.searchForm.get('minSize')?.value || undefined
    };

    this.getRooms(filters).subscribe({
      next: (response) => {
        this.rooms.update(() => response);
        this.totalRooms.update(() => response.length);
        this.isLoading.update(() => false);
      },
      error: (error) => {
        this.error = 'Failed to fetch rooms. Please try again later.';
        this.isLoading.update(() => false);
        console.error('Error fetching rooms:', error);
      }
    });
  }

  search() {
    this.isLoading.update(() => true)
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