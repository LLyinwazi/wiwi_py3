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
# 报表A 每天上午6:00 发送  报表时间,都是发送前一天的
ltime_A = (date.today() + timedelta(days=-1)).strftime("%d-%m-%Y")
# 报表B 每天下午17:00 发送, 发送当天的
ltime_B = (date.today()).strftime("%d-%m-%Y")
print("time:" + ltime_A)
if not os.path.exists(ltime_A):
    # 当天没有文件, 终止程序.
    print("no file today.")
    sys.exit()
zip_name = ltime_A + ".zip"
if os.path.exists(zip_name):
    # 文件已存在,重命名备份
    os.rename(zip_name, "{}.{}".format(zip_name, time.strftime('%H%M%S')))
# 压缩文件
zip_file = zipfile.ZipFile(zip_name, "w")
for f in os.listdir(ltime_A):
    zip_file.write('./{}/{}'.format(ltime_A, f), compress_type=zipfile.ZIP_DEFLATED)
# 邮箱正文
contents = ['{} daily report.  \n Mpurse Report '.format(ltime_A), ]
# 附件
attachment = [zip_file.filename]
# 邮件抬头
subject = '{} Mpurse Report'.format(ltime_A)
# 接收地址
# to = ['zouguixing@statefortune.com.cn', ]
to = ['amarinder@mpurseservices.com', 'abinash.jha@mpurseservices.com', 'manoj.nigam@mpurseservices.com',
      'zouguixing@statefortune.com.cn', 'praful.purohit@mpurseservices.com', 'oujiquan@statefortune.com.cn']

# 链接邮箱服务器
mail_test = yagmail.SMTP(user="service@mpursewallet.com", password="qwerty@123", host='smtp.office365.com',
                         smtp_ssl=False)
# 发送邮件
mail_test.send(to=to, subject=subject, contents=contents, attachments=attachment)
