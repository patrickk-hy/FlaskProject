import pandas as pd
from database.operations import save_excel_data, aggregate_data


def process_excel(file_path):
    # 读取Excel文件
    print(file_path)
    df = pd.read_csv(file_path)
    print(df)
    # # 数据清洗/转换
    # df = clean_data(df)

    # 保存到数据库
    # print(df.to_dict())
    save_excel_data(df)
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