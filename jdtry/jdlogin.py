# -*- coding:utf-8 -*-

import time
import json
import config
from bs4 import BeautifulSoup
from log import logger
from selenium import webdriver

# chromedriver download address
# https://chromedriver.storage.googleapis.com/index.html


class jdlogin:
    def __init__(self):
        self.users = config.getUsers()


    def _login_account_token(self, user):
        token = ''
        option = webdriver.ChromeOptions()
        # 隐私模式
        option.add_argument('--incognito')
        # option.add_argument('--headless')
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        option.add_experimental_option('excludeSwitches', ['enable-automation']) 
        browser = webdriver.Chrome(chrome_options=option,  executable_path=r'./chromedriver')
        
        try:
            browser.get('https://passport.jd.com/new/login.aspx')
            accountbutton = browser.find_element_by_css_selector(
                'div.login-tab.login-tab-r a')
            accountbutton.click()
            # time.sleep(3)

            uinput = browser.find_element_by_id('loginname')
            uinput.send_keys(user["phone"])
            time.sleep(2)

            pinput = browser.find_element_by_id('nloginpwd')
            pinput.send_keys(user['password'])
            time.sleep(1)

            button = browser.find_element_by_id('loginsubmit')
            button.click()
            time.sleep(35)

            for cookie in browser.get_cookies():
                print(cookie)
                # print('name='+cookie["name"])
                # print('value='+cookie["value"])
                if ("thor" == cookie["name"] and ".jd.com" == cookie["domain"]):
                    token = cookie["value"]

        finally:
            browser.close()

        return token

    def _get_current_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    def refresh_token(self):
        if (len(self.users) == 0):
            logger.info("获取用户信息失败")
            return

        for user in self.users:
            token = user["token"]
            if (len(token) == 0):
                time.sleep(3)

                token = self._login_account_token(user)
                if (len(token) == 0):
                    logger.error('获取用户[{0}]token失败'.format(user["phone"]))
                    return
                user["token"] = token
                user["time"] = self._get_current_time()
                logger.info(user)
                config.saveUserConfig(user)
                logger.info('获取用户[{0}]token成功,token:[{1}]'.format(user["phone"], user["token"]))
    

        
if __name__ == '__main__':
    login = jdlogin()
    login.refresh_token()




