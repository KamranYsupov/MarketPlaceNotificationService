import json

import websockets
import aiohttp
from aiohttp.client_reqrep import ClientResponse
from rest_framework.response import Response
from rest_framework.exceptions import APIException


async def send_websocket_data(uri: str, data: dict) -> dict:
    async with websockets.connect(uri) as websocket:
        json_data = json.dumps(data)
        await websocket.send(json_data)
                
        return await websocket.recv()
    

async def get_response_data_or_raise_http_exception(
    response: ClientResponse,
    excpected_status_code: int = 200,
):
    response_data = await response.json()
    if response.status == excpected_status_code:
        return response_data
    
    raise APIException(
        detail=response_data.get('detail'), 
        code=response.status
    )