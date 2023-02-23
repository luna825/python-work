# 考点工作相关API
from lib.dbfwr import DBFReader
from lib.excel import write_to_excel, ExcelReader
from model.place import PlacePaperModel
from itertools import groupby


# 生成带序号的考试试卷信息
def make_place_paper(file_path, result_path):
    dbfReader = DBFReader(file_path)
    data = dbfReader.read_to_list_dict(PlacePaperModel.fields())
    papers = [PlacePaperModel(**d) for d in data]
    result = [dict(r) for r in _set_paper_number(papers)]
    write_to_excel(result, PlacePaperModel.fields(), result_path)


def _set_paper_number(data):
    res = []
    tmp = sorted(data, key=lambda x: x.sort_id)
    for key, group in groupby(tmp, lambda x: x.group_id):
        g = list(group)
        prefix = str(len(g)) + '-'
        for i, item in enumerate(g):
            item.set_number(prefix + str(i+1))
        res.extend(g)
    return res


# 2023年考点健康打卡数据和实际考生数据进行合并
def make_health_info(file1, file2):
    """
    :param file1:  实际考生数据
    :param file2:  健康打卡数据
    :return:
    """
    ks_header = ("报名号", "姓名", "证件号", "报考单位", "报考单位名称", "考生来源", "毕业单位名称", "联系电话", "本校考生")
    ks_excel = ExcelReader(file1)
    ks_data = ks_excel.read(ks_header)

    health_header = (
        "报名号", "上报时间", "你当前个人涉疫情况", "你当前个人防疫状态", "你现在所处省份", "你的当前位置", "重庆市外的考生",
        "行程安排", "简要说明"
    )
    health_excel = ExcelReader(file2)
    health_data = health_excel.read(health_header)

    ks_dict = {item['报名号']: item for item in ks_data}
    health_dict = {item['报名号']: item for item in health_data}

    merged_dict = {}
    for bmh, item in ks_dict.items():
        if bmh in health_dict:
            merged_dict[bmh] = {**item, **health_dict[bmh]}
        else:
            merged_dict[bmh] = item

    merged_list = [item for bmh, item in merged_dict.items()]

    write_to_excel(merged_list, ks_header + health_header[1:], './result/test')


# 对本校应届学生按院系分组
def group_self_stu(file):
    header = ("报名号", "姓名", "证件号", "报考单位名称", "本校考生", "打卡时间", "前个人涉疫情况", "你现在所处省份", "联系电话")
    reader = ExcelReader(file)
    data = reader.read(header)
    sorted(data, key=lambda x: x['本校考生'])
    result = _groupy_data('本校考生', data)
    for key, values in result.items():
        write_to_excel(values, header, './result/' + key + '-' + str(len(values)))


def _groupy_data(key: str, data: list):
    result = {}
    for d in data:
        if d[key] in result.keys():
            result[d[key]].append(d)
        else:
            result[d[key]] = [d]
    return result
