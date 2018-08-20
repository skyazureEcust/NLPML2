from dataprocess import RawDataProcessor
from util import CommonUtil
#     price_end_time), 2))
market_open_time = '09:30:00'
market_close_time = '23:30:00'
# print(CrawlerUtil.get_sample_time_list(market_open_time, market_close_time, 1))

time1 = '2016/06/06  23:30:00'
time2 = '2016/06/05  09:30:00'
# print(CrawlerUtil.get_interval_seconds(CrawlerUtil.get_datetime_from_string(time1), CrawlerUtil.get_datetime_from_string(time2)))
# dt_time = CrawlerUtil.get_datetime_from_string(time)
# dt_time_date = dt_time.date()
# print(str(dt_time_date))
# cur_time = str(CrawlerUtil.get_sample_time_list(market_open_time, market_close_time, 1)[0])
print(CommonUtil.get_next_sample_time(CommonUtil.get_datetime_from_string(time1),
                                      1, market_open_time, market_close_time))
