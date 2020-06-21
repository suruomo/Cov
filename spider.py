# -*- coding: utf-8 -*-
__author__ = 'suruomo'
__date__ = '2020/6/20 16:44'

import time
import json
import requests
from selenium.webdriver import Chrome, ChromeOptions


def get_tencent_data():
    url1 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"  # 总数据统计url
    url2 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"  # 历史数据统计url
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }
    r1 = requests.get(url1, headers)
    r2 = requests.get(url2, headers)

    res1 = json.loads(r1.text)
    res2 = json.loads(r2.text)

    data_all1 = json.loads(res1["data"])
    data_all2 = json.loads(res2["data"])

    # 获取历史数据
    history = {}
    for i in data_all2["chinaDayList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")  # 匹配时间
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式
        confirm = i["confirm"]  # 累计确诊
        suspect = i["suspect"]  # 现存疑似
        heal = i["heal"]  # 累计治愈
        dead = i["dead"]  # 累计死亡
        importedCase = i["importedCase"]  # 累计境外输入
        noInfect = i["noInfect"]  # 累计无症状感染
        history[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead, "importedCase": importedCase,
                       "noInfect": noInfect}
        print(history[ds])
    # 获取历史新增数据
    for i in data_all2["chinaDayAddList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")  # 匹配时间
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        importedCase = i["importedCase"]  # 累计境外输入
        noInfect = i["infect"]  # 累计无症状感染
        history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead,
                            "importedCase_add": importedCase, "noInfect_add": noInfect})

    # 获取详情数据
    details = []
    update_time = data_all1["lastUpdateTime"]
    data_country = data_all1["areaTree"]
    data_province = data_country[0]["children"]
    for pro_infos in data_province:
        province = pro_infos["name"]
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            suspect = city_infos["total"]["suspect"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([update_time, province, city, confirm, confirm_add, suspect, heal, dead])

    return history, details


# 爬取百度热搜数据：封装好函数
def get_baidu_hot():
    url = "https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1"
    # 隐藏浏览器：无头模式，不用每次打开浏览器
    option = ChromeOptions()
    option.add_argument("--headless")  # 隐藏游览器
    option.add_argument("--no--sandbox")
    browser = Chrome(options=option, executable_path="chromedriver.exe")
    browser.get(url)
    # 必须要用单引号!!!
    # 查看更多按钮，获取全部20条数据
    but = browser.find_element_by_css_selector(
        '#ptab-0 > div > div.VirusHot_1-5-6_32AY4F.VirusHot_1-5-6_2RnRvg > section > div')
    but.click()
    time.sleep(1)  # 等待一秒
    c = browser.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[1]/section/a/div/span[2]')
    context = [i.text for i in c]
    browser.close()
    return context
