from util import CrawlerUtil as CrawlerUtil, CrawlerLogger as CrawlerLogger
from newsnlp import BaiduNLPProcessor
# 特征文件路径
FEATURE_PATH = 'D:/CFETSIT/外汇项目组/技术工作/技术研究/舆情监测/原始数据获取/feature/feature.xlsx'
# 原始数据文件路径
RAW_NEWS_PATH = 'D:/CFETSIT/外汇项目组/技术工作/技术研究/舆情监测/原始数据获取/data/华尔街见闻_外汇_20160630_20180617.xlsx'
# RAW_NEWS_PATH = 'D:/CFETSIT/外汇项目组/技术工作/技术研究/舆情监测/原始数据获取/data/华尔街见闻_外汇_0_10000.xlsx'
# RAW_NEWS_PATH = 'D:/CFETSIT/外汇项目组/技术工作/技术研究/舆情监测/原始数据获取/data/华尔街见闻_外汇_demo.xlsx'
# 新闻分词后保存路径
SEGMENTED_NEWS_PATH = 'D:/CFETSIT/外汇项目组/技术工作/技术研究/舆情监测/lab/data/SEGMENTED_NEWS.csv'
SEGMENTED_NEWS_PATH_TEMP = 'D:/CFETSIT/外汇项目组/技术工作/技术研究/舆情监测/lab/data/SEGMENTED_NEWS_TEMP.csv'
# 特征向量保存路径
FEATURE_VECTOR_PATH = 'D:/CFETSIT/外汇项目组/技术工作/技术研究/舆情监测/lab/data/FEATURE_VECTOR.csv'
FEATURE_VECTOR_PATH_TEMP = 'D:/CFETSIT/外汇项目组/技术工作/技术研究/舆情监测/lab/data/FEATURE_VECTOR_TEMP.csv'
# 实际价格文件路径
ORIGIN_PRICE_PATH = 'D:/CFETSIT/外汇项目组/技术工作/技术研究/舆情监测/原始数据获取/data/USDCNY20160630_20171230.csv'
# 全局变量
# 特征字典[AAAA:黄金]
featureDict = dict()
# 新闻列表：[1, 2018/6/17  20:17:46, 伊朗：三个OPEC成员国将投票反对增产。]
newsList = list()
# 新闻分词后列表：[1, 2018/6/17  20:17:46, 伊朗, ：, 三个, OPEC, 成员国, 将, 投票, 反对, 增产, 。]
newsSegmentationList = list()
# 有关键词匹配的新闻列表：[1, 2018/6/17  20:17:46, OPEC]
newsMappedList = list()
# 情感特征列表：[1, 2018/6/17  20:17:46, [0, 0, 0.6, 0]]
featureVectorList = list()
# USD/CNY价格数据列表：[2016/6/30 15:00,	6.6433]
originalPriceList = list()


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
        value = feature_table.cell_value(rowNum, 1)
        featureDict[key] = value
    logger.info("Prepare Feature...Done!")


# 2.读取原始新闻数据
def prepare_raw_news():
    logger.info("In Prepare Raw News...")
    raw_news_data = CrawlerUtil.read_excel(RAW_NEWS_PATH)
    raw_news_table = raw_news_data.sheet_by_index(0)
    raw_news_rows = raw_news_table.nrows
    for rowN in range(0, raw_news_rows):
        news_item = list()
        news_index = int(raw_news_table.cell_value(rowN, 0))
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
    count = 1
    for news_item in newsList:
        word_list = BaiduNLPProcessor.lexer(news_item[2])
        word_list.insert(0, news_item[0])
        word_list.insert(1, CrawlerUtil.get_string_from_datetime(news_item[1]))
        newsSegmentationList.append(word_list)
        logger.info(count)
        count += 1
    CrawlerUtil.write_csv(SEGMENTED_NEWS_PATH, newsSegmentationList)
    logger.info("Segment News...Done!")


# 3*.读取分词后的新闻文件
def read_segmented_news():
    logger.info("In Read Segmented News...")
    global newsSegmentationList
    newsSegmentationList = CrawlerUtil.read_csv(SEGMENTED_NEWS_PATH)
    logger.info("Read Segmented News Done!")


# 4.对每条新闻进行特征关键词匹配
def news_keyword_map():
    logger.info("In News Keyword Map...")
    count = 0
    for word_list in newsSegmentationList:
        news_mapped = list()
        news_mapped.append(int(word_list[0]))
        news_mapped.append(word_list[1])
        for word_index in range(2, len(word_list)):
            word = word_list[word_index]
            if word in featureDict.values():
                if word not in news_mapped:
                    news_mapped.append(word)
        if len(news_mapped) > 2:
            count += 1
            newsMappedList.append(news_mapped)
    logger.info("News Keyword Map...Done!")
    logger.info("News With Keyword: " + str(count))


# 5.对匹配到特征的新闻进行情感分析
def news_sentiment():
    logger.info("In News Sentiment...")
    count = 1
    for mapped_news in newsMappedList:
        feature_vector_item = list()
        news_index = mapped_news[0]
        news_time = mapped_news[1]
        feature_vector_item.append(news_index)
        feature_vector_item.append(news_time)
        feature_vector = list()
        keyword_sentiment_dict = dict()
        # 下标从0开始，减1
        news_mapped = newsList[news_index - 1]
        for mapped_news_index in range(2, len(mapped_news)):
            keyword = mapped_news[mapped_news_index]
            sentiment_result = BaiduNLPProcessor.sentiment_classify(news_mapped[2])
            keyword_sentiment_dict[keyword] = sentiment_result
        keys = featureDict.keys()
        for key in keys:
            if featureDict[key] in keyword_sentiment_dict.keys():
                feature_vector.append(keyword_sentiment_dict[featureDict[key]])
            else:
                feature_vector.append(0)
        feature_vector_item.append(feature_vector)
        featureVectorList.append(feature_vector_item)
        logger.info(count)
        count += 1
    CrawlerUtil.write_csv(FEATURE_VECTOR_PATH, featureVectorList)
    logger.info("News Sentiment Done!")


# USD/CNY价格数据处理
def prepare_original_price():
    global originalPriceList
    originalPriceList = CrawlerUtil.read_csv(ORIGIN_PRICE_PATH)


logger = CrawlerLogger.Logger("../logs/raw_data_processor.log")
