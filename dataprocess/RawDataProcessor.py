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
# 原始价格文件路径
ORIGINAL_PRICE_PATH = '../files/ORIGINAL_PRICE.csv'
# ORIGINAL_PRICE_PATH = '../files/ORIGINAL_PRICE_DEMO.csv'
# 预处理后价格文件路径
PROCESSED_PRICE_PATH = '../files/PROCESSED_PRICE'
# 特征向量文件路径
FEATURE_VECTOR_PATH = '../files/FEATURE_VECTOR'
# 缩减后的特征向量文件路径
REDUCED_FEATURE_VECTOR_PATH = '../files/REDUCED_FEATURE_VECTOR'
# CSV文件尾缀
CSV_FILE_SUFFIX = '.csv'
# 新闻影响衰减极限值：预设为30分钟
NEWS_INFLUENCE_DACAY_THRESHOLD = 30
# 新闻影响极大值所在的时间点：预设为1分钟
NEWS_INFLUENCE_MOST = 1
# 特征向量缩放倍数
FEATURE_VECTOR_SCALE = 10000
# 价格取样长度，1：1分钟，5：5分钟，10：10分钟
PRICE_SAMPLE_MINUTE = 10
# 货币对精度
CURRENCY_PAIR_PRECISION = 4
# 开市时间
MARKET_OPEN_TIME = '09:30:00'
# 闭市时间
MARKET_CLOSE_TIME = '23:30:00'
# 价格时间区间
PRICE_START_TIME = '2016/07/01  09:30:00'
PRICE_END_TIME = '2017/12/29  23:27:00'

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
# 预处理后价格列表：[2018/6/30 15:00:00, 6.6433]
processedPriceList = list()


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


# 对原始价格数据进行预处理，采样（请注意设置采样频率）
def process_original_price():
    logger.info("In Process Original Price...")
    global originalPriceList
    originalPriceList = CrawlerUtil.read_csv(ORIGINAL_PRICE_PATH)
    sample_datetime = None
    sample_price_list = list()
    # 对每一个原始价格
    for original_price in originalPriceList:
        logger.debug('price time: ' + original_price[0])
        price_datetime = CrawlerUtil.get_datetime_from_string(original_price[0])
        price_value = float(original_price[1])
        if sample_datetime is None:
            sample_datetime = CrawlerUtil.get_datetime_from_string(PRICE_START_TIME)
        time_interval = CrawlerUtil.get_interval_seconds(price_datetime, sample_datetime)
        # 价格时间在采集区间外(价格对应时间远早于采集时刻点)，取下一个价格
        if time_interval < -PRICE_SAMPLE_MINUTE * 60 / 2:
            continue
        # 如果当前时间超过采样区间（晚于），先计算上一个采样时间的平均价格，再寻找下一个采样点
        while time_interval >= PRICE_SAMPLE_MINUTE * 60 / 2:
            # 如果当前采样点有价格
            if len(sample_price_list) > 0:
                price_sum = 0
                for price_item in sample_price_list:
                    price_sum += price_item
                average_price = round(price_sum / len(sample_price_list), CURRENCY_PAIR_PRECISION + 2)
                sample_datetime_str = CrawlerUtil.get_string_from_datetime(sample_datetime)
                average_price_item = [sample_datetime_str, average_price]
                # 将采样时间及对应的计算后的价格加入列表
                processedPriceList.append(average_price_item)
                # 重置采样点价格列表
                sample_price_list = list()
            # 计算下一个采样点
            sample_datetime = CrawlerUtil.get_next_sample_time(sample_datetime, PRICE_SAMPLE_MINUTE,
                                                               MARKET_OPEN_TIME, MARKET_CLOSE_TIME)
            time_interval = CrawlerUtil.get_interval_seconds(price_datetime, sample_datetime)
        logger.debug('sample datetime:' + CrawlerUtil.get_string_from_datetime(sample_datetime))
        # 价格时间在采集区间外
        if sample_datetime > CrawlerUtil.get_datetime_from_string(PRICE_END_TIME):
            break
        # 属于当前采样点，加入当前采样点价格列表，前闭后开[,)
        sample_price_list.append(price_value)
    # 处理最后一个采集时刻的价格列表
    # 如果当前采样点有价格
    if len(sample_price_list) > 0:
        price_sum = 0
        for price_item in sample_price_list:
            price_sum += price_item
        average_price = round(price_sum / len(sample_price_list), CURRENCY_PAIR_PRECISION + 2)
        sample_datetime_str = CrawlerUtil.get_string_from_datetime(sample_datetime)
        average_price_item = [sample_datetime_str, average_price]
        # 将采样时间及对应的计算后的价格加入列表
        processedPriceList.append(average_price_item)
    file_path = PROCESSED_PRICE_PATH + '_' + str(PRICE_SAMPLE_MINUTE) + CSV_FILE_SUFFIX
    CrawlerUtil.write_csv(file_path, processedPriceList)
    logger.info("Process Original Price Done!")


# 生成特征向量，并与目标值对应
def generate_feature_vector():
    logger.info("In Generate Feature Vector...")
    prepare_feature()
    # 设置标题
    title_list = list(featureDict.keys())
    title_list.append('TARGET')
    featureVectorList.append(title_list)
    feature_size = len(featureDict.keys())
    global newsFeatureList
    newsFeatureList = CrawlerUtil.read_csv(NEWS_FEATURE_PATH)
    global processedPriceList
    file_path = PROCESSED_PRICE_PATH + '_' + str(PRICE_SAMPLE_MINUTE) + CSV_FILE_SUFFIX
    processedPriceList = CrawlerUtil.read_csv(file_path)
    # 新闻从20160630开始到20171229，价格从20160701开始到20171229
    last_news_begin = 0
    news_feature_begin_index = last_news_begin
    pre_price_item = list()
    pre_price_item.append(PRICE_START_TIME)
    pre_price_item.append(0)
    # 将闭市时间内的新闻统一设置为开市前NEWS_INFLUENCE_MOST分钟时发生的
    for news_index in range(0, len(newsFeatureList)):
        news_feature = newsFeatureList[news_index]
        news_time = news_feature[0]
        # 重设新闻时间
        news_feature[0] = CrawlerUtil.\
            reset_news_time(news_time, NEWS_INFLUENCE_MOST, MARKET_OPEN_TIME, MARKET_CLOSE_TIME)
        newsFeatureList[news_index] = news_feature
    for current_price_item in processedPriceList:
        if PRICE_START_TIME <= current_price_item[0] < PRICE_END_TIME:
            # 计算价格的变化
            price_delta = round((float(current_price_item[1]) - float(pre_price_item[1])) * FEATURE_VECTOR_SCALE,
                                CURRENCY_PAIR_PRECISION)
            current_price_time = CrawlerUtil.get_datetime_from_string(current_price_item[0])
            pre_price_time = CrawlerUtil.get_datetime_from_string(pre_price_item[0])
            logger.debug(current_price_time)
            # 计算pre_price_time到current_price_time新闻的作用总和
            # last_interval_minutes >= 1
            last_interval_minutes = int(CrawlerUtil.get_interval_seconds(current_price_time, pre_price_time) / 60)
            influence_feature_vector = [0.0] * feature_size
            # 对两个价格之间的每个采样点计算新闻的影响
            is_influenced_price = False
            for minute_i in range(0, last_interval_minutes):
                # 计算的时刻点，pre_price_time之后的时刻点，包括current_price_time
                time_i = CrawlerUtil.get_minute_changed(pre_price_time, minute_i + 1)
                # 该时刻点受到影响对应的新闻
                for news_feature_begin_index in range(last_news_begin, len(newsFeatureList)):
                    interval_seconds = CrawlerUtil.get_interval_seconds(
                        time_i, CrawlerUtil.get_datetime_from_string(newsFeatureList[news_feature_begin_index][0]))
                    # 如果有新闻在影响范围内
                    if 0 <= interval_seconds <= NEWS_INFLUENCE_DACAY_THRESHOLD * 60:
                        for news_feature_end_index in range(news_feature_begin_index, len(newsFeatureList)):
                            if CrawlerUtil.get_datetime_from_string(newsFeatureList[news_feature_end_index][0]) \
                                    > time_i:
                                break
                        str_begin_end = str(minute_i + 1) + ': news->' + str(news_feature_begin_index) + ' : ' + str(
                            news_feature_end_index - 1)
                        logger.debug(str_begin_end)
                        for news_feature_index in range(news_feature_begin_index, news_feature_end_index):
                            current_news_feature = newsFeatureList[news_feature_index]
                            influence_score = decay_influence(CrawlerUtil.get_datetime_from_string(
                                current_news_feature[0]), time_i)
                            for value_i in range(0, feature_size):
                                influence_feature_vector[value_i] += float(current_news_feature[value_i + 1]) \
                                                                     * influence_score
                        is_influenced_price = True
                        break
                    elif interval_seconds < 0:
                        break
                last_news_begin = news_feature_begin_index
            if is_influenced_price:
                influence_feature_vector.append(price_delta)
                featureVectorList.append(influence_feature_vector)
        pre_price_item = current_price_item
    file_path = FEATURE_VECTOR_PATH + '_' + str(PRICE_SAMPLE_MINUTE) + CSV_FILE_SUFFIX
    CrawlerUtil.write_csv(file_path, featureVectorList)
    logger.info("Generate Feature Vector Done!")


# 定义影响衰减函数
def decay_influence(dt_news_time, dt_current_time):
    delta_seconds = CrawlerUtil.get_interval_seconds(dt_current_time, dt_news_time)
    if delta_seconds > NEWS_INFLUENCE_DACAY_THRESHOLD * 60:
        return 0
    # 0-60秒
    if delta_seconds <= NEWS_INFLUENCE_MOST * 60:
        influence_score = 1/(NEWS_INFLUENCE_MOST * 60) * delta_seconds
    else:
        influence_score = NEWS_INFLUENCE_DACAY_THRESHOLD/(NEWS_INFLUENCE_DACAY_THRESHOLD - NEWS_INFLUENCE_MOST) \
                          - 1/(NEWS_INFLUENCE_DACAY_THRESHOLD - NEWS_INFLUENCE_MOST) * delta_seconds / 60
    return round(influence_score * FEATURE_VECTOR_SCALE, CURRENCY_PAIR_PRECISION)


# 缩减特征向量
def reduce_feature_vector():
    logger.info("In Reduce Feature Vector...")
    prepare_feature()
    origin_feature_num = len(featureDict.keys())
    global featureVectorList
    reduced_feature_vector_list = list()
    feature_list = list()
    feature_count_threshold = 2
    file_path = FEATURE_VECTOR_PATH + '_' + str(PRICE_SAMPLE_MINUTE) + CSV_FILE_SUFFIX
    featureVectorList = CrawlerUtil.read_csv(file_path)
    feature_count_dict = dict()
    feature_count_list = [0] * origin_feature_num
    is_title = True
    for feature_vector in featureVectorList:
        if is_title:
            is_title = False
        else:
            for feature_value_index in range(0, origin_feature_num):
                if feature_vector[feature_value_index] != '0.0':
                    feature_count_list[feature_value_index] += 1
    feature_index = 0
    for key in featureDict.keys():
        feature_count = feature_count_list[feature_index]
        feature_count_dict[key] = feature_count
        if feature_count >= feature_count_threshold:
            feature_list.append(feature_index)
        feature_index += 1
    logger.info(str('Reduce Feature Vector to: ' + str(len(feature_list))))
    feature_list.append(origin_feature_num)
    # 拼装计数超过阈值的特征向量
    for feature_vector in featureVectorList:
        reduced_feature_vector = list()
        for feature_value_index in range(0, origin_feature_num + 1):
            if feature_value_index in feature_list:
                try:
                    reduced_feature_vector.append(feature_vector[feature_value_index])
                except IndexError:
                    logger.error(feature_vector)
                    logger.error(feature_value_index)
        reduced_feature_vector_list.append(reduced_feature_vector)
    file_path = REDUCED_FEATURE_VECTOR_PATH + '_' + str(PRICE_SAMPLE_MINUTE) + CSV_FILE_SUFFIX
    CrawlerUtil.write_csv(file_path, reduced_feature_vector_list)
    logger.info("Reduce Feature Vector Done!")
