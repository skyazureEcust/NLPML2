# 处理原始新闻文件
import os
from util import CommonUtil, LogHelper
from pyltp import SentenceSplitter

logger = LogHelper.Logger("../logs/news_processor.log")
# 特征文件路径
FEATURE_PATH = '../files/newsprocess/FEATURE.xlsx'
# 原始数据文件路径
# RAW_NEWS_PATH = '../files/newsprocess/RAW_NEWS.xlsx'
RAW_NEWS_PATH = '../files/newsprocess/RAW_NEWS_DEMO.xlsx'
# 新闻分词后保存路径
SEGMENTED_NEWS_PATH = '../files/newsprocess/SEGMENTED_NEWS.csv'
LTP_DATA_PATH = 'D:/Tool/Python_Tool/ltp_data_v3.4.0'  # ltp模型目录的路径
CFETSFX_LEXICON_PATH = 'D:/Tool/Python_Tool/ltp_data_v3.4.0/cfetsfx_lexicon.txt'
cws_model_path = os.path.join(LTP_DATA_PATH, 'cws.model')  # 分词模型路径，模型名称为`cws.model`


# 全局变量
# 特征字典[AAAA:黄金]
featureDict = dict()
# 新闻列表：[1, 2018/6/17  20:17:46, 伊朗：三个OPEC成员国将投票反对增产。]
newsList = list()


# 1.读取特征表
def prepare_feature():
    logger.info("In Prepare Feature...")
    # 获取sheet
    feature_data = CommonUtil.read_excel(FEATURE_PATH)
    feature_table = feature_data.sheet_by_index(0)
    # 获取总行数
    feature_rows = feature_table.nrows
    # 获取总列数
    # feature_cols = feature_table.ncols
    for rowNum in range(1, feature_rows):
        key = feature_table.cell_value(rowNum, 0)
        value = feature_table.cell_value(rowNum, 1)
        featureDict[key] = value
    logger.info("Prepare Feature...Done!")


# 2.读取原始新闻文件，进行分句
def prepare_raw_news():
    logger.info("In Prepare Raw News...")
    raw_news_data = CommonUtil.read_excel(RAW_NEWS_PATH)
    raw_news_table = raw_news_data.sheet_by_index(0)
    raw_news_rows = raw_news_table.nrows
    for rowN in range(0, raw_news_rows):
        news_item = list()
        news_index = int(raw_news_table.cell_value(rowN, 0))
        news_time = CommonUtil.get_datetime_from_cell(raw_news_table.cell_value(rowN, 1))
        news_content = raw_news_table.cell_value(rowN, 2)
        sentences = SentenceSplitter.split(news_content)
        news_sentence_list = list(sentences)
        news_item.append(news_index)
        news_item.append(news_time)
        news_item.append(news_sentence_list)
        newsList.append(news_item)
    print(newsList)
    logger.info("Prepare Raw News...Done!")

# 针对每句进行词法分析（分词、词性分析），构造特征情感三元组（特征, 情感, 程度），计算针对各特征的情感值


prepare_raw_news()
