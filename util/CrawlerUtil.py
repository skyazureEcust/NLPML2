# 爬虫工具类
import time
import re
import xlrd
import xlwt
import datetime


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


# 读取Excel日期类型数据，返回datetime类型
def get_datetime_from_cell(s_cell):
    return xlrd.xldate.xldate_as_datetime(s_cell, 0)
