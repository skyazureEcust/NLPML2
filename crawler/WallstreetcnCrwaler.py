# coding=utf-8
import sys
import requests
import json
from util import CrawlerUtil as CrawlerUtil, CrawlerLogger as CrawlerLogger


# 根据时间段抓取新闻数据
def get_news_item(start_date, end_date):
    # 从最新到最远获取新闻
    reverse_year = int(end_date[0:4])
    reverse_month = int(end_date[4:6])
    reverse_day = int(end_date[6:8])
    reverse_pattern = (reverse_year, reverse_month, reverse_day, 23, 59, 59, 99, 99, 99)
    reverse_cursor = CrawlerUtil.convert_date_to_long(reverse_pattern)
    logger.info("reverseCursor is %s" % reverse_cursor)
    finished_year = int(start_date[0:4])
    finished_month = int(start_date[4:6])
    finished_day = int(start_date[6:8])
    finished_pattern = (finished_year, finished_month, finished_day, 0, 0, 0, 0, 0, 0)
    finished_cursor = CrawlerUtil.convert_date_to_long(finished_pattern)
    logger.info("finishedCursor is %s" % finished_cursor)
    # 需要爬数据的网址
    url_pattern = 'https://api-prod.wallstreetcn.com/apiv1/content/lives?' \
                  'channel=weex-channel,gold-channel,gold-forex-channel,' \
                  'forex-channel,goldc-channel,oil-channel&client=pc'
    news_limit = 100
    cursor = reverse_cursor
    file_content = ''
    # 页面计数器
    page_num = 0
    # 循环开始
    while int(cursor) > int(finished_cursor):
        page_num += 1
        url = url_pattern + "&cursor=" + str(cursor) + "&" + str(news_limit)
        logger.info(url)
        page = requests.Session().get(url)
        page.encoding = 'utf-8'
        if page.status_code == 200:
            data_all = json.loads(page.text)
            res_data = data_all['data']
            data_items = res_data['items']
            cursor = res_data['next_cursor']
            for item_i in range(len(data_items)):
                display_time = data_items[item_i]['display_time']
                context_text = data_items[item_i]['content_text']
                context = context_text.strip().replace('\n', '')
                context = context.replace('\r', '')
                time = CrawlerUtil.convert_long_to_date(display_time)
                file_content = file_content + time + "," + context + "\n"
                # print(item_i+1, ": " , time, ", ", context_text)
        CrawlerUtil.save_to_file('output/wallstreetcn_%s_%s.csv' % (start_date, end_date), file_content)
        file_content = ''
        # 无下一页数据时退出循环
        if cursor == '':
            break
    logger.info("Finished With %s Pages Crawled." % page_num)


logger = CrawlerLogger.Logger("logs/wallstreetcn_crawler.log")
startDate = ''
endDate = ''
print("the script name is ", sys.argv[0])
if len(sys.argv) > 2:
    for num in range(1, 3):
        logger.info("parameter %d is %s " % (num, sys.argv[num]))
        if CrawlerUtil.check_date(sys.argv[num]):
            if num == 1:
                startDate = sys.argv[num]
            if num == 2:
                endDate = sys.argv[num]
        else:
            startDate = CrawlerUtil.get_today()
            endDate = startDate
            logger.warning('The Format of Argument \"%s\" Should Be A Date like \"20180406\", Now Set To \"%s\", \"%s\"'
                           % (sys.argv[num], startDate, endDate))
else:
    startDate = CrawlerUtil.get_today()
    endDate = startDate
    logger.warning('The Number of Argument Should Be 2 like \"20180406 20180408\", Now Set To \"%s\", \"%s\"'
                   % (startDate, endDate))

get_news_item(startDate, endDate)
