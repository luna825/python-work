import dbfread
import dbf


class DBFReader(object):
    def __init__(self, file_path):
        self.table = dbfread.DBF(file_path, encoding='gbk', lowernames=True, char_decode_errors='ignore')

    def read(self, fields: list, callback, count: int = 0):
        assert len(fields) > 0, '读取的字段不能为空'

        i = 0
        for record in self.table:
            if 0 < count == i:
                break

            data = {}
            for field in fields:
                if isinstance(field, str):
                    data[field] = record[str.lower(field)]
                if isinstance(field, dict):
                    # data[field.get('name')] = record[str.lower(field.get('key'))]
                    name = field.get('name')

                    if field.get('value', None) is not None:
                        data[name] = field.get('value')
                    elif name in data:
                        data[name] = data[name] + record[str.lower(field.get('key'))]
                    else:
                        data[name] = record[str.lower(field.get('key'))]

            callback(data)
            i = i + 1

    def read_to_list_dict(self, fields: list, count: int = 0):
        res = []
        self.read(fields, res.append, count)
        return res

    def read_to_list_tuple(self, fields: list, count: int = 0):
        tmp = self.read_to_list_dict(fields, count)
        return [tuple(d.values()) for d in tmp]


class DBFWriter(object):
    def __init__(self, path, field_specs):
        self.table = dbf.Table(filename=path, field_specs=field_specs, codepage='cp936')

    def write(self, data):
        for record in data:
            self.table.append(record)
        return self

    def open(self):
        self.table.open(mode=dbf.READ_WRITE)
        return self

    def close(self):
        self.table.close()
