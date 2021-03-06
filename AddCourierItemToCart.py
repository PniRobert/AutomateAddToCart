import asyncio
import aiohttp

from add_to_cart_util import getProjectInfo, approveProject, updateProject
from add_to_cart_util import setCourierDeliveryAddress, setPickupLocation, addToShoppingCart
from auth_info import authCookieName, authCookieValue

# pnienv = "qa1"

# productKey = "337c731e2cc14900"
# productKey = "880e9a0b0a627f97"
# productKey = "550f7cadad98fe98"
# productKey = "34a92d9f78cb90a4"
# productKey = "fadb30ec37bdebc8" # same day poster mega staging
# productKey = "b904ce0e33e714d7"  # same day poster
productKey = "33cbcb43f16860e4" # same day flyer
selectedQuantity = 2
seattleStore = "1361"


async def generateCourierCartItem():
    cookies = {authCookieName: authCookieValue}
    async with aiohttp.ClientSession(cookies=cookies) as session:
        # await setEnvironment(session)
        projectInfo = await getProjectInfo(session, productKey)
        await approveProject(session, projectInfo[1])
        await updateProject(session, projectInfo[1], productKey, selectedQuantity, "IsCourierDelivery")
        await setCourierDeliveryAddress(session, "8830 25th Ave SW", "Seattle", "98106", "WA")
        await setPickupLocation(session, seattleStore)
        await addToShoppingCart(session, projectInfo[0], projectInfo[1], selectedQuantity)


if __name__ == "__main__":
    asyncio.run(generateCourierCartItem())
