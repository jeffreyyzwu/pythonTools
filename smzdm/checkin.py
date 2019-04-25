from log import logger
import request
from urllib.parse import unquote

def setQueryHeader(config):
    config.update({
        "headers": {
            "Host": "zhiyou.smzdm.com",
            "Referer": "https://www.smzdm.com/",
            "DNT": "1",
            "Accept-Encoding": "deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Cookie": config["token"]
        }})


def checkin(config):
    setQueryHeader(config)
    logger.info(config)

    url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
    response = request.openUrl(url, config, {})
    content = response.read().decode('utf-8')

    logger.info("张大妈签到结果:{0}".format(content))
