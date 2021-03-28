import config
import removefollow
import applyjdtry
from log import logger
import threading

def main():
    logger.info('----------------------------开始搬砖--------------------------------')

    users = config.getUsers()
    tasks=[]
    for user in users:
        user["headers"] = {}
        token = user["token"]
        if (token and len(token) > 0):
            task = threading.Thread(target=runTask,args=(user,))
            task.setDaemon(True)
            tasks.append(task)
            task.start()

    for task in tasks:
        task.join()
            
    config.checkToken()
    logger.info('--------全部报名结束-----------')

def runTask(user):
    logger.info('--------------账户切换成功:{0},开始报名--------------'.format(user["phone"]))

    removefollow.remove(user)
    applyjdtry.apply(user)

    logger.info('--------------账户:{0}报名结束--------------'.format(user["phone"]))


if __name__ == '__main__':
    main()