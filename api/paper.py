from lib.excel import ExcelReader, write_to_excel
from lib.dbfwr import DBFReader
from pathlib import Path


def analysis_self_paper(score_path, subject_config, result_path):
    """
    自命题成绩分析
    :param score_path: 自命题成绩库
    :param subject_config: 一个科目的成绩配置
    :param result_path: 分析结果
    """

    header = ('num', 'total', 'pro1', 'pro2')
    file_name = Path(subject_config).name

    # 读取成绩配置文件
    excelReader = ExcelReader(subject_config)
    subject_info = excelReader.read(header)

    # 读取成绩
    dbfReader = DBFReader(score_path)
    result = []
    # 分析处理
    for info in subject_info:
        data = {}
        num = info.get('num')
        total = info.get('total')
        pro1 = total * info.get('pro1')
        pro2 = total * info.get('pro2')
        score_data = [d.get(num) for d in dbfReader.read_to_list_dict([num])]
        data['num'] = num
        data['total'] = total
        data['avg'] = round(sum(score_data) / len(score_data), 2)
        data['pro1'] = len(list(filter(lambda x: _filter_score(x, pro1), score_data))) / len(score_data)
        data['pro2'] = len(list(filter(lambda x: _filter_score(x, pro2), score_data))) / len(score_data)
        result.append(data)

    write_to_excel(result, ['num', 'total', 'avg', 'pro1', 'pro2'], result_path)


def _filter_score(x, bound):
    return x >= bound
