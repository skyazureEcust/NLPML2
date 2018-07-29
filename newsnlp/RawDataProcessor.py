from util import CrawlerUtil as CrawlerUtil, CrawlerLogger as CrawlerLogger
from newsnlp import BaiduNLPProcessor
# 特征文件路径
FEATURE_PATH = 'D:/CFETSIT/外汇项目组/技术工作/技术研究/舆情监测/原始数据获取/feature/feature.xlsx'
# 原始数据文件路径
# RAW_NEWS_PATH = 'D:/CFETSIT/外汇项目组/技术工作/技术研究/舆情监测/原始数据获取/data/华尔街见闻_外汇_20160630_20180617.xlsx'
RAW_NEWS_PATH = 'D:/CFETSIT/外汇项目组/技术工作/技术研究/舆情监测/原始数据获取/data/华尔街见闻_外汇_demo.xlsx'
# 新闻分词后保存路径
SEGMENTED_NEWS_PATH = 'D:/CFETSIT/外汇项目组/技术工作/技术研究/舆情监测/lab/data/SEGMENTED_NEWS.csv'
# 全局变量
# 特征唯一标识
featureKeyList = list()
# 特征信息列表（第一列为特征名称）
featureValueList = list()
# 新闻列表
newsList = list()
# 新闻分词后列表
newsSegmentationList = list()
# 带有关键词的新闻列表
newsWithKeywordList = list()
# 有关键词匹配的新闻列表
newsMappedList = list()


# 1.读取特征表
def prepare_feature():
    logger.info("In Prepare Feature...")
    # 获取sheet
    feature_data = CrawlerUtil.read_excel(FEATURE_PATH)
    feature_table = feature_data.sheet_by_index(0)
    # 获取总行数
    feature_rows = feature_table.nrows
    # 获取总列数
    # feature_cols = feature_table.ncols
    for rowNum in range(1, feature_rows):
        key = feature_table.cell_value(rowNum, 0)
        featureKeyList.append(key)
        # value_list = []
        # for colNum in range(1, feature_cols):
        #     value_list.append(feature_table.cell_value(rowNum, colNum))
        # featureValues.append(value_list)
        featureValueList.append(feature_table.cell_value(rowNum, 1))
    logger.info("Prepare Feature...Done!")


# 2.读取原始新闻数据
def prepare_raw_news():
    logger.info("In Prepare Raw News...")
    raw_news_data = CrawlerUtil.read_excel(RAW_NEWS_PATH)
    raw_news_table = raw_news_data.sheet_by_index(0)
    raw_news_rows = raw_news_table.nrows
    for rowN in range(0, raw_news_rows):
        news_item = list()
        news_index = raw_news_table.cell_value(rowN, 0)
        news_time = CrawlerUtil.get_datetime_from_cell(raw_news_table.cell_value(rowN, 1))
        news_content = raw_news_table.cell_value(rowN, 2)
        news_item.append(news_index)
        news_item.append(news_time)
        news_item.append(news_content)
        newsList.append(news_item)
    logger.info("Prepare Raw News...Done!")


# 3.对每条新闻进行分词
def news_segment():
    logger.info("In Segment News...")
    for news_item in newsList:
        word_list = BaiduNLPProcessor.lexer(news_item[2])
        word_list.insert(0, CrawlerUtil.get_string_from_datetime(news_item[0]))
        word_list.insert(1, CrawlerUtil.get_string_from_datetime(news_item[1]))
        newsSegmentationList.append(word_list)
    CrawlerUtil.write_csv(SEGMENTED_NEWS_PATH, newsSegmentationList)
    logger.info("Segment News...Done!")


# 4.对每条新闻进行特征关键词匹配
def news_keyword_map():
    logger.info("In News Keyword Map...")
    count = 0
    for word_list in newsSegmentationList:
        for word in word_list[2]:
            news_mapped = list()
            news_mapped.append(word_list[0])
            news_mapped.append(word_list[1])
            if word in featureValueList:
                news_mapped.append(word)
                count += 1
            if len(news_mapped) > 2:
                newsMappedList.append(news_mapped)
    logger.info("News Keyword Map...Done!")
    logger.info("News With Keyword: " + count)

# 5.对匹配到特征的新闻进行情感分析
# def news_sentiment():




logger = CrawlerLogger.Logger("logs/raw_data_processor.log")