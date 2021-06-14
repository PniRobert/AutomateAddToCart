from time import sleep
import asyncio
import aiohttp

from auth_info import authCookieName, authCookieValue
from add_to_cart_util import setCourierDeliveryAddress
# pnienv = "qa1"


async def visitSite():
    cookies = {authCookieName: authCookieValue}
    async with aiohttp.ClientSession(cookies=cookies) as session:
        await setCourierDeliveryAddress(session, "321 West Galer Street", "Seattle",
                                        "98119", "WA")


if __name__ == "__main__":
    asyncio.run(visitSite())
