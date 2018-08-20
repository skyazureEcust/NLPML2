from util import CommonUtil

# 特征文件路径
FEATURE_PATH = '../files/newsprocess/FEATURE.xlsx'



# 1.读取特征表
def get_feature():
    # 特征字典[AAAA:黄金]
    feature_dict = dict()
    # 获取sheet
    feature_data = CommonUtil.read_excel(FEATURE_PATH)
    feature_table = feature_data.sheet_by_index(0)
    # 获取总行数
    feature_rows = feature_table.nrows
    # 获取总列数
    # feature_cols = feature_table.ncols
    for rowNum in range(1, feature_rows):
        key = feature_table.cell_value(rowNum, 0)
        value = feature_table.cell_value(rowNum, 1)
        feature_dict[key] = value
    return feature_dict