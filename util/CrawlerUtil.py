# 爬虫工具类
import time
import re
import xlrd
import xlwt
import datetime
import csv


# 时间格式转换Long：Date
def convert_long_to_date(l_time):
    time_local = time.localtime(l_time)
    # 转换成新的时间格式(2018-04-06 20:28:54)
    date = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return date


# 时间格式转换Date：Long
def convert_date_to_long(d_date):
    timestamp = int(time.mktime(d_date))
    return timestamp


# 保存为文件
def save_to_file(s_file_name, s_content):
    # 追加写文件
    fh = open(s_file_name, 'a', encoding="utf-8")
    fh.write(s_content)
    fh.close()


# 参数是否为日期格式：20180406
def check_date(s_date):
    match = re.search("\d{4}\d{2}\d{2}", s_date)
    if match:
        return True
    else:
        return False


# 参数是否为数字：1
def check_integer(s_int):
    return s_int.isdigit()


# 获取今天的日期
def get_today():
    return time.strftime('%Y%m%d', time.localtime(time.time()))


# 获取现在的日期
def get_now():
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


# 字符串转时间
def get_datetime_from_string(s_str):
    return datetime.datetime.strptime(s_str, '%Y/%m/%d  %H:%M:%S')


# 把datetime转成字符串
def get_string_from_datetime(dt_time):
    return dt_time.strftime("%Y/%m/%d  %H:%M:%S")


# 读取Excel文件
def read_excel(s_path):
    return xlrd.open_workbook(s_path)


# 数据保存为Excel文件
def write_excel(s_filename, list_time, list_data):
    # 创建excel对象
    book = xlwt.Workbook()
    # 添加一个表
    sheet = book.add_sheet('Sheet1')
    i = 0
    for row_item in list_data:
        sheet.write(i, 0, get_string_from_datetime(list_time[i]))
        j = 1
        for item in row_item:
            sheet.write(i, j, item)
            j += 1
        i += 1
    # 保存excel
    book.save(s_filename)


# 读取csv文件
def read_csv(s_path):
    with open(s_path) as csv_file:
        reader = csv.reader(csv_file)
        return list(reader)


# 读取csv文件，返回reader
def reader_csv(s_path):
    with open(s_path) as csv_file:
        reader = csv.reader(csv_file)
        return reader


# 保存为csv文件
def write_csv(s_filename, list_data):
    # 使用数字和字符串的数字都可以
    with open(s_filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in list_data:
            writer.writerow(row)


# 读取Excel日期类型数据，返回datetime类型
def get_datetime_from_cell(s_cell):
    return xlrd.xldate.xldate_as_datetime(s_cell, 0)


# 比较两个时间相差的秒数
def get_interval_seconds(dt_time1, dt_time2):
    interval = dt_time1 - dt_time2
    interval_seconds = interval.days * 24 * 3600 + interval.seconds
    return interval_seconds


# 获得标准采样时间点,1：1分钟，5：5分钟，10：10分钟
def get_sample_time(dt_time, i_minute):
    if i_minute == 1:
        time_year = dt_time.year
        time_month = dt_time.month
        time_day = dt_time.day
        time_hour = dt_time.hour
        time_minute = dt_time.minute
        sample_time = datetime.datetime(time_year, time_month, time_day, time_hour, time_minute)
        return sample_time


# 获得调整后的时间
def get_minute_changed(dt_time, i_minute):
    new_time = dt_time + datetime.timedelta(minutes=i_minute)
    return new_time


# 判断时间是否在闭市范围
def is_in_market_close(s_date_time, s_market_open, s_market_close):
    current_time = get_datetime_from_string(s_date_time).time()
    market_open_time = datetime.datetime.strptime(s_market_open, '%H:%M:%S').time()
    market_close_time = datetime.datetime.strptime(s_market_close, '%H:%M:%S').time()
    if current_time > market_close_time or current_time < market_open_time:
        return True
    else:
        return False


# 根据新闻时间重设时间
def reset_news_time(s_news_time, i_adjust, s_market_open, s_market_close):
    news_date_time = get_datetime_from_string(s_news_time)
    current_time = news_date_time.time()
    market_open_time = datetime.datetime.strptime(s_market_open, '%H:%M:%S').time()
    market_close_time = datetime.datetime.strptime(s_market_close, '%H:%M:%S').time()
    # 闭市之后，00:00之前，日期增加一天，再设置时间
    if current_time > market_close_time:
        new_time_temp = news_date_time + datetime.timedelta(days=1)
        new_date = new_time_temp.date()
        new_news_time = new_date.strftime('%Y/%m/%d') + '  ' + s_market_open
        new_news_time_adjusted = get_datetime_from_string(new_news_time) - datetime.timedelta(minutes=i_adjust)
        return get_string_from_datetime(new_news_time_adjusted)
    # 开市之前，只需设置时间
    elif current_time < market_open_time:
        new_date = news_date_time.date()
        new_news_time = new_date.strftime('%Y/%m/%d') + '  ' + s_market_open
        new_news_time_adjusted = get_datetime_from_string(new_news_time) - datetime.timedelta(minutes=i_adjust)
        return get_string_from_datetime(new_news_time_adjusted)
    else:
        return s_news_time
