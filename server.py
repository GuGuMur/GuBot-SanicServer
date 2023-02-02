from sanic import Sanic
from sanic.response import file,json_dumps,json
from sanic_ext import Extend
import os
import requests
import regex as re
import httpx
import xmltodict
import pendulum
import ujson
import httpx
import feedparser
import xmltodict
import pendulum
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

app = Sanic("GuSanic")
Extend(app)

@app.get("api/prts/page_png/<page>")
async def PRTS_page_screenshot(request, page):
    po = get_topic_base(page)
    return await file(po)

def get_topic_base(pagename):
    filepath = f"""/home/bot/sanicserver/cache/prts_pic/{pagename}.png"""
    if (os.path.exists(filepath)) :
        os.remove(filepath)
    options = Options();DRIVER_PATH = r'/usr/bin/chromedriver'
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')  # 无头参数
    options.add_argument('--disable-gpu')  # 禁用gpu 防止占用资源出现bug
    options.add_argument('window-size=800x1000')  # 设置分窗口辨率
    options.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素可能会报错
    options.add_argument('--hide-scrollbars')
    driver = Chrome(options=options)

    driver.get(f"https://prts.wiki/w/{pagename}")
    element=driver.find_element(by=By.ID,value="mw-content-text")
    element.screenshot(filepath)
    return filepath

@app.get("/api/prts/rc/topic")
async def PRTS_topic_rc_deal(request):
    '''用于生成PRTS中topic页面的最近更改'''
    timeout = httpx.Timeout(10.0, connect=60.0, read=60.0, write=60.0, pool=60.0)
    async with httpx.AsyncClient(verify=False,timeout=timeout) as client:
        headers = {"User-Agent": "GuGuMur-GuBotAPI/1.0"}
        page = await client.post("https://prts.wiki/api.php?urlversion=2&days=5&limit=50&action=feedrecentchanges&feedformat=atom&namespace=2600", headers=headers)
        txt = xmltodict.parse(page.content)["feed"]["entry"]
        return_l = []
        group_member_list = ["永暮","NAAKII","AMUKnya","翱翔","爱吃鱼的牙同学","Enko","咕咕mur","Hjhk258","N2","RaYmondCheung","Visu2209","调零修罗","冬灵血巫大師"]
        for i in txt:
            if i['author']['name'] not in group_member_list:
                detail_j = {"title":i['title'],
                            "link":i['link']['@href'],
                            "author":i['author']['name']
                            }
                return_l.append(detail_j)
        return_t = ujson.dumps(return_l,ensure_ascii=False)
        return json(return_t,ensure_ascii=False,indent=4)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7954, access_log=False)