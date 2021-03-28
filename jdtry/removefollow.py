import json
import time
import request
from log import logger
import config

def getFollowList(user):
    url = 'https://t.jd.com/follow/vender/qryCategories.do?qryKey=&_={0}'.format(time.time())
    follows = []
    setHeader(user)

    try:
        response = request.openUrl(url, user, {})
        content = str(response.read(), 'utf-8')
        decodeContent = json.loads(content)

        if decodeContent.__contains__("data"):
            # logger.info(decodeContent)
            for category in decodeContent.get("data",[]):
                for entry in category["entityIdSet"]:
                    follows.append(entry)
        else:
            # logger.error(decodeContent)
            if (decodeContent.get("error","") == "NotLogin"):
                user["token"] = ""
                config.saveUserConfig(user)
                logger.info("clear token and save to config file")


    except Exception as ex:
        logger.error("账户:{0}获取店铺关注列表报错, url:{1}，错误信息:{2}".format(user["phone"], url, ex))

    logger.info("账户:{0}关注店铺总数:{1}, 具体如下:{2}".format(user["phone"],len(follows), follows))

    return follows

def setHeader(user):
    user["headers"].update({
        "Host": "t.jd.com",
        "Referer": "https://t.jd.com/vender/followVenderList.action"
    })


def removeFollow(user, vendor):
    url = 'https://t.jd.com/follow/vender/unfollow.do?venderId={0}&_={1}'.format(vendor, time.time())
    setHeader(user)

    try:
        response = request.openUrl(url, user, {})
        content = str(response.read(), 'utf-8')
        # decodeContent = json.loads(content)
        logger.info("账户:{0}取消店铺{1}关注, 结果信息:{2}".format(user["phone"], vendor, content))


    except Exception as ex:
        logger.error("账户:{0}取消店铺关注列表报错, url:{1}, 错误信息:{2}".format(user["phone"], url, ex))

def remove(user):
    while True:
        follows = getFollowList(user)
        if (follows and len(follows) > 100):
            for follow in follows:
                removeFollow(user, follow)
        else:
            break



