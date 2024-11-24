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
import { Room, RoomFilters } from '../../models/room';
import { RoomCardComponent } from "../../components/room-card/room-card.component";
import { SearchBarComponent } from "../../components/search-bar/search-bar.component";





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
    RoomCardComponent,
    SearchBarComponent
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
  roomList: any;

  ngOnInit() {
    this.adjustColumns(window.innerWidth);
  }

  roomsUpdate(data: Array<Room>) {

    console.log(data)
    this.rooms.update(() => data)
  }



  onPageChange(event: PageEvent) {
    this.pageSize = event.pageSize;
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
