# coding=UTF-8
import os
import re
import shutil
import zipfile

# 打包压缩日志文件并移动到指定目录
from datetime import date, timedelta


def zip_logs2(prefix):
    root_path = "/www/mpurselogs"
    ## 获取昨天日期
    date_time = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
    for sub_dir in os.listdir(root_path):
        print("sub_dir->" + sub_dir)
        path_join = os.path.join(root_path, sub_dir)
        if os.path.isfile(path_join):
            continue
        # 切换到子文件夹 如 account
        os.chdir(path_join)
        # 罗列当前目录下所有文件
        sub_files = os.listdir()
        # 压缩文件的文件名
        zip_file_name = prefix + "_" + sub_dir + "_" + date_time + ".log.zip"
        if (os.path.exists(zip_file_name)):
            # 已存在的文件, 不需要压缩
            cp_to_backup(zip_file_name, root_path)
            continue
        # 文件已存在
        zip_file_exit = False
        for f in sub_files:
            # 正则匹配 包含数字并且以 .log 结尾的文件
            if (re.match('.*\d+.*\\.log$', f)):
                if (not zip_file_exit):
                    # 需要用时再创建
                    file_open = zipfile.ZipFile(zip_file_name, "w")
                    zip_file_exit = True
                # 匹配到文件, 添加到压缩包
                print("adding " + f + " ......")
                file_open.write(f, compress_type=zipfile.ZIP_DEFLATED)
        if (zip_file_exit):
            cp_to_backup(zip_file_name, root_path)


def cp_to_backup(file_name: str, root_path: str):
    '''
    复制到一个 root_path目录下
    :param file_name: 原压缩包文件
    :param root_path: 目标目录
    :return:
    '''
    dest = root_path + os.sep + file_name
    if os.path.exists(dest):
        # 目标文件已存在, 需要排查原因.
        print(">>>>warning<<<<  destination already exits.-->" + dest)
        for i in range(0, 100):
            dest = root_path + os.sep + file_name + "." + str(i) + ".zip"
            if not os.path.exists(dest):
                break
    shutil.copy(file_name, dest)


if __name__ == '__main__':
    zip_logs2("vm97")
    print("------------completed-------------------")
