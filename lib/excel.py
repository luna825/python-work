import xlwt
import xlrd


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


class ExcelReader(object):

    def __init__(self, path):
        self.table = xlrd.open_workbook(path).sheets()[0]

    # 行数
    def get_row_number(self):
        return self.table.nrows

    def get_header(self, header_row):
        return self.table.row_values(rowx=header_row, start_colx=0, end_colx=None)

    def read(self, header: tuple, header_row=0):
        result = []
        o_header = self.get_header(header_row)
        lines = self.get_row_number()
        for line in range(header_row + 1, lines):
            data = {}
            for field in header:
                col = o_header.index(field)
                if col > -1:
                    cell = self.table.cell_value(line, col)
                    data[field] = cell
            if len(data.keys()) > 0:
                result.append(data)

        return result


def write_to_excel(data, header, file_name):
    excel = EasyExcel()
    excel.add_sheet("sheet1").set_header(header).write(data).save(file_name)