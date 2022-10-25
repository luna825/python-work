import xlwt


class EasyExcel(object):

    def __init__(self):
        self.excel = xlwt.Workbook()
        self.sheet = None
        self.header = ()

    def add_sheet(self, name):
        self.sheet = self.excel.add_sheet(name)
        return self

    def set_header(self, header: tuple):

        assert self.sheet is not None, "无数据表"

        self.header = header
        for i, head in enumerate(header):
            self.sheet.write(0, i, head)

        return self

    def write(self, data: list):

        assert self.sheet is not None, "无数据表"

        if len(self.header) > 0:
            start = 1
            for r, row in enumerate(data):
                for key, value in row.items():
                    c = self.header.index(key)
                    self.sheet.write(r + start, c, value)
        else:
            for r, row in enumerate(data):
                for c, value in enumerate(row.values()):
                    self.sheet.write(r, c, value)
        return self

    def save(self, name):
        self.excel.save(name + '.xls')


def write_to_excel(data, header, file_name):
    excel = EasyExcel()
    excel.add_sheet("sheet1").set_header(header).write(data).save(file_name)