import json
import request
import config
import urllib
from bs4 import BeautifulSoup
from log import logger


def fetchFreeBeautyTry(user):
    config.getConfig(user)
    prodList, shopList = getFreeBeautyTryList(user)
    for prod in prodList:
        signFreeBeautyTry(prod, user)

    for shop in shopList:
        getShopDetail(shop, user)
        signFreeBeautyTry(shop, user)


def getFreeBeautyTryList(user):
    url = 'https://m.dianping.com/beautytry/productlist?channel=1&category=0&period=0&cityid=7&longitude=%2A&latitude=%2A&dpid=%2A&type=0'
    response = request.openUrl(url, user, {})
    content = response.read()
    decodeContent = json.loads(content)

    prodList = []
    for prod in decodeContent["data"]["goodProductList"]:
        if (prod["hasRegister"] == False):
            prodList.append({
                "id": prod["id"],
                "name": prod["name"]
            })
    logger.info(
        '-----获取以下未申请的免费试用,总数:{0}---\n{1}'.format(len(prodList), prodList))

    shopList = []
    for shop in decodeContent["data"]["experienceProductList"]:
        if (shop["hasRegister"] == False):
            shopList.append({
                "id": shop["id"],
                "name": shop["simpleName"],
                "price": shop["price"]
            })
    logger.info(
        '-----获取以下未申请的0元探新店产品试用,总数:{0}---\n{1}'.format(len(shopList), shopList))

    return prodList, shopList


def getShopDetail(prod, user):
    url = 'https://m.dianping.com/beautytry/productlist/detail'
    params = {
        "channel": 1,
        "category": 0,
        "userid": '',
        "longitude": '',
        "latitude": '',
        "dpid": '',
        "productid": prod["id"],
        "productbackendid": 0,
        "cityid": 7,
        "utm_source": 'rb'
    }
    fetchUrl = "?".join([url, urllib.parse.urlencode(params)])
    user["headers"].update({
        "Host": "m.dianping.com",
        "Referer": fetchUrl + '&businesskey=',
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1"
    })
    response = request.openUrl(fetchUrl, user, {})
    jsondata = json.loads(response.read())
    shop = jsondata["data"]["selectShop"]
    prod.update({
        "shopId" : shop["shopId"],
        "shopType" : shop["shopType"]
    })

    # logger.info(prod)


def signFreeBeautyTry(prod, user):
    url = 'https://m.dianping.com/beauty-salvia/try-center/tryresult.html'
    params = {
        "token": user["token"],
        "longitude": "*",
        "lng": "*",
        "latitude": "*",
        "lat": "*",
        "dpid": "*",
        "channel": "1",
        "category": "0",
        "catid": "50",
        "utm_source": "rb",
        "cityid": "7",
        "ci": "",
        "mina_name": "",
        "productid": prod["id"],
        "source": "",
        "shopid": prod.get("shopId",''),
        "mobile": user["phone"]
    }
    queryParams = urllib.parse.urlencode(params)
    fetchUrl = "?".join([url, queryParams])
    user["headers"].update({
        "Host": "m.dianping.com",
        "Referer": fetchUrl,
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1"
    })
    response = request.openUrl(fetchUrl, user, {})
    content = response.read()

    soup = BeautifulSoup(content, "html.parser")
    for result in soup.find_all('div', {"class": "result-text"}):
        logger.info(prod["name"] + ': ' + result.get_text(strip=True))
