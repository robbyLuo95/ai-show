import requests
from selenium.webdriver.common.touch_actions import TouchActions
from selenium import webdriver
from selenium.webdriver import ChromeOptions

import time
import datetime


def main():
    option = ChromeOptions()
    # 无界面模式
    # option.add_argument('--headless')
    # option.add_argument("--disable-blink-features=AutomationControlled")
    # option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # option.add_experimental_option('useAutomationExtension', False)
    # option.add_experimental_option('excludeSwitches', ['enable-logging'])
    # driver = webdriver.Chrome(executable_path='<path-to-chrome>', options=option)
    sel = webdriver.Chrome(options=option)
    # sel.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    # })
    sel.maximize_window()
    url = "http://localhost:5003/upload"
    request_url = {
        'https://www.591.com.hk/',
        'https://sale.591.com.hk/',
        'https://rent.591.com.hk/'
    }
    today = datetime.date.today().strftime('%y%m%d')
    msg = ''
    i = 0
    for u in request_url:
        sel.get(u)
        time.sleep(10)
        img = sel.get_screenshot_as_png()
        img_name = str(today) + str(i) + '.png'
        file = {'file': (img_name, img, 'image/png', {})}
        res = requests.request("POST", url, data={'name': 'final'}, files=file)
        data = res.json()
        if data['image_info'] != {}:
            for k, v in data['image_info'].items():
                msg += '检测类别：' + k + ';置信度为' + str(v[1]) + ';结果图片url为' + data['draw_url'] + "\n"
        i += 1
    if msg != "":
        send(msg)


def find_error():
    mobileEmulation = {'deviceName': 'iPhone X'}
    options = webdriver.ChromeOptions()
    options.add_experimental_option('mobileEmulation', mobileEmulation)
    sel = webdriver.Chrome(chrome_options=options)
    request_url = {
        # 'https://sale.591.com.hk/',
    }
    ocr_request_url = {
        'https://newhouse.debug.591.com.hk/newhouse/detail/4680'
    }
    today = datetime.date.today().strftime('%y%m%d')
    msg = ''
    i = 0
    for u in request_url:
        sel.get(u)
        time.sleep(20)
        img = sel.get_screenshot_as_png()
        img_name = str(today) + str(i) + '.png'
        file = {'file': (img_name, img, 'image/png', {})}
        message = yolo_find(u, file)
        msg += message
        i += 1
    for orc_u in ocr_request_url:
        sel.get(orc_u)
        time.sleep(20)
        img = sel.get_screenshot_as_png()
        img_name = str(today) + str(i) + '.png'
        file = {'file': (img_name, img, 'image/png', {})}
        message = orc_find(orc_u, file)
        msg += message
        i += 1
    if msg != "":
        send(msg)


def yolo_find(request_url, file):
    msg = ''
    url = "http://localhost:5003/upload"
    t = time.time()
    print(t)
    res = requests.request("POST", url, data={'name': 'error'}, files=file)
    print(time.time() - t)
    data = res.json()
    if data['image_info'] != {}:
        c = ''
        z = ''
        for k, v in data['image_info'].items():
            if len(c) == 0:
                c = k
            else:
                c = c + ',' + k
            if len(z) == 0:
                z = str(v[1])
            else:
                z = z + ',' + str(v[1])
        msg = request_url + '发现错误；检测错误类别：' + c + ';置信度为' + z + ';结果图片url为http://localhost:5003/' + data['draw_url'] + "\n"
    return msg


def orc_find(request_url, file):
    url = "http://localhost:5003/orc/upload"
    t = time.time()
    print(t)
    res = requests.request("POST", url, data={'name': 'error'}, files=file)
    print(time.time() - t)
    data = res.json()
    msg = ''
    for e in data['image_info']:
        print(e)
        if '服務器出了點間題' in e:
            msg = request_url + '发现错误；结果图片url为http://localhost:5003/' + data['draw_url'] + "\n"
    return msg


def send(msg, users="10865", title="数据检测"):
    for user in users.split(","):
        data = {
            "alertid": 47,
            "alertuser": user,
            "title": title,
            "msg": msg
        }
        url = r"http://eagle.591.com.tw/jalert/alert_action"
        requests.post(url, data)


if __name__ == '__main__':
    find_error()
    # main()
