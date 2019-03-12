import time
from selenium import webdriver
import json
from log import logger

# chromedriver download address
# https://chromedriver.storage.googleapis.com/index.html

def login(user):
    option = webdriver.ChromeOptions()
    # option.add_argument('--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data')
    #option.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
    # option.add_argument('--proxy-server=http://171.37.135.94:8123')
    browser = webdriver.Chrome(
        chrome_options=option,  executable_path=r'./chromedriver')
    token = ''
    try:
        browser.get('https://www.dianping.com/login')
        browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
        accountbutton = browser.find_element_by_css_selector(
            'div.bottom-area span.bottom-password-login')
        accountbutton.click()

        iphonebutton = browser.find_element_by_id('tab-account')
        iphonebutton.click()

        uinput = browser.find_element_by_id('account-textbox')
        uinput.send_keys(user["phone"])
        pinput = browser.find_element_by_id('password-textbox')
        pinput.send_keys(user['password'])
        button = browser.find_element_by_id('login-button-account')
        button.click()

        time.sleep(5)
        # print(browser.page_source)
        # print(browser.current_url)
        # print(browser.get_cookies())

        for cookie in browser.get_cookies():
            # print('name='+cookie["name"])
            # print('value='+cookie["value"])
            if ("dper" == cookie["name"]):
                token = cookie["value"]

    finally:
        browser.close()

    return token


def getToken(user):
    token = ''
    if (user.__contains__('token')):
        token = user["token"]

    if (len(token) == 0):
        token = login(user)

    user["token"] = token
    if (len(token) == 0):
        logger.info('user:{0} login fail'.format(user["phone"]))
    else:
        logger.info('user:{0} login success, token:{1}'.format(user["phone"], token))

    return token
