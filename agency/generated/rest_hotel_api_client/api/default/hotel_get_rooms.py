import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hotel_get_rooms_response_200_item import HotelGetRoomsResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    start_date: Union[Unset, datetime.date] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    minsize: Union[Unset, int] = UNSET,
    minprize: Union[Unset, float] = UNSET,
    maxprice: Union[Unset, float] = UNSET,
    beds: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_start_date: Union[Unset, str] = UNSET
    if not isinstance(start_date, Unset):
        json_start_date = start_date.isoformat()
    params["start-date"] = json_start_date

    json_end_date: Union[Unset, str] = UNSET
    if not isinstance(end_date, Unset):
        json_end_date = end_date.isoformat()
    params["end-date"] = json_end_date

    params["minsize"] = minsize

    params["minprize"] = minprize

    params["maxprice"] = maxprice

    params["beds"] = beds

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/rooms",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["HotelGetRoomsResponse200Item"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = HotelGetRoomsResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["HotelGetRoomsResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.date] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    minsize: Union[Unset, int] = UNSET,
    minprize: Union[Unset, float] = UNSET,
    maxprice: Union[Unset, float] = UNSET,
    beds: Union[Unset, int] = UNSET,
) -> Response[List["HotelGetRoomsResponse200Item"]]:
    """fetch rooms with optional filter.

    Args:
        start_date (Union[Unset, datetime.date]):
        end_date (Union[Unset, datetime.date]):
        minsize (Union[Unset, int]):
        minprize (Union[Unset, float]):
        maxprice (Union[Unset, float]):
        beds (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['HotelGetRoomsResponse200Item']]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
        minsize=minsize,
        minprize=minprize,
        maxprice=maxprice,
        beds=beds,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.date] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    minsize: Union[Unset, int] = UNSET,
    minprize: Union[Unset, float] = UNSET,
    maxprice: Union[Unset, float] = UNSET,
    beds: Union[Unset, int] = UNSET,
) -> Optional[List["HotelGetRoomsResponse200Item"]]:
    """fetch rooms with optional filter.

    Args:
        start_date (Union[Unset, datetime.date]):
        end_date (Union[Unset, datetime.date]):
        minsize (Union[Unset, int]):
        minprize (Union[Unset, float]):
        maxprice (Union[Unset, float]):
        beds (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['HotelGetRoomsResponse200Item']
    """

    return sync_detailed(
        client=client,
        start_date=start_date,
        end_date=end_date,
        minsize=minsize,
        minprize=minprize,
        maxprice=maxprice,
        beds=beds,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.date] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    minsize: Union[Unset, int] = UNSET,
    minprize: Union[Unset, float] = UNSET,
    maxprice: Union[Unset, float] = UNSET,
    beds: Union[Unset, int] = UNSET,
) -> Response[List["HotelGetRoomsResponse200Item"]]:
    """fetch rooms with optional filter.

    Args:
        start_date (Union[Unset, datetime.date]):
        end_date (Union[Unset, datetime.date]):
        minsize (Union[Unset, int]):
        minprize (Union[Unset, float]):
        maxprice (Union[Unset, float]):
        beds (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['HotelGetRoomsResponse200Item']]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
        minsize=minsize,
        minprize=minprize,
        maxprice=maxprice,
        beds=beds,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.date] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    minsize: Union[Unset, int] = UNSET,
    minprize: Union[Unset, float] = UNSET,
    maxprice: Union[Unset, float] = UNSET,
    beds: Union[Unset, int] = UNSET,
) -> Optional[List["HotelGetRoomsResponse200Item"]]:
    """fetch rooms with optional filter.

    Args:
        start_date (Union[Unset, datetime.date]):
        end_date (Union[Unset, datetime.date]):
        minsize (Union[Unset, int]):
        minprize (Union[Unset, float]):
        maxprice (Union[Unset, float]):
        beds (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['HotelGetRoomsResponse200Item']
    """

    return (
        await asyncio_detailed(
            client=client,
            start_date=start_date,
            end_date=end_date,
            minsize=minsize,
            minprize=minprize,
            maxprice=maxprice,
            beds=beds,
        )
    ).parsed
