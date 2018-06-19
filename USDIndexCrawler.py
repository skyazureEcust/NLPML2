import sys
import requests
import json
import CrawlerLogger as CrawlerLogger
import CrawlerUtil as CrawlerUtil
# 根据时间段抓取美元指数
def getUSDIndex(data_type, data_count):
    urlPattern = 'https://forexdata.wallstreetcn.com/kline?prod_code=USDOLLARINDEX&candle_period=' \
                 + data_type + \
                 '&fields=time_stamp,open_px,close_px,high_px,low_px,ma5,ma10,ma20,ma60,upper,mid,' \
                 'lower,diff,dea,macd,k,d,j,rsi6,rsi12,rsi24&data_count=' \
                 + data_count  # 需要爬数据的网址

    logger.info(urlPattern)
    page = requests.Session().get(urlPattern)
    page.encoding = 'utf-8'
    fileContent = ''
    if page.status_code == 200:
        data_all = json.loads(page.text)
        res_data = data_all['data']
        candle_data = res_data['candle']
        # 处理标题
        data_fields = candle_data['fields']
        for item_i in range(len(data_fields)):
            fileContent += data_fields[item_i] + ','
        fileContent += '\n'
        # 处理数据
        data_list = candle_data['USDOLLARINDEX']
        for item_i in range(len(data_list)):
            data_items = data_list[item_i]
            data_item = ''
            for item_j in range(len(data_items)):
                # 日期格式转换
                if item_j == 0:
                    data_item += CrawlerUtil.convertLongToDate(data_items[item_j]) + ','
                else:
                    data_item += str(data_items[item_j]) + ','
            fileContent += data_item + '\n'

        logger.info("Finished With %s Items Crawled." % (len(data_list)))

    CrawlerUtil.saveToFile('output/USDIndex_%s.csv' % CrawlerUtil.getNow(), fileContent)


logger = CrawlerLogger.Logger("log/WallstreetcnCrwaler.log")
if(len(sys.argv) > 2):
    for num in range(1, 3):
        logger.info("parameter %d is %s " % (num, sys.argv[num]))
        if CrawlerUtil.integerCheck(sys.argv[num]):
            if num == 1:
                data_type = sys.argv[num]
            if num == 2:
                data_count = sys.argv[num]
        else:
            data_type = 8
            data_count = 256
            logger.warning('The Format of Argument \"%s\" Should Be A Integer like \"8\", Now Set To \"%s\", \"%s\"'
                           % (sys.argv[num], data_type, data_count))
else:
    data_type = 8
    data_count = 256
    logger.warning('The Number of Argument Should Be 2 like \"8 256\", Now Set To \"%s\", \"%s\"'
                   % (data_type, data_count))
getUSDIndex(data_type, data_count)
