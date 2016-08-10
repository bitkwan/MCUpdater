import os
import tempfile
import platform
import urllib.request
import sys
import threading
import getpass
import config
import hashlib
import json
import requests

pwd = os.getcwd()
def readFile(file):
    f = open(file)
    line = f.readline()
    while line:
        txt = str(line,)
        line = f.readline()
    f.close()
    return(txt)

def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

def callbackfunc(blocknum, blocksize, totalsize):
    global url
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    downsize=blocknum * blocksize
    if downsize >= totalsize:
    	downsize=totalsize
    s ="%.2f%%"%(percent)+"====>"+"%.2f"%(downsize/1024/1024)+"M/"+"%.2f"%(totalsize/1024/1024)+"M \r"
    sys.stdout.write(s)
    sys.stdout.flush()
    if percent == 100:
        print('')
def dl(url,filename):
    urllib.request.urlretrieve(url, filename, callbackfunc)

def unzip(source_zip,target_dir):
    print("")
    print("- 正在下载依赖")
    program_pwd = "C:\\Users\\" + getpass.getuser() + "\\AppData\\Local\\Temp\\"
    if os.path.isfile(program_pwd+'7z.exe') == False:
        dl("http://uuz.cat/7z/7z.exe",program_pwd+"7z.exe")
    if os.path.isfile(program_pwd+'7z.dll') == False:
        dl("http://uuz.cat/7z/7z.dll",program_pwd+"7z.dll")
    if os.path.isfile(program_pwd+'7z.sfx') == False:
        dl("http://uuz.cat/7z/7z.sfx",program_pwd+"7z.sfx")

    print("")
    print("- 正在解压Java")
    cmd=program_pwd+'7z.exe x \"'+source_zip+'" -y -aos -o\"'+target_dir+'\"'
    os.system(cmd)

def md5sum(file_name):
    fp = open(file_name, 'rb')
    content = fp.read()
    fp.close()
    m = hashlib.md5(content)
    file_md5 = m.hexdigest()
    return file_md5

print("")
print("正在检查环境...")

FileList = []
rootdir = os.environ['APPDATA']+"\\mcupdater\\"

for root, subFolders, files in os.walk(rootdir):
    if 'done' in subFolders:
        subFolders.remove('done')
    for f in files:
        if f.find('java.exe') != -1:
            FileList.append(os.path.join(root, f))


if FileList:
    shell = readFile(config.BAT_PATH)
    rpe_shell = shell.replace("{dir}", pwd)
    rpe_shell = rpe_shell.replace("{java}", FileList[0])

    tmp_filename = tempfile.mktemp(".bat")
    open(tmp_filename, "w").close()
    print(tmp_filename)

    file_object = open(tmp_filename, 'w')
    file_object.write(rpe_shell)
    file_object.close()

    ModList = []
    rootdir = config.MC_DIR+"mods/"

    for root, subFolders, files in os.walk(rootdir):
        if 'done' in subFolders:
            subFolders.remove('done')
        for f in files:
            if f.find('.jar') != -1:
                filepath=os.path.join(root, f)
                ModList.append({md5sum(os.path.join(root, f)):filepath.replace(rootdir, "")})
            if f.find('.zip') != -1:
                filepath=os.path.join(root, f)
                ModList.append({md5sum(os.path.join(root, f)):filepath.replace(rootdir, "")})
            if f.find('.litemod') != -1:
                filepath=os.path.join(root, f)
                ModList.append({md5sum(os.path.join(root, f)):filepath.replace(rootdir, "")})

    #print(json.dumps(ModList, sort_keys=True, indent=4))
    _json = json.dumps(ModList, sort_keys=True, indent=4)
    r = requests.post(config.API_URL,data=_json)
    #print(r.text)
else:
    print("")
    print("x 系统检测到没有安装Java")
    bit=platform.machine()
    if bit=="AMD64":
        packge_name = "j8x64.zip"
    else:
        packge_name="j8x86.zip"
    print("")
    print("- 正在下载Java环境包..")

    tmp_filename = tempfile.mktemp(".zip")

    threading.Thread(target=dl("http://uuz.cat/"+packge_name,tmp_filename), args=('')).start()
    program_pwd=os.environ['APPDATA']+"\\mcupdater\\"
    if os.path.exists(program_pwd)==False:
        os.mkdir(program_pwd)
    unzip(tmp_filename,program_pwd)
    print("")
    print("O Java环境已经安装完成,请重启本程序")