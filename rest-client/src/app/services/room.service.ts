import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, forkJoin } from 'rxjs';
import { Room, RoomFilters } from '../models/room';
import { Agency } from '../models/agency';
import { AgencyService } from './agency.service';



@Injectable({
  providedIn: 'root',
})
export class RoomService {
  constructor(private http: HttpClient, private agencyService: AgencyService) { }

  private getRoomsFromAgency(agency: Agency, filters: RoomFilters): Observable<Room[]> {
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

    // Include agency name in the rooms fetched
    return new Observable(observer => {
      this.http.get<Room[]>(`${agency.url}/rooms`, { params }).subscribe({
        next: (rooms) => {
          const roomsWithAgency = rooms.map(room => ({ ...room, agency: agency.name }));
          observer.next(roomsWithAgency);
          observer.complete();
        },
        error: (error) => {
          observer.error(error);
        },
      });
    });
  }

  public fetchRooms(filters: RoomFilters): Observable<Room[]> {
    // Create an array of observables for all agency URLs
    const agencyRequests = this.agencyService.getAgencies().map(agency =>
      this.getRoomsFromAgency(agency, filters)
    );

    // Use forkJoin to send the requests concurrently and combine the results
    return new Observable(observer => {
      forkJoin(agencyRequests).subscribe({
        next: (responses) => {
          // Merge all room responses from different agencies
          const allRooms = responses.flat();

          // Create a map to store the cheapest room for each unique room (by id)
          const roomMap = new Map<string, Room>();

          // Iterate through all rooms and update the map with the cheaper room
          allRooms.forEach(room => {
            if (!roomMap.has(room.id) || room.price < roomMap.get(room.id)?.price!) {
              roomMap.set(room.id, room);
            }
          });

          // Get the values from the map (this will be the unique rooms with the cheapest options)
          const uniqueRooms = Array.from(roomMap.values());
          observer.next(uniqueRooms);
          observer.complete();
        },
        error: (error) => {
          observer.error('Failed to fetch rooms from agencies. Please try again later.');
        }
      });
    });
  }
}
