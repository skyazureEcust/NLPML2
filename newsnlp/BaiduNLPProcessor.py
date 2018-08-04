from aip import AipNlp
import time
from util import CrawlerUtil as CrawlerUtil, CrawlerLogger as CrawlerLogger

APP_ID = '11415218'
API_KEY = '2nG3xSaPag0e6sndbLFo2Zvv'
SECRET_KEY = 'xjXGEWN8VAvBhxaZ9EcAGl7E0ATLXnmj'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


# 词法分析
def lexer(text):
    # text = "伊朗：三个OPEC成员国将投票反对增产
    word_list = list()
    # 去除gbk无法识别的字符（百度API使用gbk编码）
    text = text.encode('gbk', 'ignore').decode('gbk')
    while len(word_list) == 0:
        try:
            word_list = lexer_try(text)
        except Exception as e:
            logger.warning(e)
            logger.warning('Fuck Baidu API! We Will Retry...')
            time.sleep(2)
    return word_list


# 情感倾向分析
# sentiment 表示情感极性分类结果, 0:负向，1:中性，2:正向
# confidence 表示分类的置信度
# positive_prob	 表示属于积极类别的概率
# negative_prob	表示属于消极类别的概率
def sentiment_classify(text):
    # 去除gbk无法识别的字符（百度API使用gbk编码）
    text = text.encode('gbk', 'ignore').decode('gbk')
    # sentiment_score正常不会等于-9
    sentiment_score = -9
    while sentiment_score == -9:
        try:
            sentiment_score = sentiment_classify_try(text)
        except Exception as e:
            logger.warning(e)
            logger.warning('Fuck Baidu API! We Will Retry...')
            time.sleep(2)
    return sentiment_score


# 提取标签
def keyword(text):
    result = client.keyword(text, text)
    items = result['items']
    return items


# 评论观点
# prop	匹配上的属性词
# adj	匹配上的描述词
# sentiment	该情感搭配的极性（0表示消极，1表示中性，2表示积极）
# begin_pos	该情感搭配在句子中的开始位置
# end_pos	该情感搭配在句子中的结束位置
# abstract	对应于该情感搭配的短句摘要
def comment_tag(text):
    options = dict()
    options["type"] = 8
    result = client.commentTag(text, options)
    # items = result['items']
    logger.info(result)
    return result


def lexer_try(text):
    result = client.lexer(text)
    word_list = list()
    if result:
        if 'items' in result.keys():
            items = result['items']
            for item_i in range(len(items)):
                word_list.append(items[item_i]['item'])
        else:
            logger.warning(result)
    return word_list


def sentiment_classify_try(text):
    result = client.sentimentClassify(text)
    sentiment_score = -9
    if result:
        if 'items' in result.keys():
            items = result['items']
            # 0:负向，1:中性，2:正向
            sentiment_type = items[0]['sentiment']
            if sentiment_type == 2:
                sentiment_score = items[0]['positive_prob'] * items[0]['confidence']
            elif sentiment_type == 0:
                sentiment_score = -1 * items[0]['negative_prob'] * items[0]['confidence']
            elif sentiment_type == 1:
                sentiment_score = 0
    # 返回值保留4位小数
    return round(sentiment_score, 4)


# 词义相似度分析
#  score 相似度分数
def word_sim(s_word1, s_word2):
    # 调用词义相似度
    return client.wordSimEmbedding(s_word1, s_word2)
    # #如果有可选参数
    # options = {}
    # options["mode"] = 0
    # # 带参数调用词义相似度
    # client.wordSimEmbedding(word1, word2, options)

logger = CrawlerLogger.Logger("../logs/baidu_npl_processor.log")
