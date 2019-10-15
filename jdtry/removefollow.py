﻿import json
import time
import request
from log import logger
import config

def getFollowList(user):
    url = 'https://t.jd.com/follow/vender/qryCategories.do?qryKey=&_={0}'.format(
        time.time())
    follows = []
    setHeader(user)

    try:
        response = request.openUrl(url, user, {})
        content = str(response.read(), 'utf-8')
        decodeContent = json.loads(content)

        if decodeContent.__contains__("data"):
            for category in decodeContent.get("data",[]):
                for entry in category["entityIdSet"]:
                    follows.append(entry)
        else:
            logger.error(decodeContent)
            if (decodeContent.get("error","") == "NotLogin"):
                user["token"] = ""
                config.saveUserConfig(user)
                logger.info("clear token and save to config file")


    except Exception as ex:
        logger.error("获取店铺关注列表报错, url:{0}".format(url))
        logger.error(ex)

    logger.info(follows)
    logger.info("关注店铺总数:{0}".format(len(follows)))

    return follows

def setHeader(user):
    user["headers"].update({
        "Host": "t.jd.com",
        "Referer": "https://t.jd.com/vender/followVenderList.action"
    })


def removeFollow(user, vendor):
    url = 'https://t.jd.com/follow/vender/unfollow.do?venderId={0}&_={1}'.format(
        vendor, time.time())
    setHeader(user)

    try:
        response = request.openUrl(url, user, {})
        content = str(response.read(), 'utf-8')
        decodeContent = json.loads(content)
        logger.info(decodeContent)

    except Exception as ex:
        logger.error("取消店铺关注列表报错, url:{0}".format(url))
        logger.error(ex)


def remove(user):
    while True:
        follows = getFollowList(user)
        if (follows and len(follows) > 0):
            for follow in follows:
                removeFollow(user, follow)
        else:
            break



