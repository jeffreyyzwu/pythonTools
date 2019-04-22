import config
import login
import freedine
import freebeautytry
import freecheckin
from log import logger

def main():
    logger.info('----------------------------开始搬砖--------------------------------')
    users = config.getUsers()
    for user in users:
        token = login.getToken(user)
        if (token and len(token) > 0):
            logger.info('--------------用户切换成功:{0},开始报名--------------'.format(user["phone"]))

            freecheckin.checkin(user)
            freedine.fetchFreeDine(user)
            freebeautytry.fetchFreeBeautyTry(user)

            logger.info('--------------用户:{0}报名结束--------------'.format(user["phone"]))

    config.checkToken()
    logger.info('--------全部报名结束-----------')

if __name__ == '__main__':
    main()