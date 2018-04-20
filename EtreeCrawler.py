import requests
from lxml import etree
from lxml import html
url='https://wallstreetcn.com/live/forex' #需要爬数据的网址
page=requests.Session().get(url)
selector=etree.HTML(page)
newsList=selector.xpath('//div[@class="live-item score-2"]')
