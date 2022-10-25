# 文件相关操作api
import re

from lib.file import locate_files, copy_file
from lib.dbfwr import DBFReader
import os


class FileOperate(object):

    def __init__(self, filename, new_filename=None, to='.'):
        self.filename = filename
        self.new_filename = new_filename
        self.to = to
        self.files = []
        self.message = None

    # 查找
    def find(self, file_dir, match=False):
        files = list(locate_files(file_dir, self.filename, match))
        if len(files) == 0:
            self.message = '未找到:' + self.filename
        self.files = files
        return files

    # 排出
    def exclude(self, keyword):
        assert len(self.files) > 0, '文件不存在'
        self.files = [file for file in self.files if re.match(keyword, str(file)) is None]

    def copy_one(self, root_dir):
        assert len(self.files) == 1, '存在多个文件'
        copy_file(self.files[0], os.path.join(root_dir, self.to), self.new_filename)
        print(self.files[0])

    def copy(self, root_dir):

        for i, file in enumerate(self.files):
            new_filename = None
            if self.new_filename is not None:
                new_filename = self.new_filename + '_' + str(i)
            copy_file(file, os.path.join(root_dir, self.to), new_filename)

    @property
    def has_message(self):
        return self.message is not None


def create_file_operate(dbf_file, fields):
    dbf_reader = DBFReader(dbf_file)
    files_dict = dbf_reader.read_to_list_dict(fields)
    files_config = [FileOperate(d.get('origin'), d.get('filename', None), d.get('target', '.')) for d in files_dict]
    return files_config


def make_file(dbf_file, fields, basedir, target):
    operates = create_file_operate(dbf_file, fields)
    error = []
    for o in operates:
        o.find(basedir)
        if o.has_message:
            error.append(o.message)
        else:
            o.copy_one(target)
    return error



