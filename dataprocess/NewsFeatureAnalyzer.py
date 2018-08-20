# 外汇市场新闻特征分析工具
from util import CommonUtil, LogHelper, NewsUtil

# 分析对于初选的特征关键词，对应的情感词汇有哪些
def feature_about():
    # 获取特征列表
    feature_dict = NewsUtil.get_feature()
    # 获取特征对应的情感词汇
