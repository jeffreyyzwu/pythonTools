from log import logger
import request
import config
import json
import login


def setQueryHeader(user):
    user["headers"].update({
        "Host": "m.dianping.com",
        "Origin": "https://h5.dianping.com",
        "Referer": "https://h5.dianping.com/app/app-community-free-meal/index.html?utm_source=qgzq&from=m_richbutton_1",
        "DNT": "1"
    })


def checkin(user):
    config.getConfig(user)

    url = 'https://m.dianping.com/mobile/event/arro/checkin'
    setQueryHeader(user)
    response = request.openUrl(url, user, {})
    content = response.read()
    content = str(content, 'utf-8')

    logger.info("霸王餐签到结果:{0}".format(content))
    checkLoginStatus(user, content)


def checkLoginStatus(user, content):
    json_data = json.loads(content)

    retCode = json_data["code"]
    if (retCode == 401):
        isLogin = json_data["msg"]["isLogin"]
        if (isLogin == "0"):
            login.refreshToken(user)

    # {"code":401,"msg":{"isLogin":"0","errorMsg":"未登录"}}
    # {"code":201,"msg":{"isLogin":"1","dayNum":9,"availableIntegral":191,"errorMsg":"今天已经打过卡了"}}
