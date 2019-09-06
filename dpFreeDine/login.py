from log import logger
# from dpaccount import DianPingAccount
import config


def saveUserConfig(user):
    config.saveUserConfig(user)


def refreshToken(user):
    logger.info("-----更新token-------")
    token = ''

    return token


def getToken(user):
    token = ''
    if (user.__contains__('token')):
        token = user["token"]

    if ((not token) or len(token) == 0):
        token = refreshToken(user)

    return token
