# -*- coding: UTF-8 -*-

import requests
import time
import json
import zlib
import base64
import random

from log import logger
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class DianPingAccount:
    _check_risk_url = 'https://account.dianping.com/account/ajax/checkRisk'
    _login_url = 'https://account.dianping.com/account/ajax/passwordLogin'

    def __init__(self, user):
        super(DianPingAccount, self).__init__()
        self._phone = user["phone"]
        self._password = user["password"]

        self._headers = {
            'Host': 'account.dianping.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'https://account.dianping.com/account/iframeLogin?callback=EasyLogin_frame_callback0&wide=false&protocol=https:&redir=http%3A%2F%2Fwww.dianping.com%2F',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Origin':  'https://account.dianping.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'DNT': '1'
        }
        self.session = None
        self._token_dict = None

    def _gen_token_dict(self):
        self._token_dict = {
            "rId": "100049",
            "ver": "1.0.6",
            "brVD": [290, 375],
            "brR": [[1680, 1050], [1680, 947], 24, 24],
            "bI": [
                "https://account.dianping.com/account/iframeLogin?callback=EasyLogin_frame_callback0&wide=false&protocol=https:&redir=http%3A%2F%2Fwww.dianping.com%2F",
                "https://account.dianping.com/login?redir=http%3A%2F%2Fwww.dianping.com%2F"
            ],
            "mT": ["212,246", "212,246", "212,246", "212,246", "212,246", "212,246", "212,247", "212,247", "212,247", "213,247",
                   "213,247", "214,247", "215,247", "216,247", "218,247", "219,247", "222,247", "226,247", "230,247", "234,248",
                   "240,248", "245,249", "249,249", "256,250", "263,251", "269,251", "274,251", "280,251", "284,251", "285,251"],
            "kT": ["4,INPUT", "1,INPUT", "3,INPUT", "1,INPUT", "0,INPUT", "2,INPUT", "O,INPUT", "K,INPUT", "I,INPUT", "\u0012,INPUT", "[,INPUT"],
            "aT": ["212,246,BUTTON", "103,234,BUTTON", "72,257,BUTTON", "95,163,INPUT", "155,165,INPUT", "174,113,INPUT", "202,52,A", "145,349,SPAN"],
            "tT": [],
            "aM": ""
        }

    def _gen_token(self, encrypted_passwd):
        if not self._token_dict:
            self._gen_token_dict()

        dict = self._token_dict
        dict["cts"] = int(time.time() * 1000)
        dict["ts"] = dict["cts"] - random.randint(10000, 50000)
        if (len(encrypted_passwd) == 0):
            dict["sign"] = self._gen_check_risk_sign()
        else:
            dict["sign"] = self._gen_login_sign(encrypted_passwd)

        return self._b64encode(dict)

    def _gen_check_risk_sign(self):
        data = "riskChannel=201&user={0}".format(self._phone)
        return self._b64encode(data)

    def _gen_login_sign(self, encrypted_passwd):
        data = "countrycode=86&encryptPassword={0}&keepLogin=on&username={1}".format(
            encrypted_passwd, self._phone)
        return self._b64encode(data)

    def _b64encode(self, data):
        json_str = json.dumps(data, separators=(',', ':'))
        input_byte = bytearray(str(json_str), 'UTF-8')
        zlibbed_str = zlib.compress(input_byte)
        result = base64.b64encode(zlibbed_str).decode('ascii')

        return result

    def _get_check_risk_data(self):
        data = {
            'riskChannel': 201,
            'user': self._phone,
            '_token': self._gen_token('')
        }

        return data

    def _encrypt(self, input_str, public_key):
        public_key = '-----BEGIN PUBLIC KEY-----\n' + \
            public_key + '\n-----END PUBLIC KEY-----'
        rsa = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(rsa)
        ciphertext = cipher.encrypt(input_str.encode('utf8'))
        return base64.b64encode(ciphertext).decode('ascii')

    def _get_login_data(self, public_key, uuid):
        data_arr = [self._password, uuid]
        data_str = json.dumps(data_arr, separators=(',', ':'))
        encrypted_passwd = self._encrypt(data_str, public_key)

        return {
            'countrycode': 86,
            'encryptPassword': encrypted_passwd,
            'keepLogin': 'on',
            'username': self._phone,
            '_token': self._gen_token(encrypted_passwd)
        }

    def login(self):
        token = ''
        try:
            token = self._user_login()
        except Exception as ex:
            logger.error("模拟登录失败")
            logger.error(ex)

        return token

    def _user_login(self):
        self.session = requests.Session()
        r = self.session.post('https://account.dianping.com/account/ajax/checkRisk',
                              headers=self._headers,
                              data=self._get_check_risk_data(),
                              verify=False
                              )
        r_dict = json.loads(r.text)
        logger.info("login check risk response:{}".format(r_dict))

        public_key = r_dict and r_dict['msg'] and r_dict['msg']['publicKey']
        if not public_key:
            print("Error: Cannot get public key!")
            return ''

        uuid = r_dict and r_dict['msg'] and r_dict['msg']['uuid']
        if not uuid:
            print("Error: Cannot get uuid!")
            return ''

        print('check risk success, public key:{0}, uuid:{1}'.format(
            public_key, uuid))

        r = self.session.post(self._login_url,
                              headers=self._headers,
                              data=self._get_login_data(public_key, uuid),
                              verify=False
                              )
        logger.info("dp login response content:{}".format(r.json()))

        if not r or not r.cookies:
            logger.error("Error: Login failed!")
            return ''

        if r and r.cookies:
            logger.info(r.cookies)
            for (k, v) in r.cookies.items():
                if (k == "dper"):
                    return v

        return ''
