import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="HotelBookRoomResponse200")


@_attrs_define
class HotelBookRoomResponse200:
    """
    Attributes:
        id (Union[Unset, str]):
        reservation_end_date (Union[Unset, datetime.date]):
        reservation_start_date (Union[Unset, datetime.date]):
        room_id (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    reservation_end_date: Union[Unset, datetime.date] = UNSET
    reservation_start_date: Union[Unset, datetime.date] = UNSET
    room_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        reservation_end_date: Union[Unset, str] = UNSET
        if not isinstance(self.reservation_end_date, Unset):
            reservation_end_date = self.reservation_end_date.isoformat()

        reservation_start_date: Union[Unset, str] = UNSET
        if not isinstance(self.reservation_start_date, Unset):
            reservation_start_date = self.reservation_start_date.isoformat()

        room_id = self.room_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if reservation_end_date is not UNSET:
            field_dict["reservation_end_date"] = reservation_end_date
        if reservation_start_date is not UNSET:
            field_dict["reservation_start_date"] = reservation_start_date
        if room_id is not UNSET:
            field_dict["room_id"] = room_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _reservation_end_date = d.pop("reservation_end_date", UNSET)
        reservation_end_date: Union[Unset, datetime.date]
        if isinstance(_reservation_end_date, Unset):
            reservation_end_date = UNSET
        else:
            reservation_end_date = isoparse(_reservation_end_date).date()

        _reservation_start_date = d.pop("reservation_start_date", UNSET)
        reservation_start_date: Union[Unset, datetime.date]
        if isinstance(_reservation_start_date, Unset):
            reservation_start_date = UNSET
        else:
            reservation_start_date = isoparse(_reservation_start_date).date()

        room_id = d.pop("room_id", UNSET)

        hotel_book_room_response_200 = cls(
            id=id,
            reservation_end_date=reservation_end_date,
            reservation_start_date=reservation_start_date,
            room_id=room_id,
        )

        hotel_book_room_response_200.additional_properties = d
        return hotel_book_room_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
