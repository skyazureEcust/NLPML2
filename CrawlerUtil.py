# 爬虫工具类
import time
import re


# 时间格式转换Long：Date
def convertLongToDate(longTime):
    timeLocal = time.localtime(longTime)
    # 转换成新的时间格式(2018-04-06 20:28:54)
    date = time.strftime("%Y-%m-%d %H:%M:%S", timeLocal)
    return date

# 时间格式转换Date：Long
def convertDateToLong(date):
    timestamp = int(time.mktime(date))
    return timestamp

# 保存为文件
def saveToFile(file_name, contents):
    #追加写文件
    fh = open(file_name, 'a', encoding="utf-8")
    fh.write(contents)
    fh.close()

# 参数是否为日期格式：20180406
def dateCheck(sDate):
    match = re.search("\d{4}\d{2}\d{2}", sDate)
    if match:
        return True
    else:
        return False

# 参数是否为数字：1
def integerCheck(sInt):
    return sInt.isdigit()

# 获取今天的日期
def getToday():
    return time.strftime('%Y%m%d', time.localtime(time.time()))

# 获取现在的日期
def getNow():
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
