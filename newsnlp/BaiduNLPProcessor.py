from aip import AipNlp

APP_ID = '11415218'
API_KEY = '2nG3xSaPag0e6sndbLFo2Zvv'
SECRET_KEY = 'xjXGEWN8VAvBhxaZ9EcAGl7E0ATLXnmj'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

text = "马其顿外长和希腊外长6月17日正式签署协议，马其顿国名将更改为“北马其顿共和国”，结束两国20多年的争端。新国名将在国内及国际上使用，并将写入马其顿宪法。这项协议仍需要马其顿议会和马其顿全民公投才能最终通过"

""" 调用词法分析 """
result = client.lexer(text)
wordList = result['items']
for item_i in range(len(wordList)):
    print(wordList[item_i]['item'])

