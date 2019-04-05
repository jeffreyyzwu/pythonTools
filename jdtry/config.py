import json
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

