from aip import AipNlp

APP_ID = '11415218'
API_KEY = '2nG3xSaPag0e6sndbLFo2Zvv'
SECRET_KEY = 'xjXGEWN8VAvBhxaZ9EcAGl7E0ATLXnmj'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


# 词法分析
def lexer(text):
    # text = "伊朗：三个OPEC成员国将投票反对增产"
    try:
        result = client.lexer(text)
    except Exception as e:
        print(text, e)
        result = client.lexer(text)
    if result:
        items = result['items']
        word_list = []
        for item_i in range(len(items)):
            word_list.append(items[item_i]['item'])
        return word_list
    else:
        print('Error Occurs in Processing ', text)
        return []


# 情感倾向分析
# sentiment 表示情感极性分类结果, 0:负向，1:中性，2:正向
# confidence 表示分类的置信度
# positive_prob	 表示属于积极类别的概率
# negative_prob	表示属于消极类别的概率
def sentiment_classify(text):
    result = client.sentimentClassify(text)
    items = result['items']
    return items


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
    print(result)
    return result
