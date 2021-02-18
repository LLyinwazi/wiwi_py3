# coding=utf-8
import os
import re
import shutil

root_path = "/www/dep/"
pure_code = root_path + "pure_code/"
pure_war = root_path + "pure_war/"

intf = ["mpurse-base", "mpurse-parent", "mpurse-core", "mpurse-commons", "mpurse-job",
        "mpurse-cc-interface", "mpurse-payutils", "mpurse-kms-interface",
        "mpurse-op-interface", "mpurse-message-interface", "mpurse-account-interface",
        "mpurse-member-interface", "mpurse-trisk-interface", "mpurse-trade-icici",
        "mpurse-trade-interface",
        "mpurse-qcenter-interface", "mpurse-workflow-interface"]

serv = ["mpurse-cc-service",
        "mpurse-kms-service",
        "mpurse-op-service",
        "mpurse-message-service",
        "mpurse-account-service",
        "mpurse-member-service",
        "mpurse-trisk-service",
        "mpurse-trade-service",
        "mpurse-qcenter-service",
        "mpurse-workflow-service",
        "mpurse-api", "mpurse-oms", "mpurse-website"]

sp_boot = ["trade-mq", "mpurse-job2", ]

git_path = ["java_skeleton", "java_pubcore", "java_bizcore", "java_web"]


# 下载代码
def git_download():
    os.chdir(root_path)
    if not os.path.exists(pure_code):
        os.mkdir(pure_code)
    if not os.path.exists(pure_war):
        os.mkdir(pure_war)
    #     删除旧仓库
    # os.system('rm -fr ' + pure_code + '*')
    # os.system('rm -fr ' + pure_war + ' * ')
    #         下载代码
    os.system("git config --global user.name 'jenkins'")
    os.system("git config --global user.password 'jenkins@2020'")
    # os.system('git clone -b release http://150.109.123.249:9000/MpurseJava/java_web.git')  # 下载代码
    # os.system('git clone -b release http://150.109.123.249:9000/MpurseJava/java_bizcore.git')
    # os.system('git clone -b release http://150.109.123.249:9000/MpurseJava/java_pubcore.git')
    # os.system('git clone -b release http://150.109.123.249:9000/MpurseJava/java_skeleton.git')
    # os.system('git clone -b release http://150.109.123.249:9000/MpurseJava/java_devTest.git')
    for p in git_path:
        for ff in os.listdir(root_path + p):
            if not ff.startswith(".git"):
                shutil.copytree(root_path + p + "/" + ff, pure_code + ff)
    pass


def git_check_his(commit_id):
    os.system('git checkout ' + commit_id)  # 下检出指定版本
    # os.system('git clone -b tag http://150.109.123.249:9000/MpurseJava/java_bizcore.git')
    # os.system('git clone -b tag http://150.109.123.249:9000/MpurseJava/java_pubcore.git')
    # os.system('git clone -b tag http://150.109.123.249:9000/MpurseJava/java_skeleton.git')


# maven 目录
# mvn = r'mvn '
mvn = r'C:\devTool\maven-3.5.4-wiwi_0\bin\mvn '


# 编译代码
def build():
    os.chdir(pure_code)
    cmd = mvn + "clean install -Dmaven.test.skip=true"
    for f in intf:
        os.chdir(pure_code + f)
        r = os.popen(cmd)
        print(r.read())


# build war
def build1():
    os.chdir(pure_code)
    cmd = mvn + "clean package -Dmaven.test.skip=true"
    pattern = re.compile(r".*.[w,j]ar$")
    for f in serv + sp_boot:
        os.chdir(pure_code + f)
        r = os.popen(cmd)
        print(r.read())
        tar_dir = pure_code + f + "/target/"
        for ff in os.listdir(tar_dir):
            print(pattern.match(ff))
            if pattern.match(ff) is not None:
                war_ff = pure_war + ff
                if os.path.exists(war_ff):  # 删除旧文件
                    os.remove(war_ff)
                    print("deleted old file:%s" % war_ff)
                shutil.copy(tar_dir + ff, war_ff)  # 复制war 包到目标目录


def conf_reset():
    os.system("git config --global user.name 'zouguixing'")


if __name__ == '__main__':
    git_download()
    # build()
    # build1()
    conf_reset()
