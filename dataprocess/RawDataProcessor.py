from util import CrawlerUtil as CrawlerUtil, CrawlerLogger as CrawlerLogger
from newsnlp import BaiduNLPProcessor
logger = CrawlerLogger.Logger("../logs/raw_data_processor.log")
# 特征文件路径
FEATURE_PATH = '../files/FEATURE.xlsx'
# 原始数据文件路径
RAW_NEWS_PATH = '../files/RAW_NEWS.xlsx'
# 新闻分词后保存路径
SEGMENTED_NEWS_PATH = '../files/SEGMENTED_NEWS.csv'
# 新闻情感分析后保存路径
NEWS_ITEM_PATH = '../files/NEWS_ITEM.csv'
# 新闻特征保存路径
NEWS_FEATURE_PATH = '../files/NEWS_FEATURE.csv'
# 实际价格文件路径
ORIGIN_PRICE_PATH = '../files/ORIGIN_PRICE.csv'
# 特征向量文件路径
FEATURE_VECTOR_PATH = '../files/FEATURE_VECTOR.csv'
# 新闻影响衰减极限值：预设为1200s
NEWS_INFLUENCE_DACAY_THRESHOLD = 1200
# 新闻影响极大值所在的时间点：预设为60s
NEWS_INFLUENCE_MOST = 60
# 特征向量缩放倍数
FEATURE_VECTOR_SCALE = 10000

# 全局变量
# 特征字典[AAAA:黄金]
featureDict = dict()
# 新闻列表：[1, 2018/6/17  20:17:46, 伊朗：三个OPEC成员国将投票反对增产。]
newsList = list()
# 新闻分词后列表：[1, 2018/6/17  20:17:46, 伊朗, ：, 三个, OPEC, 成员国, 将, 投票, 反对, 增产, 。]
newsSegmentationList = list()
# 有关键词匹配的新闻列表：[1, 2018/6/17  20:17:46, OPEC]
newsMappedList = list()
# 新闻情感分析后列表：[1, 2018/6/17  20:17:46, [0, 0, 0.6, 0]]
newsItemList = list()
# 新闻特征向量列表：[2018/6/30 15:00:00, 0, 0, 0.6, 0]
newsFeatureList = list()
# USD/CNY价格数据列表：[2018/6/30 15:00:00, 6.6433]
originalPriceList = list()
# 特征向量和目标值列表：[0, 0.2, 0.6, 0, ->0.001]
featureVectorList = list()


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
            for feature_word in featureDict.values():
                if feature_word in word and feature_word not in news_mapped:
                    news_mapped.append(feature_word)
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
        newsItemList.append(feature_vector_item)
        feature_vector.insert(0, news_time)
        newsFeatureList.append(feature_vector)
        logger.info(count)
        count += 1
    CrawlerUtil.write_csv(NEWS_ITEM_PATH, newsItemList)
    CrawlerUtil.write_csv(NEWS_FEATURE_PATH, newsFeatureList)
    logger.info("News Sentiment Done!")


# 统计特征向量的计算
def feature_col_count():
    logger.info("In Count Feature Appear...")
    prepare_feature()
    feature_count_dict = dict()
    global newsFeatureList
    newsFeatureList = CrawlerUtil.read_csv(NEWS_FEATURE_PATH)
    feature_count_list = [0] * len(featureDict.keys())
    for feature_vector in newsFeatureList:
        feature_index = 0
        for feature_value_index in range(1, len(feature_vector)):
            if feature_vector[feature_value_index] != '0':
                feature_count_list[feature_index] += 1
            feature_index += 1
    feature_index = 0
    for key in featureDict.keys():
        feature_count = feature_count_list[feature_index]
        feature_index += 1
        feature_count_dict[key] = feature_count
        row_item = key + "," + feature_count
        logger.info(row_item)
    logger.info("Count Feature Appear Done!")


# 生成特征向量，并与目标值对应
def generate_feature_vector():
    logger.info("In Generate Feature Vector...")
    prepare_feature()
    feature_size = len(featureDict.keys())
    global newsFeatureList
    newsFeatureList = CrawlerUtil.read_csv(NEWS_FEATURE_PATH)
    global originalPriceList
    originalPriceList = CrawlerUtil.read_csv(ORIGIN_PRICE_PATH)
    # 新闻从20160630开始，价格从20160701开始到20170630
    last_news_begin = 0
    price_start_time = '2016/07/01  09:30:00'
    price_end_time = '2017/06/30  23:59:59'
    for current_price_item in originalPriceList:
        is_finished = False
        if price_start_time < current_price_item[0] < price_end_time:
            price_delta = (float(current_price_item[1]) - float(pre_price_item[1]))
            # 计算价格的变化率
            last_interval_seconds = CrawlerUtil.get_interval_seconds(CrawlerUtil.get_datetime_from_string(
                current_price_item[0]), CrawlerUtil.get_datetime_from_string(pre_price_item[0]))
            price_delta_rate = round(price_delta * FEATURE_VECTOR_SCALE / last_interval_seconds, 6)
            current_time = CrawlerUtil.get_datetime_from_string(current_price_item[0])
            logger.debug(current_time)
            for news_feature_begin_index in range(last_news_begin, len(newsFeatureList) - 1):
                if is_finished:
                    break
                interval_seconds = CrawlerUtil.get_interval_seconds(
                    current_time, CrawlerUtil.get_datetime_from_string(newsFeatureList[news_feature_begin_index][0]))
                if 0 <= interval_seconds <= 1200:
                    influence_feature_vector = [0] * feature_size
                    for news_feature_end_index in range(news_feature_begin_index, len(newsFeatureList) - 1):
                        if is_finished:
                            break
                        if CrawlerUtil.get_datetime_from_string(newsFeatureList[news_feature_end_index][0]) \
                                > current_time:
                            for news_feature_index in range(news_feature_begin_index, news_feature_end_index - 1):
                                current_news_feature = newsFeatureList[news_feature_index]
                                influence_score = decay_influence(CrawlerUtil.get_datetime_from_string(
                                    current_news_feature[0]), current_time)
                                for value_i in range(0, feature_size):
                                    influence_feature_vector[value_i] += float(current_news_feature[value_i + 1]) \
                                                                         * influence_score
                            is_finished = True
                            influence_feature_vector.append(price_delta_rate)
                            featureVectorList.append(influence_feature_vector)
                            break
                elif interval_seconds < 0:
                    is_finished = True
                last_news_begin = news_feature_begin_index
        pre_price_item = current_price_item
    CrawlerUtil.write_csv(FEATURE_VECTOR_PATH, featureVectorList)
    logger.info("Generate Feature Vector Done!")


# 定义影响衰减函数
def decay_influence(dt_news_time, dt_current_time):
    delta_second = CrawlerUtil.get_interval_seconds(dt_current_time, dt_news_time)
    if delta_second > NEWS_INFLUENCE_DACAY_THRESHOLD:
        return 0
    if delta_second < NEWS_INFLUENCE_MOST:
        influence_score = 1/60 * delta_second
    else:
        influence_score = 1200/1140 - 1/1140 * delta_second
    return round(influence_score * FEATURE_VECTOR_SCALE, 4)
