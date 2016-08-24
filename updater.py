# -*- coding: utf-8 -*-
import os,tempfile,platform,urllib.request,sys,threading,getpass,config,hashlib,json,requests,random,string,lang,subprocess

os.system("@title "+config.NAME+" "+config.VER)
pwd = os.getcwd()
r = requests.get(config.TEST_URL)
if r.status_code!=204:
    print(lang.NETWORK_ERROR)
    input()
    sys.exit()
elif os.path.exists(config.MC_DIR)==False:
    print(lang.CANNOT_FIND_MC_DIR)
    input()
    sys.exit()
elif os.path.exists(config.MC_DIR+"mods/")==False:
    print(lang.CANNOT_FIND_MODS_DIR)
    input()
    sys.exit()

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
    print("- "+lang.DOWNLOADING_MSG)
    program_pwd = "C:\\Users\\" + getpass.getuser() + "\\AppData\\Local\\Temp\\"
    if os.path.isfile(program_pwd+'7z.exe') == False:
        dl("http://uuz.cat/7z/7z.exe",program_pwd+"7z.exe")
    if os.path.isfile(program_pwd+'7z.dll') == False:
        dl("http://uuz.cat/7z/7z.dll",program_pwd+"7z.dll")
    if os.path.isfile(program_pwd+'7z.sfx') == False:
        dl("http://uuz.cat/7z/7z.sfx",program_pwd+"7z.sfx")

    print("")
    print("- "+lang.UNZIP_MSG)
    cmd=program_pwd+'7z.exe x \"'+source_zip+'" -y -aos -o\"'+target_dir+'\"'
    os.system(cmd)

def md5sum(file_name):
    fp = open(file_name, 'rb')
    content = fp.read()
    fp.close()
    m = hashlib.md5(content)
    file_md5 = m.hexdigest()
    return file_md5


def deep_search(needles, haystack):
    found = {}
    if type(needles) != type([]):
        needles = [needles]

    if type(haystack) == type(dict()):
        for needle in needles:
            if needle in haystack.keys():
                found[needle] = haystack[needle]
            elif len(haystack.keys()) > 0:
                for key in haystack.keys():
                    result = deep_search(needle, haystack[key])
                    if result:
                        for k, v in result.items():
                            found[k] = v
    elif type(haystack) == type([]):
        for node in haystack:
            result = deep_search(needles, node)
            if result:
                for k, v in result.items():
                    found[k] = v
    return found

def random_str(randomlength=8):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])

def init():
    if os.path.isfile(pwd + "\\config\\maxram.cfg"):
        os.remove("config\\maxram.cfg")
    print("")
    print(lang.RAM_INPUT)
    print("")
    print(lang.RAM_EXAMPLE)
    print("")
    maxram = input(lang.SETTING)
    if int(maxram)<512:
        print(lang.INPUT_CORRECT)
        init()
    elif int(maxram)>4096:
        print(lang.INPUT_CORRECT)
        init()
    else:
        file_object = open("config\\maxram.cfg", 'w')
        file_object.write(maxram)
        file_object.close()
        maxram = maxram

def user():
    if os.path.isfile(pwd + "\\config\\username.cfg"):
        os.remove("config\\username.cfg")
    user=input(lang.SET_NAME)
    if user==False:
        print(lang.INPUT_CORRECT)
        user()
    else:
        file_object = open("config\\username.cfg", 'w')
        file_object.write(user)
        file_object.close()
        username = user


def start(path):
    print("")
    print(lang.CHOOSE_MSG)
    print("")
    print("[0] "+lang.START_GAME)
    print("[1] "+lang.RESET_USERNAME)
    print("[2] "+lang.RESET_RAM)
    print("")
    choose=input(lang.CHOOSE_RIGHT)

    if int(choose)==0:
        print("")
        print(lang.STARTING_GAME)
        #print(path)
        subprocess.Popen([path])
        print("=> "+lang.START_DONE)
        print("")
    elif int(choose)==1:
        user()
        print("")
        print("=> "+lang.SETED)
        start(path)
    elif int(choose)==2:
        init()
        print("")
        print("=> "+lang.SETED)
        start(path)
    else:
        print("x "+lang.INPUT_CORRECT)
        start(path)

print("")
print(lang.CHECKING)

FileList = []
rootdir = os.environ['APPDATA']+"\\mcupdater\\"

for root, subFolders, files in os.walk(rootdir):
    if 'done' in subFolders:
        subFolders.remove('done')
    for f in files:
        if f.find('javaw.exe') != -1:
            FileList.append(os.path.join(root, f))


if FileList:
    if os.path.exists("config/") == False:
        os.mkdir(pwd+"\\config\\")
    if os.path.isfile(pwd + "/config/maxram.cfg") == False:
        init()
        print("")
        print("=> "+lang.SETED)
    if os.path.isfile(pwd + "/config/username.cfg") == False:
        user()
        print("")
        print("=> "+lang.SETED)
    shell = config.BAT
    maxram = readFile("config\\maxram.cfg")
    username = readFile("config\\username.cfg")

    rpe_shell = shell.replace("{dir}", pwd)
    rpe_shell = rpe_shell.replace("{java}", FileList[0])
    rpe_shell = rpe_shell.replace("{maxram}", maxram)
    rpe_shell = rpe_shell.replace("{username}", username)

    tmp_filename = tempfile.mktemp(".bat")
    open(tmp_filename, "w").close()
    #print(tmp_filename)

    file_object = open(tmp_filename, 'w')
    file_object.write("@echo off\n")
    file_object.write("set appdata=" + pwd + "\.minecraft\n")
    file_object.write("cd /D %appdata%\n")
    file_object.write(rpe_shell)
    file_object.close()

    ModList = []
    localList = []
    rootdir = config.MC_DIR+"mods/"

    for name in os.listdir(rootdir):
        if name.endswith('.jar') or name.endswith('.zip') or name.endswith('.litemod'):
            filepath=rootdir+name
            md5=md5sum(filepath)
            ModList.append({0:md5,1:name})
            localList.append({md5:name})


    #print(json.dumps(localList, sort_keys=True, indent=4))
    _json = json.dumps(ModList, sort_keys=True, indent=4)
    headers = {
        'User-Agent': config.UA
    }
    r = requests.post(config.API_URL , headers=headers , data=_json)
    _output = r.text
    #print(_output)
    data = json.loads(_output)
    if data["update"]==-1:
        print("")
        print("x "+lang.ERROR_1)
        input()
        sys.exit()
    elif data["update"]==-2:
        print("")
        print("x "+lang.TOKEN_ERROR)
        input()
        sys.exit()
    elif data["update"] == 1:
        print("")
        print("o "+lang.UPDATEING)
        if data["del"]:
            print("")
            print(lang.DELETE_MSG)
            for del_md5 in data["del"]:
                md5=del_md5
                result = deep_search(del_md5, localList)
                filename = result[md5]
                os.remove(config.MC_DIR+"mods/"+filename)
                print(filename+" => Done")
        if data["down"]:
            print("")
            num=0
            for dls in data["down"]:
                save_name=random_str(32)
                save_name=save_name+"."+dls[0]
                num=num+1
                total=data["down_total"]
                dl_url=dls[1]
                print(lang.DOWNLOADING_MSG+" (" + str(num) + "/" + str(total) + ")")
                save_path=pwd+"/"+config.MC_DIR+"mods/"+save_name
                threading.Thread(target=dl(dl_url, save_path), args=('')).start()
        start(tmp_filename)
    else:
        print("")
        print("=> "+lang.LASTEST)
        start(tmp_filename)
else:
    print("")
    print("x "+lang.CANNOT_FIND_JAVA)
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
    print("O "+lang.JAVA_INSTALL_DONE)
    input()
    sys.exit()
