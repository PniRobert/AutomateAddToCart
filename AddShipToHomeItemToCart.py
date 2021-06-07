import asyncio
import aiohttp

from add_to_cart_util import getProjectInfo, approveProject, updateProject
from add_to_cart_util import setShipMethod, addToShoppingCart
from auth_info import authCookieName, authCookieValue

# pnienv = "qa1"

# productKey = "880e9a0b0a627f97"
# productKey = "550f7cadad98fe98"
# productKey = "34a92d9f78cb90a4"
# productKey = "fadb30ec37bdebc8" # same day poster mega staging
productKey = "1d9fccc4c2386dfa"  # Ultra Thick Business Cart
selectedQuantity = 100


async def generateCourierCartItem():
    cookies = {authCookieName: authCookieValue}
    async with aiohttp.ClientSession(cookies=cookies) as session:
        # await setEnvironment(session)
        projectInfo = await getProjectInfo(session, productKey)
        await approveProject(session, projectInfo[1])
        await updateProject(session, projectInfo[1], productKey, selectedQuantity, None)
        await setShipMethod(session)
        await addToShoppingCart(session, projectInfo[0], projectInfo[1], selectedQuantity)


if __name__ == "__main__":
    asyncio.run(generateCourierCartItem())
