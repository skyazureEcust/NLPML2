from snownlp import SnowNLP
from snownlp import sentiment
# SnowNLP库：
# words：分词
# tags：关键词
# sentiments：情感度
# pinyin：拼音
# keywords(limit)：关键词
# summary：关键句子
# sentences：语序
# tf：tf值
# idf：idf值
# sentiment.train('D:/Tool/Python/Lib/site-packages/snownlp-0.12.3-py3.6.egg/snownlp/sentiment/neg.txt', 'D:/Tool/Python/Lib/site-packages/snownlp-0.12.3-py3.6.egg/snownlp/sentiment/pos.txt')
# sentiment.save('D:/Tool/Python/Lib/site-packages/snownlp-0.12.3-py3.6.egg/snownlp/sentiment/sentiment.marshal')
s = SnowNLP(u'在岸人民币兑美元盘初再次刷新五年半低位，一度至6.6690元，较上日夜盘收盘跌近40点。')
# s.words         # [u'这个', u'东西', u'真心', u'很', u'赞']
print(s.words)
s.tags  # [(u'这个', u'r'), (u'东西', u'n'), (u'真心', u'd')
# , (u'很', u'd'), (u'赞', u'Vg')]
print(s.sentiments)
