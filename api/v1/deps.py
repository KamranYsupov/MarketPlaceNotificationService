import aiohttp

from django.conf import settings 

from .utils import get_response_data_or_raise_http_exception


async def get_current_user(request) -> dict:
    auth_header = request.headers.get('Authorization')
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{settings.AUTH_USERS_SERVICE_API_V1_URL}/users/me/',
            headers={'Authorization': str(auth_header)}
        ) as response:
            return await get_response_data_or_raise_http_exception(response)
