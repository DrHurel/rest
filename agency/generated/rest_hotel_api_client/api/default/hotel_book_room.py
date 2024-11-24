from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hotel_book_room_body import HotelBookRoomBody
from ...models.hotel_book_room_response_200 import HotelBookRoomResponse200
from ...types import UNSET, Response


def _get_kwargs(
    uuid: str,
    *,
    body: HotelBookRoomBody,
    token: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    params["token"] = token

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/room/{uuid}/book",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[HotelBookRoomResponse200]:
    if response.status_code == 200:
        response_200 = HotelBookRoomResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[HotelBookRoomResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: HotelBookRoomBody,
    token: str,
) -> Response[HotelBookRoomResponse200]:
    """
    Args:
        uuid (str):
        token (str):
        body (HotelBookRoomBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HotelBookRoomResponse200]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
        token=token,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: HotelBookRoomBody,
    token: str,
) -> Optional[HotelBookRoomResponse200]:
    """
    Args:
        uuid (str):
        token (str):
        body (HotelBookRoomBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HotelBookRoomResponse200
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
        token=token,
    ).parsed


async def asyncio_detailed(
    uuid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: HotelBookRoomBody,
    token: str,
) -> Response[HotelBookRoomResponse200]:
    """
    Args:
        uuid (str):
        token (str):
        body (HotelBookRoomBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HotelBookRoomResponse200]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
        token=token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: HotelBookRoomBody,
    token: str,
) -> Optional[HotelBookRoomResponse200]:
    """
    Args:
        uuid (str):
        token (str):
        body (HotelBookRoomBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HotelBookRoomResponse200
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
            token=token,
        )
    ).parsed
