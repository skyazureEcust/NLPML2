from dataprocess import RawDataProcessor
from util import CrawlerUtil
from datetime import datetime
from datetime import timedelta
price_begin_time = '2017/06/30  03:26:01'
price_end_time = '2017/06/30  23:59:00'
# print(CrawlerUtil.get_interval_minutes(CrawlerUtil.get_datetime_from_string(
#     price_end_time), CrawlerUtil.get_datetime_from_string(price_begin_time)))
# print(CrawlerUtil.get_datetime_from_string(
#     price_end_time)-timedelta(minutes=2))
#
# print(CrawlerUtil.get_minute_changed(CrawlerUtil.get_datetime_from_string(
#     price_end_time), 2))
market_open_time = '09:30:00'
market_close_time = '23:30:00'
# print(CrawlerUtil.is_in_market_close(price_begin_time, market_open_time, market_close_time))

print(CrawlerUtil.reset_news_time(price_end_time, 1, market_open_time, market_close_time))

print(CrawlerUtil.reset_news_time(price_begin_time, 2, market_open_time, market_close_time))
