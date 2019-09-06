import json
import request
import config
import urllib
from bs4 import BeautifulSoup
from log import logger


def fetch(user):
    config.getConfig(user)
    prodList = getFreeTryList(user)
    for prod in prodList:
        signFreeTry(prod, user)


def getFreeTryList(user):
    url = 'https://m.dianping.com/beautytry/fun/productlist?channel=16&category=0&cityid=7&longitude=0&latitude=&env=0'
    response = request.openUrl(url, user, {})
    content = json.loads(response.read())
    data = content["data"]

    prodList = []
    for item in data:
        propItems = data[item]
        if (isinstance(propItems,list)):
            for prod in propItems:
                if (prod["hasRegister"] == False):
                    prodList.append({
                        "id": prod["id"],
                        "name": prod["name"],
                        "channel": prod["channelId"],
                        "price": prod["price"]
                    })
    logger.info(
        '-----获取以下未申请的免费试用,总数:{0}---\n{1}'.format(len(prodList), prodList))

    return prodList


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


def signFreeTry(prod, user):
    # https://m.dianping.com/play-next/node/freetry/result?productid=66818&jumpFromWx=&cityid=7&latitude=22.54881&longitude=113.94119&channel=16&product=dpapp&pushEnabled=0
    url = 'https://m.dianping.com/play-next/node/freetry/result'
    params = {
        "token": user["token"],
        "longitude": "*",
        "lng": "*",
        "latitude": "*",
        "lat": "*",
        "dpid": "*",
        "channel": prod["channel"],
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
    for result in soup.find_all('div', {"class": "supply-result"}):
        logger.info(prod["name"] + ': ' + result.get_text(strip=True))
