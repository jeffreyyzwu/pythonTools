import urllib.request
import json
import time
from bs4 import BeautifulSoup
import request
import config
from log import logger


# curl 'https://t.jd.com/follow/vender/qryCategories.do?qryKey=&_=1553005750094'
# -H 'Pragma: no-cache'
# -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate, br'
# -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8'
# -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
# -H 'Accept: */*'
# -H 'Cache-Control: no-cache'
# -H 'X-Requested-With: XMLHttpRequest'
# -H 'Cookie: __jdu=874504023; shshshfpa=d39a7919-c8c7-2717-cb0d-df50e2ad74dc-1547385653;
# shshshfpb=eE%2FsOqmZ1Lj4sz5vhixaOHw%3D%3D; pinId=36FUVsddcl8;
# __jdv=122270672|www.google.com.hk|-|referral|-|1552028982416;
# pin=letone; unick=clutch_888; _tp=1UaqQVSkw75T5LiZ9Qa1gw%3D%3D;
# _pst=letone; areaId=19; ipLoc-djd=19-1607-47388;
# PCSYCityID=1607; __jdc=122270672; ceshi3.com=201;
# __jda=122270672.874504023.1547385649.1552490416.1553004707.18;
# user-key=88b32452-4818-4ccf-be56-4344df848bc0; cn=0;
# shshshfp=e379b1281961d04be53c6305cf404a14;
# shshshsID=445855d52171ae55c7f6b313cdea08fb_1_1553004709264;
# 3AB9D23F7A4B3C9B=E6YQB6PYHTZW3OM7QWOQL2QFOTE4U6MSZVK6VMFRJIVY3DF4VUCVHHJXEGT5DKW72CVMOZ7K5TKPK2Z6KELWCIKQRI;
# wlfstk_smdl=vhsjvcnqxusxb0vyt03dbi3znpk3aes6;
# TrackID=1W1vt5OlIkD7KVXQWF5GjQ4VB3n5bAi4UNazTrz1Zq_6_A_7HGj3NAXdx2drQYk6vd1qdjt4BWYKrqpwzdnjMrKQiFvlCC57j5pC2Ev_8Ir8wSBnonCobZupoLlxfV6s0;
# thor=C25639EC8FACE8E393A35C0115A80C1ABD847EDDABCB4E9DB88E5458EDB813D32613D64F3C86D96CDD0C281E915660BEE6E227DC2E41B7414C7DE6A2B7D3DF9B22DC1CA8EDB443E63971260DFE2FFF746FBDB22D500A27F650FDEC2702AF2719370AF11D8CB847E7B1FE10C29D6AA780619756D99E3CE2ACE0D8970FB91E74E8;
# __jdb=122270672.12.874504023|18.1553004707'
# -H 'Connection: keep-alive'
# -H 'Referer: https://t.jd.com/vender/followVenderList.action' --compressed


def getFollowList(user):
    url = 'https://t.jd.com/follow/vender/qryCategories.do?qryKey=&_={0}'.format(
        time.time())
    follows = []
    setHeader(user)

    try:
        response = request.openUrl(url, user, {})
        content = str(response.read(), 'utf-8')
        decodeContent = json.loads(content)

        for category in decodeContent["data"]:
            for entry in category["entityIdSet"]:
                follows.append(entry)

    except Exception as ex:
        logger.error("获取店铺关注列表报错, url:{0}".format(url))
        logger.error(content)
        logger.error(ex)

    logger.info(follows)
    return follows


def setHeader(user):
    user["headers"].update({
        "Host": "t.jd.com",
        "Referer": "https://t.jd.com/vender/followVenderList.action"
    })


def removeFollow(user, vendor):
    url = 'https://t.jd.com/follow/vender/unfollow.do?venderId={0}&_={1}'.format(
        vendor, time.time())
    setHeader(user)

    try:
        response = request.openUrl(url, user, {})
        content = str(response.read(), 'utf-8')
        decodeContent = json.loads(content)
        logger.info(decodeContent)

    except Exception as ex:
        logger.error("取消店铺关注列表报错, url:{0}".format(url))
        logger.error(content)
        logger.error(ex)


def remove(user):
    follows = getFollowList(user)
    for follow in follows:
        removeFollow(user, follow)


# curl 'https://t.jd.com/follow/vender/unfollow.do?venderId=646566&_=1553005386125'
# -H 'Cookie: __jdu=874504023; shshshfpa=d39a7919-c8c7-2717-cb0d-df50e2ad74dc-1547385653;
# shshshfpb=eE%2FsOqmZ1Lj4sz5vhixaOHw%3D%3D; pinId=36FUVsddcl8;
# __jdv=122270672|www.google.com.hk|-|referral|-|1552028982416; pin=letone; unick=clutch_888;
# _tp=1UaqQVSkw75T5LiZ9Qa1gw%3D%3D; _pst=letone; areaId=19; ipLoc-djd=19-1607-47388;
# PCSYCityID=1607; __jdc=122270672; ceshi3.com=201; _
# _jda=122270672.874504023.1547385649.1552490416.1553004707.18;
# user-key=88b32452-4818-4ccf-be56-4344df848bc0; cn=0;
# shshshfp=e379b1281961d04be53c6305cf404a14;
# shshshsID=445855d52171ae55c7f6b313cdea08fb_1_1553004709264;
# 3AB9D23F7A4B3C9B=E6YQB6PYHTZW3OM7QWOQL2QFOTE4U6MSZVK6VMFRJIVY3DF4VUCVHHJXEGT5DKW72CVMOZ7K5TKPK2Z6KELWCIKQRI;
# wlfstk_smdl=vhsjvcnqxusxb0vyt03dbi3znpk3aes6;
# TrackID=1W1vt5OlIkD7KVXQWF5GjQ4VB3n5bAi4UNazTrz1Zq_6_A_7HGj3NAXdx2drQYk6vd1qdjt4BWYKrqpwzdnjMrKQiFvlCC57j5pC2Ev_8Ir8wSBnonCobZupoLlxfV6s0;
# thor=D166FD4657E3F918DC50DB39D7BC76C8AC46BA6F8A7006D881D5736F7C0F12FBA1934DC17AEDE52231F1009EEF59A703F248AB37A8B994C09FE11080367FFC087137B7407178F243263DA21056651ECB6C789A8783B98EC9AAA74E304C0B1D1F13966C65787F3686F11AC7EC5EA879015872491C5DEAE5F109FAB62035236A2F;
# __jdb=122270672.8.874504023|18.1553004707'
# -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate, br'
# -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8'
# -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
# -H 'Accept: */*' -H 'Referer: https://t.jd.com/vender/followVenderList.action'
# -H 'X-Requested-With: XMLHttpRequest'
# -H 'Connection: keep-alive' --compressed
