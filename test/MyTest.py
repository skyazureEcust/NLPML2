from dataprocess import RawDataProcessor
from util import CrawlerUtil

feature_data = CrawlerUtil.read_excel(RawDataProcessor.FEATURE_PATH)
feature_table = feature_data.sheet_by_index(0)
# 获取总行数
feature_rows = feature_table.nrows

print(feature_rows)

