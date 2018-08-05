from dataprocess import RawDataProcessor
from util import CrawlerUtil

price_start_time = '2016/07/01  09:30:00'
current_price_time = '2016/07/13  15:10:56'
price_end_time = price_end_time = '2017/6/30  23:59:59'
print((CrawlerUtil.get_datetime_from_string(price_start_time) - CrawlerUtil.get_datetime_from_string(price_end_time)))
print(CrawlerUtil.get_datetime_from_string(price_start_time))
print(CrawlerUtil.get_datetime_from_string(price_end_time))
print(price_start_time < current_price_time < price_end_time)


current_time = '2016/07/01  10:44:42'
news_feature_time = '2016/09/14  10:20:15'
interval = CrawlerUtil.get_datetime_from_string(news_feature_time) - CrawlerUtil.get_datetime_from_string(current_time)

seconds = interval.days*24*3600 + interval.seconds
print(seconds)