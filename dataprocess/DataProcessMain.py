from dataprocess import RawDataProcessor

# 第一步，生成新闻分词后关键词列表文件
# RawDataProcessor.prepare_feature()
# RawDataProcessor.prepare_raw_news()
# RawDataProcessor.news_segment()

# 第二步，生成新闻特征文件
# RawDataProcessor.prepare_feature()
# RawDataProcessor.prepare_raw_news()
# RawDataProcessor.read_segmented_news()
# RawDataProcessor.news_keyword_map()
# RawDataProcessor.news_sentiment()

# 第三步，生成特征向量和目标值
RawDataProcessor.generate_feature_vector()
