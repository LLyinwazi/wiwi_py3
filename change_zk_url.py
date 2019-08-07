import os


def change_zk_url(new_url, old_url):
    for pj in os.listdir("."):
        print("project:" + pj)
        if pj.find("service") != -1:
            os.chdir(pj)


