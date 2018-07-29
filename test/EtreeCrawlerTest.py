import requests
from lxml import etree

# 需要爬数据的网址
url = 'https://wallstreetcn.com/live/forex'
page = requests.Session().get(url)
selector = etree.HTML(page)
newsList = selector.xpath('//div[@class="live-item score-2"]')
