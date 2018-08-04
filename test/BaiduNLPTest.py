from newsnlp import BaiduNLPProcessor
import re

# text = '人民币今天上涨了3个百分点'
# result = BaiduNLPProcessor.sentiment_classify(text)
# print(result)

# text = '⑪ 08:30 日本5月综合和服务业PMI'
# text = text.encode('gbk', 'ignore').decode('gbk')
# print(text)
# result = BaiduNLPProcessor.lexer(text)
# print(result)

word1 = '白银'
word2 = '黄金'
print(BaiduNLPProcessor.word_sim(word1, word2))

