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

