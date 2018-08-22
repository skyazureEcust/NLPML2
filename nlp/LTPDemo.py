import os
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import CustomizedSegmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
from pyltp import SementicRoleLabeller


LTP_DATA_PATH = 'D:/Tool/Python_Tool/ltp_data_v3.4.0'  # ltp模型目录的路径
CFETSFX_LEXICON_PATH = 'D:/Tool/Python_Tool/ltp_data_v3.4.0/cfetsfx_lexicon.txt'
cws_model_path = os.path.join(LTP_DATA_PATH, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_PATH, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_PATH, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
par_model_path = os.path.join(LTP_DATA_PATH, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
srl_model_path = os.path.join(LTP_DATA_PATH, 'srl')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。


# 分句
sentence = SentenceSplitter.split('BBH货币策略全球主管Marc Chandler：英国脱欧没有可比先例，它所带来的一系列反应和结果还远未可知。今天英镑的表现比大多数货币要强劲。股票基金也许会在季末买入英镑来弥补之前过多的空头对冲仓位，这或许是重建英镑空头仓位、减少英镑头寸风险或全盘做空英镑的机会。区间看似遥远，但却是个很有趣的技术区间。')  # 分句
print('\n'.join(sentence))


# 分词
segmentor = Segmentor()  # 初始化实例
segmentor.load(cws_model_path)  # 加载模型
words = segmentor.segment('供给侧改革')  # 分词
print(list(words))
segmentor.release()  # 释放模型


# 使用分词外部词典
segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, CFETSFX_LEXICON_PATH)  # 加载模型，第二个参数是您的外部词典文件路径
words = segmentor.segment('7月1日CFETS人民币汇率指数为94.88，按周跌0.41')
print(list(words))
segmentor.release()


# 使用个性化分词模型
# customized_segmentor = CustomizedSegmentor()  # 初始化实例
# customized_segmentor.load(cws_model_path, CFETSFX_LEXICON_PATH)  # 加载模型，第二个参数是您的增量模型路径
# words = customized_segmentor.segment('亚硝酸盐是一种化学物质')
# print(list(words))
# customized_segmentor.release()


# 词性标注
postagger = Postagger()  # 初始化实例
postagger.load(pos_model_path)  # 加载模型
postags = postagger.postag(words)  # 词性标注
print(list(postags))
postagger.release()  # 释放模型


# 命名实体识别
recognizer = NamedEntityRecognizer() # 初始化实例
recognizer.load(ner_model_path)  # 加载模型
netags = recognizer.recognize(words, postags)  # 命名实体识别
print(list(netags))
recognizer.release()  # 释放模型


# 依存句法分析
parser = Parser()  # 初始化实例
parser.load(par_model_path)  # 加载模型
arcs = parser.parse(words, postags)  # 句法分析
print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
parser.release()  # 释放模型


# 语义角色标注
# labeller = SementicRoleLabeller() # 初始化实例
# labeller.load(srl_model_path)  # 加载模型
# # arcs 使用依存句法分析的结果
# roles = labeller.label(words, postags, arcs)  # 语义角色标注
# # 打印结果
# for role in roles:
#     print(role.index, "".join(
#         ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
# labeller.release()  # 释放模型