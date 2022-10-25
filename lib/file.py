import os
from shutil import copy, copytree
from pathlib import Path


def locate_files(basedir, keyword, match=False):
    """
    查找指定目录的文件
    :param match: 模糊查询
    :param basedir: 根目录
    :param keyword: 文件关键字
    :return: 目标文件的list 可迭代
    """
    p = Path(basedir)
    if match:
        keyword = f'*{keyword}*'
    files = p.rglob(keyword)
    return files


def copy_file(file, target_dir, new_filename=None):
    if os.path.exists(target_dir) is not True:
        os.makedirs(target_dir)

    if new_filename is None:
        filename = Path(file).name
    else:
        filename = new_filename + Path(file).suffix

    p = Path(target_dir)
    copy(file, p.joinpath(filename))


def copy_dir(file_dir, target_dir):
    if os.path.exists(target_dir) is not True:
        os.makedirs(target_dir)

    p = Path(target_dir)

    copytree(file_dir, os.path.join(target_dir, file_dir.name))
