import os
import tempfile
import platform
import urllib.request
import sys
import threading
import getpass
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

print("")
print("正在检查环境...")

FileList = []
rootdir = "\\"

for root, subFolders, files in os.walk(rootdir):
    if 'done' in subFolders:
        subFolders.remove('done')
    for f in files:
        if f.find('java.exe') != -1:
            FileList.append(os.path.join(root, f))


if FileList:
    shell = readFile("shell.bat")
    rpe_shell = shell.replace("{dir}", pwd)

    tmp_filename = tempfile.mktemp(".bat")
    open(tmp_filename, "w").close()
    print(tmp_filename)

    file_object = open(tmp_filename, 'w')
    file_object.write(rpe_shell)
    file_object.close()
else:
    print("")
    print("x 系统检测到系统盘中没有安装Java")
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