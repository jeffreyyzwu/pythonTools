import json
import request
import config
import urllib
import os.path
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
    url = 'https://i.meituan.com/beautytry/productlist?token={0}&channel=10&category=0&period=0&cityid=30&longitude=&latitude=&dpid=&type=0'
    url = url.format(user["token"])

    response = request.openUrl(url, user, {})
    content = response.read()
    # logger.debug(content)

    decodeContent = json.loads(content)
    # logger.debug(decodeContent)

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
    url = 'https://i.meituan.com/beautytry/productlist/detail'
    params = {
        "channel": 10,
        "category": 0,
        "userid": '',
        "longitude": '',
        "latitude": '',
        "dpid": '',
        "productid": prod["id"],
        "productbackendid": 0,
        "cityid": 30,
        "utm_source": 'rb'
    }
    fetchUrl = "?".join([url, urllib.parse.urlencode(params)])
    response = request.openUrl(fetchUrl, user, {})
    content = response.read()
    if b'<!DOCTYPE html>' in content:
        logger.debug('reponse content is html')
        # logger.debug(content)
        return

    jsondata = json.loads(content)
    shopId = getShopId(jsondata)
    shop = jsondata["data"]["selectShop"]
    prod.update({
        "shopId": shopId,
        "shopType": shop["shopType"]
    })

    logger.info(prod)


def getShopId(data):
    shopUrl = data["data"]["shopUrl"]
    url = urllib.parse.urlparse(shopUrl)
    if url.scheme == "imeituan":
        params = urllib.parse.parse_qs(url.query)
        # logger.debug(params)

        if "id" in params:
            shopId = params["id"][0]
            return shopId
        else:
            logger.error("无法获取shopid", shopUrl)
            return ''
    else:
        result = os.path.split(url.path)
        shopId = result[1]
        return shopId


def signFreeBeautyTry(prod, user):
    url = 'https://i.meituan.com/beauty-salvia/try-center/tryresult.html'
    params = {
        "token": user["token"],
        "longitude": "*",
        "lng": "*",
        "latitude": "*",
        "lat": "*",
        "dpid": "",
        "channel": "10",
        "category": "0",
        "catid": "22",
        "utm_source": "rb",
        "cityid": "30",
        "ci": "30",
        "mina_name": "",
        "productid": prod["id"],
        "source": "",
        "shopid": prod.get("shopId", ''),
        "mobile": user["phone"],
        "utm_source": "rb",
        "utm_medium": "iphone",
        "f": "iphone",
        "version_name": "10.0.601",
        "regionid": "",
        "mina_name": ""
    }
    queryParams = urllib.parse.urlencode(params)
    fetchUrl = "?".join([url, queryParams])
    response = request.openUrl(fetchUrl, user, {})
    content = response.read()

    soup = BeautifulSoup(content, "html.parser")
    for result in soup.find_all('div', {"class": "result-text"}):
        logger.info(prod["name"] + ': ' + result.get_text(strip=True))
