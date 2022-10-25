# 考点工作相关API
from lib.dbfwr import DBFReader
from lib.excel import write_to_excel
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
