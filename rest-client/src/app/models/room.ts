export interface Room {
    id: string;
    name: string;
    size: number;
    price: number;
    beds: number;
    agency: string;
}

export interface RoomFilters {
    startDate?: string;
    endDate?: string;
    minsize?: number;
    minprize?: number;
    maxprice?: number;
    beds?: number;
}