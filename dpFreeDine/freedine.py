import urllib.request
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import request
import config
from log import logger

def getAllFreeDineList(user, stype):
    allActList = []
    for page in range(1, 10):
        result = getFreeDineList(page, stype, user)
        allActList.extend(result)
        if (len(result) < 10):
            break

    allActList = sortDinesList(allActList, user)
    logger.info(
        '--------获取以下未报名霸王餐,总数：{0}------------\n{1}'.format(len(allActList), allActList))
    return allActList


def sortDinesList(dineList, user):
    logger.debug(dineList)

    sortDines = []

    # exclude
    if 'excludetitle' in user:
        for dine in reversed(dineList):
            for excludetitles in user["excludetitle"]:
                count = 0
                for excludetitle in excludetitles:
                    if excludetitle in dine["name"]:
                        count += 1
                if count == len(excludetitles):
                    dineList.remove(dine)

    logger.debug(dineList)

    # sort
    for dine in reversed(dineList):
        if dine["mode"] == 5 and 'VIP专享' in dine["name"]:
            sortDines.append(dine)
            dineList.remove(dine)

    for dine in reversed(dineList):
        if dine["mode"] == 16 and '橙V直接领取' in dine["name"] and '免费' in dine["name"]:
            sortDines.append(dine)
            dineList.remove(dine)

    sortDines.extend(dineList)
    return sortDines


def getFreeDineList(page, stype, user):
    url = 'https://m.dianping.com/activity/static/list?page={0}&cityid=7&regionParentId=0&regionId=0&type={1}&sort=0&filter=1&token={2}'.format(
        page, stype, user["token"])
    actList = []

    try:
        # logger.debug(url)
        response = request.openUrl(url, user, {})
        content = str(response.read(), 'utf-8')
        decodeContent = json.loads(content)
        logger.debug(content)

        for act in decodeContent["data"]["mobileActivitys"]:
            actList.append({
                "id": str(act["offlineActivityId"]),
                "name": act["title"],
                "mode": act["mode"]
            })
    except Exception as ex:
        logger.error("获取霸王餐列表报错, url:{0}".format(url))
        logger.error(content)
        logger.error(ex)

    logger.info(
        '---获取第{0}页,type:{2}霸王餐, size:{1}---'.format(page, len(actList), stype))
    return actList

def get_date():
    current_date = datetime.strftime(datetime.now()+ timedelta(days=60), "%Y-%m-%d")
    cur_year = datetime.now().year
    for plus in [0,1]:
        for date in ['-01-01','-03-01','-05-01', '-06-01', '-08-08','-09-09', '-10-01']:
           cal_date = str(cur_year+plus) + date
           if (cal_date > current_date):
                logger.info("-----日期:{0}-----".format(cal_date))
                return cal_date

    modified_date = datetime.now() + timedelta(days=100)
    cal_date = datetime.strftime(modified_date, "%Y-%m-%d")
    logger.info("-----日期:{0}-----".format(cal_date))
    return cal_date

def get_request_data(dine, user, stype):
    if (stype in [3]):
        return {
            "offlineActivityId": dine["id"],
            "phoneNo": user["phone"],
            "marryDayStr": get_date(),
            "marryStatus": 0,
            "shippingAddress": "",
            "extraCount": "",
            "birthdayStr": "",
            "email":"landair@yeah.net",
            "babyBirths":"",
            "pregnant":"",
            "comboId":"",
            "branchId":"",
            "usePassCard":0,
            "passCardNo": ""
        }
    else:
        return {
            "passCardNo": "",
            "phoneNo": user["phone"],
            "cx": "",
            "uuid": "",
            "offlineActivityId": dine["id"],
            "env": 1,
            "source": "null"
        }
def signUpFreeDine(dine, user, stype):
    data = get_request_data(dine, user, stype)
    url = 'http://s.dianping.com/ajax/json/activity/offline/saveApplyInfo'
    user["headers"].update({
        "Host": "s.dianping.com",
        "Referer": "http://s.dianping.com/event/" + dine["id"]
    })

    try:
        response = request.openUrl(url, user, data)
        content = str(response.read(), 'utf-8')
        decodeContent = json.loads(content)
        resultCode = decodeContent["code"]

        logger.info("-----霸王餐:{0}-----".format(dine["name"]))
        if (resultCode == 200):
            logger.info('-----报名成功-----')
        else:
            errMessage = decodeContent["msg"]["html"]
            logger.info(
                '-----报名失败:{0},{1}-----'.format(resultCode, errMessage))

    except Exception as ex:
        logger.error('--------报名中断报错------')
        logger.error(content)
        logger.error(ex)


def setQueryHeader(user):
    user["headers"].update({
        "Host": "m.dianping.com",
        "Referer": "http://m.dianping.com"
    })


def getSuccessSaveFreeDine(user):
    url = 'http://m.dianping.com/mobile/event/mine?source=null'
    setQueryHeader(user)
    response = request.openUrl(url, user, {})
    content = response.read()
    soup = BeautifulSoup(content, "html.parser")

    logger.info('------成功报名的霸王餐------')
    for lind in soup.find_all('span'):
        if "title" in str(lind):
            logger.info(lind.get_text(strip=True))


def fetchFreeDine(user):
    # 1: 美食, 2:美容, 3:婚嫁 4:亲子  6:玩乐 10:生活服务 99:其他
    for stype in [3, 1, 2, 6, 10, 99]:
        config.getConfig(user)
        dineList = getAllFreeDineList(user, stype)
        for dine in dineList:
            signUpFreeDine(dine, user, stype)

    getSuccessSaveFreeDine(user)
