# give dgmanager a path then it will add a copy of that path to the dotfiles repo and update that copy every time you run dgmanager update

from os.path import isdir
import sys
import os
import git
import shutil

DEFAULT_CONFIG = ""
GLOBAL_CONFIG_PATH = os.path.expanduser("~/.config/dfmanager/dfmanager")
REPO_PATH = ""

def copyfile(src, dst):
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    elif os.path.isfile(src):
        shutil.copy(src, dst)

def dfmanager_init(name):
    # mkdir path if it doesnt alredy exist
    # call git init on that dir
    # creat the .dfmanager file with defalt config
    
    
    # path = os.path.abspath(path)
    # if not os.path.exists(path):
    #     os.mkdir(path)
    
    repo = git.Repo.init(name)
    
    f = open(os.path.abspath(name + "/.dfmanager"), "a")
    config = "\npath=" + os.path.expanduser(name + "/.dfmanager")
    f.write(DEFAULT_CONFIG + config)
    f.close()


def dfmanager_add(add, argv):
    global REPO_PATH
    f = open(os.path.expanduser(REPO_PATH + ".dfmanager"), "r")
    prev_config = f.read()
    f.close()
    if not "--force" in argv:
        for i in prev_config.split("\n"):
            if i == add:
                print(add + " alredy on watch list")
                print("run dfmanager add --force " + add + " to force add it")
                return
    f = open(os.path.expanduser(REPO_PATH + ".dfmanager"), "w")
    f.write(prev_config + add + "\n")
    print("added " + add + " to watch list")
    f.close()

def dfmanager_update(argv):
    dest_path = os.path.expanduser(REPO_PATH)
    f = open(os.path.expanduser(REPO_PATH + ".dfmanager"), "r")
    for i in f.read().split("\n"):
        dst = dest_path + i.split("/")[-1]
        if i.strip() == "":
            continue
        if os.path.exists(dst):
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            elif os.path.isfile(dst):
                os.remove(dst)
        print("updating " + i)
        copyfile(os.path.expanduser(i), dst)


def load_global_config():
    global REPO_PATH
    if not os.path.exists(GLOBAL_CONFIG_PATH):
        return

    f = open(GLOBAL_CONFIG_PATH, "r")
    config = f.read()
    for i in config.split("\n"):
        i = i.strip()
        if i == "":
            continue
        key = i.split("=")[0]
        value = i.split("=")[1]

        if key == "path":
            if not value[-1] == "/":
                value += "/"
            REPO_PATH = value


if __name__ == "__main__":
    load_global_config()
    if len(sys.argv) < 2:
        exit()
    if sys.argv[1] == "init":
        dfmanager_init(sys.argv[2])
    elif sys.argv[1] == "add":
        dfmanager_add(sys.argv[2], sys.argv)
    elif sys.argv[1] == "update":
        dfmanager_update(sys.argv)




