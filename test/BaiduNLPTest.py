from newsnlp import BaiduNLPProcessor

text = '美国政府发布加征关税的商品清单，将对从中国进口的500亿美元商品征收25%关税。'
result = BaiduNLPProcessor.sentiment_classify(text)
print(result)

# text = '⑪ 08:30 日本5月综合和服务业PMI'
# text = text.encode('gbk', 'ignore').decode('gbk')
# print(text)
# result = BaiduNLPProcessor.lexer(text)
# print(result)

# word1 = '白银'
# word2 = '黄金'
# print(BaiduNLPProcessor.word_sim(word1, word2))
