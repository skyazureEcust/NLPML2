import sys
import requests
import json
from util import CrawlerUtil as CrawlerUtil, CrawlerLogger as CrawlerLogger


# 根据时间段抓取美元指数
def get_usd_cny(p_type, p_count):
    url_pattern = 'https://forexdata.wallstreetcn.com/kline?prod_code=USDCNY&candle_period=' \
                 + str(p_type) + \
                 '&fields=time_stamp,open_px,close_px,high_px,low_px,ma5,ma10,ma20,ma60,upper,mid,' \
                 'lower,diff,dea,macd,k,d,j,rsi6,rsi12,rsi24&data_count=' \
                 + str(p_count)  # 需要爬数据的网址
    logger.info(url_pattern)
    page = requests.Session().get(url_pattern)
    page.encoding = 'utf-8'
    file_content = ''
    if page.status_code == 200:
        data_all = json.loads(page.text)
        res_data = data_all['data']
        candle_data = res_data['candle']
        # 处理标题
        data_fields = candle_data['fields']
        for item_i in range(len(data_fields)):
            file_content += data_fields[item_i] + ','
            file_content += '\n'
        # 处理数据
        data_list = candle_data['USDCNY']
        for item_i in range(len(data_list)):
            data_items = data_list[item_i]
            data_item = ''
            for item_j in range(len(data_items)):
                # 日期格式转换
                if item_j == 0:
                    data_item += CrawlerUtil.convert_long_to_date(data_items[item_j]) + ','
                else:
                    data_item += str(data_items[item_j]) + ','
                    file_content += data_item + '\n'

        logger.info("Finished With %s Items Crawled." % (len(data_list)))

    CrawlerUtil.save_to_file('output/USDCNY_%s.csv' % CrawlerUtil.get_now(), file_content)


logger = CrawlerLogger.Logger("logs/USDCNYCrwaler.log")
data_type = 0
data_count = 0
if len(sys.argv) > 2:
    for num in range(1, 3):
        logger.info("parameter %d is %s " % (num, sys.argv[num]))
        if CrawlerUtil.check_integer(sys.argv[num]):
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
get_usd_cny(data_type, data_count)