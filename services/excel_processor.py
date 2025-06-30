import pandas as pd
from database.operations import *


def process_excel(data):
    # 读取Excel文件
    # df = pd.read_csv(file_path)
    print(data)
    # # 数据清洗/转换
    # df = clean_data(df)

    # 保存到数据库
    # print(df.to_dict())
    save_excel_data(data)
    print('存储成功')
    return 1
    # return aggregate_term_data()
    # # 执行聚合
    # return aggregate_term_data(df)

def process_gender(data):
    # 读取Excel文件
    # df = pd.read_csv(file_path)
    print(data)
    # # 数据清洗/转换
    # df = clean_data(df)

    # 保存到数据库
    # print(df.to_dict())
    save_gender_data(data)
    print('存储成功')

    # # 执行聚合
    # return aggregate_data()
    return 1

def clean_data(df):
    # 实现数据清洗逻辑
    # 示例：填充空值
    df.fillna({
        'Column1': 'Unknown',
        'Column2': 0
    }, inplace=True)
    return df

def handle_agg(data):

    #测试一个函数
    result = aggregate_extra_data()
    print(result)
    return result