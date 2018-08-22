# 外汇市场新闻特征分析工具
import os
from util import CommonUtil, LogHelper, NewsUtil, ConfigHelper
from pyltp import SentenceSplitter
from pyltp import Segmentor

LTP_DATA_PATH = 'D:/Tool/Python_Tool/ltp_data_v3.4.0'  # ltp模型目录的路径
CFETSFX_LEXICON_PATH = 'D:/Tool/Python_Tool/ltp_data_v3.4.0/cfetsfx_lexicon.txt'
cws_model_path = os.path.join(LTP_DATA_PATH, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
# 原始数据文件路径
RAW_NEWS_PATH = '../files/newsprocess/RAW_NEWS.xlsx'
RAW_NEWS_DEMO_PATH = '../files/newsprocess/RAW_NEWS_DEMO.xlsx'
# 特征关键词后续分词文件路径
FEATURE_ABOUT_PATH = '../files/newsprocess/FEATURE_ABOUT.csv'

logger = LogHelper.Logger("../logs/news_feature_analyzer.log")
# 分析对于初选的特征关键词，对应的情感词汇有哪些
def feature_about():
    # 获取特征列表
    feature_dict = NewsUtil.get_feature()
    # 获取新闻中出现特征后最近的5个词及其属性
    logger.info("In Prepare Raw News...")
    raw_news_data = CommonUtil.read_excel(RAW_NEWS_DEMO_PATH)
    raw_news_table = raw_news_data.sheet_by_index(0)
    raw_news_rows = raw_news_table.nrows
    segmentor = Segmentor()  # 初始化实例
    segmentor.load_with_lexicon(cws_model_path, CFETSFX_LEXICON_PATH)  # 加载模型，第二个参数是您的外部词典文件路径
    feature_about_list = list()
    for rowN in range(0, raw_news_rows):
        news_content = raw_news_table.cell_value(rowN, 2)
        sentences = SentenceSplitter.split(news_content)
        for sentence in sentences:
            print(sentence)
            # 分词
            words = segmentor.segment(sentence)
            print(list(words))
            for word_index in range(0, len(words)):
                word = words[word_index]
                for feature_word in feature_dict.values():
                    if feature_word in word:
                        about_list = list()
                        count = 0
                        while word_index < len(words) and count < 6:
                            about_list.append(words[word_index])
                            count += 1
                            word_index += 1
                        feature_about_list.append(about_list)
                        print(about_list)
                        break
    segmentor.release()
    CommonUtil.write_csv(FEATURE_ABOUT_PATH, feature_about_list)


# 主入口
feature_about()
