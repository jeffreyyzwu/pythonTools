import json
import time
import request
from log import logger
from bs4 import BeautifulSoup
import config

def applyAllTryProducts(user, prop):
    totalPage = 10
    page = 1
    allTryProducts = []

    while page <= totalPage:
        try:
            totalPage = getTryProductList(allTryProducts, user, prop, page)
            alreadyApplyTryProducts = getAlreadyApplyTryProduct(allTryProducts, user)
            notApplyTryProds = excludeProducts(allTryProducts, alreadyApplyTryProducts)

            if (notApplyTryProds and len(notApplyTryProds) > 0):
                logger.info("未申请的试用产品:{0}".format(notApplyTryProds))
                for prodId in notApplyTryProds:
                    vendorId = getVendorByProductId(user, prodId)
                    followVendor(user, vendorId)
                    applyTryProduct(user, prodId)

            page = page + 1
            allTryProducts = []

        except Exception as ex:
            logger.error("applyAllTryProducts")
            logger.error(ex)



def excludeProducts(allTryProducts, alreadyApplyTryProducts):
    result = []
    for prod in allTryProducts:
        prodId = int(prod)
        if prodId not in alreadyApplyTryProducts:
            result.append(prodId)

    return result


def getAlreadyApplyTryProduct(allTryProducts, user):
    prodIds = ','.join(allTryProducts)
    url = 'https://try.jd.com/user/getApplyStateByActivityIds?activityIds={0}'.format(
        prodIds)
    user["headers"].update({
        "Referer": url
    })
    result = []

    try:
        response = request.openUrl(url, user, {})
        content = str(response.read(), 'utf-8')
        decodeContent = json.loads(content)

        for item in decodeContent:
            result.append(item["activityId"])

        # logger.info(result)

    except Exception as ex:
        logger.error("获取已申请试用产品报错, url:{0}".format(url))
        logger.error(content)
        logger.error(ex)

    return result


def getTryProductList(allTryProducts, user, prop, page):
    url = 'https://try.jd.com/activity/getActivityList?page={0}&activityType=1&activityState=0&cids={1}'.format(
        page, prop["cids"])
    user["headers"].update({
        "Host": "try.jd.com",
        "Referer": url
    })
    totalPage = 1

    try:
        response = request.openUrl(url, user, {})
        logger.info("all try product url:{0}".format(url))

        content = str(response.read(), 'utf-8')
        # logger.info("html content response:{0}".format(content))
        soup = BeautifulSoup(content, "html.parser")

        for result in soup.find_all('li', {"class": "item"}):
            # logger.info("result:{0}".format(result))
            # time.sleep(1)

            activityId = result.get("activity_id")
            # logger.info("activityId:{0}".format(activityId))
            if activityId is not None:
                allTryProducts.append(activityId)
        logger.info("allTryProducts:{0}".format(allTryProducts))

        for result in soup.find_all('span', {"class": "p-skip"}):
            totalPage = int(result.em.b.get_text(strip=True))
            logger.info("url:{0}总页数:{1}".format(url, totalPage))

    except Exception as ex:
        logger.error("获取试用产品列表报错, url:{0}".format(url))
        logger.error(ex)
        logger.error(content)

    return totalPage

def getVendorByProductId(user, prodId):
    url = 'http://try.jd.com/migrate/getActivityById?id={0}'.format(
        prodId)
    user["headers"].update({
        "Referer": url,
        "Host": "try.jd.com"
    })

    try:
        response = request.openUrl(url, user, {})
        content = str(response.read(), 'utf-8')
        # logger.info("vendor response content:{0}".format(content))
        decodeContent = json.loads(content)

        if "data" not in decodeContent:
            return 0

        shopInfo = decodeContent["data"]["shopInfo"]
        logger.info(shopInfo)
        
        shopId = shopInfo["shopId"]
        logger.info("shop id:{0}".format(shopId))

        return shopId
    except Exception as ex:
        logger.error(ex)
        return 0


def followVendor(user, venderId):
    url = 'http://try.jd.com/migrate/follow?_s={0}&venderId={1}'.format('pc',
        venderId)
    user["headers"].update({
        "Referer": url
    })

    response = request.openUrl(url, user, {})
    content = str(response.read(), 'utf-8')
    decodeContent = json.loads(content)
    logger.info("follow shop result:{0}".format(decodeContent))

def applyTryProduct(user, prodId):
    url = 'https://try.jd.com/migrate/apply?activityId={0}&source=0'.format(
        prodId)
    user["headers"].update({
        "Referer": url
    })

    response = request.openUrl(url, user, {})
    content = str(response.read(), 'utf-8')
    decodeContent = json.loads(content)
    logger.info("apply product id:{0}, result:{1}".format(prodId, decodeContent))

    status = decodeContent["code"]
    if (status == '-131'):
        raise Exception('apply times is limited')
    if (status == '-600'):
        user["token"] = ""
        config.saveUserConfig(user)
        logger.info("clear token and save to user config file")
        raise Exception("please login first")


def getProductProperty():
    return [
        {"cids": "737", "name": "家用电器"},
        {"cids": "12218", "name": "生鲜美食"},
        {"cids": "1320,12259", "name": "食品饮料"},
        {"cids": "1316", "name": "美妆护肤"},
        {"cids": "15901", "name": "家庭清洁"},
        {"cids": "1620,6728,9847,9855,6196,15248,14065", "name": "家居家装"},
        {"cids": "5025,6144", "name": "钟表奢品"},
        {"cids": "652,9987", "name": "手机数码"},
        {"cids": "670", "name": "电脑办公"},
        {"cids": "1315,1672,1318,11729", "name": "服饰鞋包"},
        {"cids": "1319,6233", "name": "母婴玩具"},
        {"cids": "1713,4051,4052,4053,7191,7192,5272", "name": "图书音像"},
        {"cids": "16750", "name": "个人护理"},
        {"cids": "4938,13314,6994,9192,12473,6196,5272,12379,13678,15083,15126,15980", "name": "更多惊喜"}
    ]

def hottryapply(user):
    logger.info("热门试用产品开始申请")

    url = 'http://try.jd.com'
    user["headers"].update({
        "Host": "try.jd.com",
        "Referer": url
    })

    try:
        response = request.openUrl(url, user, {})
        logger.info("opening web")
        content = str(response.read(), 'utf-8')
        soup = BeautifulSoup(content, "html.parser")
        hottryprods = []

        for result in soup.find_all('li', {"class": "ui-switchable-panel"}):
            activityId = result.get("activity_id")
            if (not activityId is None):
                hottryprods.append(activityId)

        logger.info("热门试用产品:{0}".format(hottryprods))

        for prodId in hottryprods:
            vendorId = getVendorByProductId(user, prodId)
            followVendor(user, vendorId)
            applyTryProduct(user, prodId)

    except Exception as ex:
        logger.error("获取试用产品列表报错, url:{0}".format(url))
        logger.error(ex)
        logger.error(content)

    logger.info("热门试用产品结束申请")

def apply(user):
    try:
        hottryapply(user)

        props = getProductProperty()
        applyCategories = user.get("apply", props)
        for prop in props:
            applyAllTryProducts(user, prop)

    except Exception as ex:
        logger.error(ex)
