#!/usr/bin/env python3
# 运行方式
# crontab -e
# 30 3 * * * /www/backup/mail_zip.py
import os
import subprocess
import sys
import time
import zipfile
from datetime import timedelta, date

try:
    import yagmail
except ImportError:
    result = subprocess.getoutput('pip3 install yagmail')
    print(result)
root_path = "/www/mpurselogs/doc"
# 切换到报表目录
os.chdir(root_path)
# 最终取时间
ltime_N = None
# 判断当前时间是 PM 还是 AM
if time.localtime().tm_hour > 12:
    # 下午取当天时间, 每天下午发送当天 17:00 前的报表B
    ltime_N = (date.today()).strftime("%d-%m-%Y")
else:
    # 上午取昨日时间, 每天上午6:00 发送昨日整日的报表A.
    ltime_N = (date.today() + timedelta(days=-1)).strftime("%d-%m-%Y")

if not os.path.exists(ltime_N):
    # 当天没有文件, 终止程序.
    print("no file today.")
    sys.exit()
zip_name = ltime_N + ".zip"
if os.path.exists(zip_name):
    # 文件已存在,重命名备份
    os.rename(zip_name, "{}.{}".format(zip_name, time.strftime('%H%M%S')))
# 压缩文件
zip_file = zipfile.ZipFile(zip_name, "w")
for f in os.listdir(ltime_N):
    zip_file.write('./{}/{}'.format(ltime_N, f), compress_type=zipfile.ZIP_DEFLATED)
# 邮箱正文
contents = ['{} daily report.  \n Mpurse Report '.format(ltime_N), ]
# 附件
attachment = [zip_file.filename]
# 邮件抬头
subject = '{} Mpurse Report'.format(ltime_N)
# 接收地址
to = ['zouguixing@statefortune.com.cn', ]
# to = ['amarinder@mpurseservices.com', 'abinash.jha@mpurseservices.com', 'manoj.nigam@mpurseservices.com',
#       'zouguixing@statefortune.com.cn', 'praful.purohit@mpurseservices.com', 'oujiquan@statefortune.com.cn']

# 链接邮箱服务器
mail_test = yagmail.SMTP(user="service@mpursewallet.com", password="qwerty@123", host='smtp.office365.com',
                         smtp_ssl=False)
# 发送邮件
mail_test.send(to=to, subject=subject, contents=contents, attachments=attachment)
