from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hotel_get_room_details_response_200_rooms import HotelGetRoomDetailsResponse200Rooms


T = TypeVar("T", bound="HotelGetRoomDetailsResponse200")


@_attrs_define
class HotelGetRoomDetailsResponse200:
    """
    Attributes:
        rooms (Union[Unset, HotelGetRoomDetailsResponse200Rooms]):
    """

    rooms: Union[Unset, "HotelGetRoomDetailsResponse200Rooms"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        rooms: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rooms, Unset):
            rooms = self.rooms.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rooms is not UNSET:
            field_dict["rooms"] = rooms

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.hotel_get_room_details_response_200_rooms import HotelGetRoomDetailsResponse200Rooms

        d = src_dict.copy()
        _rooms = d.pop("rooms", UNSET)
        rooms: Union[Unset, HotelGetRoomDetailsResponse200Rooms]
        if isinstance(_rooms, Unset):
            rooms = UNSET
        else:
            rooms = HotelGetRoomDetailsResponse200Rooms.from_dict(_rooms)

        hotel_get_room_details_response_200 = cls(
            rooms=rooms,
        )

        hotel_get_room_details_response_200.additional_properties = d
        return hotel_get_room_details_response_200

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
