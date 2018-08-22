from crawler import MarketDataCrawler
from util import CommonUtil
import time

# 'USDOLLARINDEX', 'EURUSD', 'USDCNH', 'USDJPY', 'GBPUSD', 'USDCAD', 'XAUUSD', 'UKOIL', 'XAGUSD', '000001', '399001', 'SPX500INDEX', 'NASINDEX', 'HKG33INDEX', 'US10YEAR', 'CHINA10YEAR', 'CHINA50', 'HKG33', 'SPX500', 'NAS100'
FEATURE_NAME_LIST = {'USDOLLARINDEX', 'EURUSD', 'USDCNH', 'USDJPY', 'GBPUSD', 'USDCAD', 'XAUUSD', 'UKOIL', 'XAGUSD', '000001', '399001', 'SPX500INDEX', 'NASINDEX', 'HKG33INDEX', 'US10YEAR', 'CHINA10YEAR', 'CHINA50', 'HKG33', 'SPX500', 'NAS100'}
VALUE_NAME = 'USDCNY'

valueDict = dict()
featureValue = dict()

# 抓取FEATURE_NAME列表中的数据
def get_feature_data():
    for feature_name in FEATURE_NAME_LIST:
        MarketDataCrawler.get_market_data(8, 1000, feature_name)
        time.sleep(5)


# 抓取VALUE_NAME的数据
def get_value_data():
    MarketDataCrawler.get_market_data(8, 1000, VALUE_NAME)


# 生成目标值列表
def get_value_list():
    value_list = CommonUtil.read_csv(MarketDataCrawler.MARKET_DATA_PATH + '/' + VALUE_NAME + '.csv')
    for value_i in range(1, len(value_list)):
        date = CommonUtil.get_datetime_from_string_(value_list[value_i][0]).date()
        # 收盘价
        value = float(value_list[value_i][2])
        valueDict[date] = value


# 针对每个目标值，获得对应的特征向量
def get_feature_value():
    feature_vector_list = list()
    feature_name_list = list()
    for feature_name in FEATURE_NAME_LIST:
        feature_name_list.append(feature_name)
        feature_list = CommonUtil.read_csv(MarketDataCrawler.MARKET_DATA_PATH + '/' + feature_name + '.csv')
        feature_dict = dict()
        for feature_i in range(1, len(feature_list)):
            date = CommonUtil.get_datetime_from_string_(feature_list[feature_i][0]).date()
            # 开盘价
            feature_value = float(feature_list[feature_i][1])
            feature_dict[date] = feature_value
        for value_key in valueDict.keys():
            if value_key in feature_dict.keys():
                feature_value = feature_dict[value_key]
            else:
                feature_value = 'N/A'
            if value_key in featureValue.keys():
                feature_items = featureValue[value_key]
            else:
                feature_items = list()
            feature_items.append(feature_value)
            featureValue[value_key] = feature_items
    feature_name_list.append(VALUE_NAME)
    feature_name_list.insert(0, 'DATE')
    feature_vector_list.append(feature_name_list)
    for key in featureValue.keys():
        feature_items = featureValue[key]
        feature_items.append(valueDict[key])
        feature_items.insert(0, key)
        feature_vector_list.append(feature_items)
    CommonUtil.write_csv('../files/marketdata/FEATURE_VECTOR.csv', feature_vector_list)


# 调整特征向量
def adjust_feature_vector():
    feature_vector_list = CommonUtil.read_csv('../files/marketdata/FEATURE_VECTOR.csv')
    pre_item = feature_vector_list[0]
    current_item = pre_item
    for vector_i in range(1, len(feature_vector_list)):
        current_item = feature_vector_list[vector_i]
        for i in range(1, len(current_item)):
            if current_item[i] == 'N/A':
                current_item[i] = pre_item[i]
        feature_vector_list[vector_i] = current_item
        pre_item = current_item
    CommonUtil.write_csv('../files/marketdata/ADJUSTED_FEATURE_VECTOR.csv', feature_vector_list)


# 抓取FEATURE_NAME列表中的测试数据
def get_feature_data_test():
    for feature_name in FEATURE_NAME_LIST:
        MarketDataCrawler.get_market_data(8, 1, feature_name)
        time.sleep(5)


get_feature_data_test()

