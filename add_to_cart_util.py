import datetime
from time import sleep
from urllib import parse as urlparse
import pytz
import json
import re

domainName = "local-qa.staples.com"
applicationPath = "/services/printing"


async def loadCartPage(session, stress):
    async with session.get(f"https://{domainName}{applicationPath}/Cart", ssl=False, timeout=None) as response:
        data = await response.text()
        if stress is True:
            sleep(0.1)
            return None

        userIdPart = re.findall(
            "set_encUserID\('.*'\)", data)[0]
        encUserId = re.split("'", userIdPart)[1]
        sleep(0.1)
        async with session.get(f"https://{domainName}{applicationPath}/services/printing/Cart/Api/GetCartCount",
                               ssl=False, timeout=None) as cartCount:
            await cartCount.text()
        async with session.post(
                f"https://{domainName}{applicationPath}/PC.WebServices/CartService.svc/GetCartItemCounts",
                json={"encUserID": encUserId}, ssl=False, timeout=None) as apiResponse:
            data = await apiResponse.text()
        sleep(0.1)
    return None


async def addToShoppingCart(session, groupKey, projectKey, selectedQuantity):
    data = {
        "GroupProjectKey": groupKey,
        "Projects": [
            {
                "ProjectKey": projectKey,
                "Quantity": selectedQuantity
            }
        ]
    }
    async with session.post(f"https://{domainName}{applicationPath}/api/v3/cart/AddGroupProjectToCart",
                            json=data, ssl=False, timeout=None) as response:
        await response.text()
    sleep(0.1)
    return None


async def updateProject(session, projectKey, productKey, selectedQuantity, specOptionKey):
    async with session.get(f"https://{domainName}{applicationPath}/api/v3/project/activeOptions/{projectKey}",
                           ssl=False, timeout=None) as optionResponse:
        selectedOptions = json.loads(await optionResponse.text())

    if specOptionKey is not None:
        selectedOptions[specOptionKey] = "True"

    data = {
        "ProjectId": projectKey,
        "ProductKey": productKey,
        "SelectedOptions": selectedOptions,
        "SelectedQuantity": selectedQuantity
    }

    async with session.post(f"https://{domainName}{applicationPath}/api/v3/project/UpdateForReview/{projectKey}",
                            json=data, ssl=False, timeout=None) as response:
        await response.text()
    sleep(0.1)
    return response.status


async def estimateShipMethods(session, productSku, selectedQuantity, price):
    tz = pytz.timezone("America/Los_Angeles")
    now = urlparse.quote(tz.localize(
        datetime.now()).isoformat(timespec="seconds"))
    url = f"https://{domainName}{applicationPath}/cart/api/ShippingMethods/Estimate?retailerProductSku={productSku}&quantity={selectedQuantity}&price={price}&orderDate={now}"
    async with session.get(url, ssl=False, timeout=None) as response:
        await response.text()
    sleep(0.05)
    return None


async def setShipMethod(session):
    async with session.post(f"https://{domainName}{applicationPath}/cart/api/ShippingMethod",
                            json={"Id": "1tJHqTB,glCJdT3MYpet5WpqwOARm9GXE"}, ssl=False, timeout=None) as response:
        await response.text()
    sleep(0.1)
    return None


async def setPickupLocation(session, storeNumber):
    async with session.post(f"https://{domainName}{applicationPath}/cart/api/PickupLocation",
                            json={"RetailerStoreId": storeNumber}, ssl=False, timeout=None) as response:
        await response.text()
        sleep(0.1)
        return None


async def setCourierDeliveryAddress(session, address1, city, zipCode, stateAbbre):
    async with session.post(f"https://{domainName}{applicationPath}/legacy/api/address/lmd/storenumber",
                            json={"Address1": address1, "City": city, "PostalCode": zipCode,
                                  "StateAbbreviation": stateAbbre},
                            ssl=False, timeout=None) as response:
        await response.text()
        sleep(0.1)
        return None


async def getStorePromisedTime(session, storeNumber, isExress):
    body = {"Products": [{"ProductSku": "PNI_PostCards_SameDay", "Options": [
        {"Key": "IsExpress", "Value": f"{isExress}"}]}], "RetailerStoreId": storeNumber}
    async with session.post(f"https://{domainName}{applicationPath}/cart/api/StorePromiseTime", json=body, ssl=False,
                            timeout=None) as response:
        await response.text()
    sleep(0.05)
    return None


async def loadUpsellPage(session):
    async with session.get(f"https://{domainName}{applicationPath}/cart/api/Info", ssl=False, timeout=None) as cartInfo:
        await cartInfo.text()
    async with session.get(
            f"https://{domainName}{applicationPath}/legacy/StoreLocatorProxy/GetDefaultStore?latitude=47.65&longitude=-122.31&locale=en_US",
            ssl=False, timeout=None) as defaultStore:
        await defaultStore.text()
    await estimateShipMethods(session)
    await getStorePromisedTime(session, True)
    await getStorePromisedTime(session, False)
    sleep(0.1)
    return None


async def approveProject(session, projectKey):
    async with session.post(f"https://{domainName}{applicationPath}/api/v3/project/Approve/{projectKey}",
                            json={}, ssl=False, timeout=None) as response:
        await response.text()
    sleep(0.1)
    return None


async def getProjectInfo(session, productKey):
    async with session.get(f"https://{domainName}{applicationPath}/product/{productKey}/builder/", ssl=False,
                           timeout=None) as response:
        data = await response.text()
        groupId = re.findall("[0-9]+", response.url.path)[0]
    sleep(0.1)
    summaryUrl = f"https://{domainName}{applicationPath}/api/builder/v3/project/group/summary/{groupId}"
    async with session.get(summaryUrl, ssl=False, timeout=None) as jsonResponse:
        data = json.loads(await jsonResponse.text())

    return (groupId, data["SubProjects"][0]["ProjectKey"])


async def setupAsRik(session, storeNumber):
    async with session.get(
            f"https://{domainName}{applicationPath}/legacy/station/6B696F736b5F72696B/{storeNumber}/redirect/",
            ssl=False, timeout=None) as response:
        await response.text()
    sleep(0.1)
    return None


async def setEnvironment(session, pnienv):
    async with session.get(f"https://{domainName}{applicationPath}/?pnienv={pnienv}",
                           ssl=False, timeout=None) as response:
        await response.text()
    sleep(0.1)
    return None
