from log import logger
import config


def saveUserConfig(user):
    config.saveUserConfig(user)


def refreshToken(user):
    logger.info("-----更新token-------")

    user["token"] = ''
    logger.info(user)

    if (token and len(token) == 0):
        logger.info('user:{0} login fail'.format(user["phone"]))
    else:
        saveUserConfig(user)
        logger.info('user:{0} login success, token:{1}'.format(
            user["phone"], token))

    return token


def getToken(user):
    token = ''
    if (user.__contains__('token')):
        token = user["token"]

    if ((not token) or len(token) == 0):
        token = refreshToken(user)

    return token
