from bs4 import BeautifulSoup
import concurrent.futures
from datetime import datetime, timezone
from datetime import timedelta
from time import sleep
from urllib import parse as urlparse
import pytz
import asyncio
import aiohttp
import json
import re

pnienv = "qa1"
domainName = "local-qa.staples.com"
applicationPath = "/services/printing"
authCookieName = "SPLUS.Phoenix.Site.Auth"
authCookieValue = "CfDJ8O9Q0PpvA_BJszQq-wRngAUhkb7u_5PxJqHvk9bZXkAv7cv_qPmGeqJiVAt56UdhPjBL23Lu9c1wHuD8lRh8Z3" + \
                  "qlcPYw2w14hC9iWvmjGfzXmfthsJSWhXKah-xo6PwLX23ZSaJLiOnaQiE7k9CyVNYIsv7aSY2X68N77kBz1MstWI3g" + \
                  "MN2jK0mFAKh7vcUv82x54xdDMu2TGzChNDRT0AGNNZBN54h0-U9JKNTKZN8V5tWUBizluklvw-Hjk3-Zts5KVvaqnZn" + \
                  "hNOjKopgHzqswEAxv4NOBnVYpq3mAEOxKBbH7qDap2b56OucjwKdUZhd5FyI6ixf1D-F5gmXgReM"

async def setCourierDeliveryAddress(session):
    async with session.post(f"https://{domainName}{applicationPath}/cart/api/address/current",
                            json={"Address1": "321 West Galer Street", "City": "Seattle", "PostalCode": "98119",
                                  "StateAbbreviation": "WA"},
                            ssl=False, timeout=None) as response:
        await response.text()
        sleep(0.1)
        return None

async def visitSite():
    cookies = {authCookieName: authCookieValue}
    async with aiohttp.ClientSession(cookies=cookies) as session:
        await setCourierDeliveryAddress(session)


if __name__ == "__main__":
    asyncio.run(visitSite())
