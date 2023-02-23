# 这是一个示例 Python 脚本。

from api.files import make_file
from api.place import make_place_paper, make_health_info, group_self_stu

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # 考点试卷编辑流水号
    # make_place_paper('./data/paper.dbf', './result/5010paper')
    make_health_info('./data/考生打卡信息.xls', './data/考生防疫健康上报信息.xls')
    # group_self_stu('./data/20221217打卡信息 -本校学生.xls')