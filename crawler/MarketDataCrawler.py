import requests
import json
from util import CommonUtil, LogHelper


MARKET_DATA_PATH = '../files/marketdata'
logger = LogHelper.Logger("../logs/MarketDataCrawler.log")
# 根据时间段抓取市场行情数据
# data_type：USDOLLARINDEX（美元指数）、USDCNY（在岸人民币）、EURUSD（欧元/美元）、USDCNH（离岸人民币）、USDJPY（美元/日元）、GBPUSD（英镑/美元）、USDCAD（美元/加元）
# XAUUSD（黄金）、UKOIL（布伦特原油）、UKOIL（WTI原油）、XAGUSD（白银）
# 000001（上证指数）、399001（深证成指）、SPX500INDEX（标普500）、NASINDEX（纳斯达克）、HKG33INDEX（恒生指数）、
# US10YEAR（美国10年期国债）、CHINA10YEAR（中国10年期国债）
# CHINA50（富时中国A50股指期货）、HKG33（恒生指数期货）、SPX500（标普500指数期货）、NAS100（纳斯达克100指数期货）
# i_type：1（1m）、2（5m）、3（15m）、4（30m）、5（1H）、7（4H）、8（1D）、10（1W）、11（1M）
# i_count：爬取的记录数，最大为1000
def get_market_data(i_type, i_count, s_data_type):
    url_pattern = 'https://forexdata.wallstreetcn.com/kline?prod_code=' + s_data_type + \
                  '&candle_period=' + str(i_type) + \
                  '&fields=time_stamp,open_px,close_px,high_px,low_px,ma5,ma10,ma20,ma60,upper,mid,lower,diff,dea,' \
                  'macd,k,d,j,rsi6,rsi12,rsi24&data_count=' + str(i_count)  # 需要爬数据的网址
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
        data_list = candle_data[s_data_type]
        for item_i in range(len(data_list)):
            data_items = data_list[item_i]
            data_item = ''
            for item_j in range(len(data_items)):
                # 日期格式转换
                if item_j == 0:
                    data_item += CommonUtil.convert_long_to_date(data_items[item_j]) + ','
                else:
                    data_item += str(data_items[item_j]) + ','
            file_content += data_item + '\n'
        logger.info("Finished With %s Items Crawled." % (len(data_list)))
        CommonUtil.save_to_file(MARKET_DATA_PATH + '/%s.csv' % s_data_type, file_content)
    else:
        logger.warning("Response Code is %s, Please Check!" % page.status_code)



# time_type = 5
# data_count = 1000
# data_type = 'USDCNY'
# get_market_data(time_type, data_count, data_type)

# if len(sys.argv) > 2:
#     for num in range(1, 3):
#         logger.info("parameter %d is %s " % (num, sys.argv[num]))
#         if CommonUtil.check_integer(sys.argv[num]):
#             if num == 1:
#                 data_type = sys.argv[num]
#             if num == 2:
#                 data_count = sys.argv[num]
#         else:
#             data_type = 8
#             data_count = 256
#             logger.warning('The Format of Argument \"%s\" Should Be A Integer like \"8\", Now Set To \"%s\", \"%s\"'
#                            % (sys.argv[num], data_type, data_count))
# else:
#     data_type = 8
#     data_count = 256
#     logger.warning('The Number of Argument Should Be 2 like \"8 256\", Now Set To \"%s\", \"%s\"'
#                    % (data_type, data_count))
