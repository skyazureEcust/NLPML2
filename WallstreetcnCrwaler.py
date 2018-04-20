# coding=utf-8
import sys
import requests
import json
import CrawlerUtil as crawlerUtil
import CrawlerLogger as crawlerlogger


# 根据时间段抓取新闻数据
def getNewsItem(startDate, endDate):
    #从最新到最远获取新闻
    reverseYear = int(endDate[0:4])
    reverseMonth = int(endDate[4:6])
    reverseDay = int(endDate[6:8])
    reversePattern = (reverseYear, reverseMonth, reverseDay, 23, 59, 59, 99, 99, 99)
    reverseCursor = crawlerUtil.convertDateToLong(reversePattern)
    logger.info("reverseCursor is %s"%(reverseCursor))
    finishedYear = int(startDate[0:4])
    finishedMonth = int(startDate[4:6])
    finishedDay = int(startDate[6:8])
    finishedPattern = (finishedYear, finishedMonth, finishedDay, 0, 0, 0, 0, 0, 0)
    finishedCursor = crawlerUtil.convertDateToLong(finishedPattern)
    logger.info("finishedCursor is %s" % (finishedCursor))
    urlPattern='https://api-prod.wallstreetcn.com/apiv1/content/lives?channel=weex-channel,' \
               'gold-channel,gold-forex-channel,forex-channel,goldc-channel,oil-channel&client=pc' #需要爬数据的网址
    newsLimit = 100
    cursor = reverseCursor
    fileContent = ''
    # 页面计数器
    pageNum = 0
    # 循环开始
    while(int(cursor) > int(finishedCursor)):
        pageNum = pageNum + 1
        url = urlPattern + "&cursor=" + str(cursor) + "&" + str(newsLimit)
        logger.info(url)
        page=requests.Session().get(url)
        page.encoding = 'utf-8'
        if page.status_code == 200:
            data_all = json.loads(page.text)
            res_data = data_all['data']
            date_items = res_data['items']
            cursor = res_data['next_cursor']
            for item_i in range(len(date_items)):
                display_time = date_items[item_i]['display_time']
                context_text = date_items[item_i]['content_text']
                context = context_text.strip().replace('\n', '')
                context = context.replace('\r', '')
                time = crawlerUtil.convertLongToDate(display_time)
                fileContent = fileContent + time + "," + context + "\n"
                # print(item_i+1, ": " , time, ", ", context_text)
        crawlerUtil.saveToFile('output/Wallstreetcn_%s_%s.csv' % (startDate, endDate), fileContent)
        fileContent = ''
        # 无下一页数据时退出循环
        if cursor == '':
            break
    logger.info("Finished With %s Pages Crawled."%(pageNum))


logger = crawlerlogger.Logger("log/WallstreetcnCrwaler.log")
startDate = ''
endDate = ''
print("the script name is ", sys.argv[0])
if(len(sys.argv) > 2):
    for num in range(1, 3):
        logger.info("parameter %d is %s " % (num, sys.argv[num]))
        if crawlerUtil.dateCheck(sys.argv[num]):
            if num == 1:
                startDate = sys.argv[num]
            if num == 2:
                endDate = sys.argv[num]
        else:
            startDate = crawlerUtil.getToday()
            endDate = startDate
            logger.warning('The Format of Argument \"%s\" Should Be A Date like \"20180406\", Now Set To \"%s\", \"%s\"'
                           % (sys.argv[num], startDate, endDate))
else:
    startDate = crawlerUtil.getToday()
    endDate = startDate
    logger.warning('The Number of Argument Should Be 2 like \"20180406 20180408\", Now Set To \"%s\", \"%s\"'
                   % (startDate, endDate))

getNewsItem(startDate, endDate)
