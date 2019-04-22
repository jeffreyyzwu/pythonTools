import json
import mail
from log import logger


def getUsers():
    with open('conf/users.json', encoding='utf-8-sig') as json_file:
        users = json.load(json_file)

        enableUsers = []
        for user in users:
            if (user.__contains__("enable") and user["enable"].lower() == "true"):
                enableUsers.append(user)

        logger.info(
            '----------load user file success-----------\n{0}'.format(enableUsers))

        json_file.close()
        return enableUsers


def saveUserConfig(user):
    logger.info("------保存更新token到users配置文件中--------")
    try:
        with open('conf/users.json', mode="r", encoding='utf-8-sig') as json_read_file:
            usersConfig = json.load(json_read_file)
            for config in usersConfig:
                if (config["phone"] == user["phone"]):
                    config["token"] = user["token"]
                    break

            with open('conf/users.json', mode="w", encoding='utf-8-sig') as json_write_file:
                content = json.dumps(usersConfig, ensure_ascii=False, indent=4)
                json_write_file.write(content)
                json_write_file.close()

            json_read_file.close()

    except Exception as ex:
        logger.error(ex)


def getConfig(user):
    user.update({
        'headers': {
            'Host': 'm.dianping.com',
            "Origin": "http://s.dianping.com",
            'Referer': 'http://s.dianping.com/event/shenzhen',
        },
        'proxy': ''
    })

    return user



def getSystem():
    with open('conf/system.json', encoding='utf-8-sig') as json_file:
        sys = json.load(json_file)
        json_file.close()
        return sys    


def checkToken():
    msg = ""
    users = getUsers()
    for user in users:
        token = user["token"]
        if (not token or len(token) == 0):
            msg += "用户:{0} token失效,请重新获取;\r\n".format(user["phone"])

    if (len(msg) > 0):
        mail.send('点评霸王餐申请系统告警', msg)