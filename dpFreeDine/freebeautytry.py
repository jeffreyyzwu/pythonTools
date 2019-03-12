import json
import request
import config
import urllib
from bs4 import BeautifulSoup
from log import logger


def fetchFreeBeautyTry(user):
    config.getConfig(user)
    prodList = getFreeBeautyTryList(user)
    for prod in prodList:
        signFreeBeautyTry(prod, user)


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
    logger.info('-----获取以下未申请的免费试用,总数:{0}---\n{1}'.format(len(prodList), prodList))

    return prodList


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
        "shopid": "",
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
    for result in soup.find_all('div',{"class":"result-text"}):
        logger.info(prod["name"],': ', result.get_text(strip=True))
        
