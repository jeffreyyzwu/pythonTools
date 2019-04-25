import config
import removefollow
import applyjdtry
from log import logger
from jdlogin import *

def main():
    logger.info('----------------------------开始搬砖--------------------------------')

    users = config.getUsers()
    for user in users:
        user["headers"]={}
        jd = jdlogin(user)
        jd.login()

    #     token = user["token"]
    #     if (token and len(token) > 0):
    #         logger.info('--------------用户切换成功:{0},开始报名--------------'.format(user["phone"]))

    #         # removefollow.remove(user)
    #         if (user.get("apply", "true") == "true"):
    #             applyjdtry.apply(user)

    #         logger.info('--------------用户:{0}报名结束--------------'.format(user["phone"]))

    # config.checkToken()
    logger.info('--------全部报名结束-----------')

if __name__ == '__main__':
    main()