from dataprocess import RawDataProcessor

# 第一步，生成新闻分词后关键词列表文件
# RawDataProcessor.prepare_feature()
# RawDataProcessor.prepare_raw_news()
# RawDataProcessor.news_segment()

# # 第二步，生成特征向量文件
RawDataProcessor.prepare_feature()
RawDataProcessor.prepare_raw_news()
RawDataProcessor.read_segmented_news()
RawDataProcessor.news_keyword_map()
RawDataProcessor.news_sentiment()
