from newsnlp import BaiduNLPProcessor

text = '2018-06-16 03:20:21,美国商品期货交易委员会（CFTC）美债持仓周报：至6月12日当周，' \
       '投机者转而美国国债期货净多头头寸4,187手合约，之前一周为净空头头寸18,169手合约。' \
       '（另附CBOT超长债、两年期、五年期和10年期美债持仓数据。）'
result = BaiduNLPProcessor.lexer(text)
print(result)
