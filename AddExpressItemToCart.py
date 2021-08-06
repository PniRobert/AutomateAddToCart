import asyncio
import aiohttp

from add_to_cart_util import getProjectInfo, approveProject, updateProject
from add_to_cart_util import setPickupLocation, addToShoppingCart
from auth_info import authCookieName, authCookieValue

# pnienv = "qa1"

productKey = "1cc56024150153ed"  # same day brochure
selectedQuantity = 25
seattleStore = "1361"


async def generate_express_item():
    cookies = {authCookieName: authCookieValue}
    async with aiohttp.ClientSession(cookies=cookies) as session:
        # await setEnvironment(session)
        projectInfo = await getProjectInfo(session, productKey)
        await approveProject(session, projectInfo[1])
        await updateProject(session, projectInfo[1], productKey, selectedQuantity, "IsExpress")
        await setPickupLocation(session, seattleStore)
        await addToShoppingCart(session, projectInfo[0], projectInfo[1], selectedQuantity)


if __name__ == "__main__":
    asyncio.run(generate_express_item())
