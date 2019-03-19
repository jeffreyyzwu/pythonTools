import urllib.request
import random
import time
from log import logger

def randomSleep():
    stime = 0.3
    while stime < 0.5:
        stime = round(random.random() * 10 / 3.657, 3)

    logger.info('random sleep:{0}s'.format(stime))
    time.sleep(stime)


def randomUserAgent():
    agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)'
    ]
    index = random.randint(0, len(agents) - 1)
    return agents[index]


def setHeader(config):
    headers = config["headers"]
    headers["User-Agent"] = randomUserAgent()

    defaultHeaders = {
        "Pragma": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8;",
        "Accept": "application/json, text/javascript",
        "X-Requested-With": "XMLHttpRequest",
        'Cookie': "thor={0};".format(config["token"])
    }
    defaultHeaders.update(headers)
    config["headers"] = defaultHeaders


def openUrl(url, config, data):
    randomSleep()
    setHeader(config)

    req = urllib.request.Request(
        url=url,
        data=urllib.parse.urlencode(data).encode("utf-8"),
        headers=config["headers"]
    )
    response = urllib.request.urlopen(req)
    return response
