import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CommonService {

  constructor() { }

  public loadAgencyList() {}

  public loadHotelsList() {}

  public loadAgencyPartner(hotel : string) {}
}
