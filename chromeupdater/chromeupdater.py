# coding=utf-8
import urllib.request, http.cookiejar, json, re, os, zipfile

def findstr(rule, string):
    find_str = re.compile(rule)
    return find_str.findall(string)

class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)
    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)
    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

class filelib:
    def open(self, path, mode='r'):
        file = open(path, mode)
        content = file.read()
        file.close()
        return content
    def write(self, path, content, mode='w'):
        file = open(path, mode)
        file.write(content)
        file.close()
        return True
    def mkdir(self, dirname):
        try:
            os.mkdir(dirname)
        except WindowsError:
            pass
        return True

class utillib:
    def __init__(self):
        self.branch = 'Stable'
        self.structure = 'x86'
        self.version = '0.0.0.0'
        self.url = []
        self.filename = ''
        self.cfg = {}
    def unzip(self, src, dest, password=''):
        with zipfile.ZipFile(src) as zfile:
            try:
                zfile.extractall(path=dest, pwd=password)
            except RuntimeError as e:
                pass
    def loadcfg(self):
        cont = filelib().open('settings.json')
        cont = re.sub('(?<!:)\\/\\/.*|\\/\\*(\\s|.)*?\\*\\/', '', cont)
        cont = cont.replace('\\', '\\\\').replace('\\\\"', '\\"')
        self.cfg = json.loads(cont)
        self.branch = self.cfg["Branch"]
        self.structure = self.cfg["Structure"]
        self.version = self.cfg["Version"]
    def older(self, v2):
        v1 = self.version.split('.')
        v2 = v2.split('.')
        vparts = min(len(v1), len(v2))
        for i in range(0, vparts):
            if int(v2[i])>int(v1[i]):
                return True
            if int(v2[i])<int(v1[i]):
                return False
        return False
    def cbk(self, a, b, c):
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print('\r%.2f%%' % per, end="")
    def download(self):
        for url in self.url:
            try:
                print('Downloading %s from url: %s' % (self.filename, url))
                urllib.request.urlretrieve(url, '.\\'+self.filename, self.cbk)
                print('Download complete!')
                return True
            except urllib.error.URLError:
                pass
            except ConnectionResetError:
                pass
    def extract(self):
        print('Extracting...')
        os.system('7za.exe x "'+self.filename+'" -o. -aoa -y')
        os.system('del /f /q "'+self.filename+'"')
        os.system('7za.exe x "chrome.7z" -o. -aoa -y')
        os.system('del /f /q chrome.7z')
        os.system('move .\\Chrome-bin\\'+self.version+' ..\\')
        os.system('move .\\Chrome-bin\\*.* ..\\')
        os.system('rd /s /q Chrome-bin')
        print('Extract complete!')
    def gc(self):
        print('Installing greenchrome...', end="")
        if os.path.exists('..\\GreenChrome.ini'):
            os.system('copy /y .\\gc\\GreenChrome.ini ..\\GreenChromeNew.ini')
        else:
            os.system('copy /y .\\gc\\GreenChrome.ini ..\\')
        os.system('copy /y .\\gc\\'+self.structure+'\\*.dll ..\\')
        print('complete!')
    def patch(self):
        print('Injecting GreenChrome.dll to Chrome.')
        os.system('setdll.exe /d:..\\GreenChrome.dll ..\\chrome.exe')
        os.system('del /f /q ..\\chrome.exe~')
    def clean(self):
        print('Cleaning old version...')
        os.system('rd /s /q ..\\'+self.version)
    def replaced(self, ver):
        self.cfg["Version"] = ver
        filelib().write('settings.json', json.dumps(self.cfg))
    def debug(self):
        print(self.branch)
        print(self.structure)
        print(self.version)

class weblib:
    def query(self, url, method='GET', postdata={}):
        if method != 'GET':
            if postdata != {}:
                postdata = postdata.encode('utf-8')
                req = urllib.request.Request(url, postdata, method=method)
            else:
                req = urllib.request.Request(url, method=method)
        else:
            req = urllib.request.Request(url)
        urllib.request.install_opener(urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())))
        result = urllib.request.urlopen(req).read().decode('utf-8')
        return result

class chrome:
    def __init__(self):
        # https://github.com/lyonna/ChromeOfflineInstallerDownloadAPI/blob/master/coi.php
        self.url = 'https://tools.google.com/service/update2'
        self.verlist = {
            'win': '6.3'
        }
        self.appidlist = {
            'win_stable': '{8A69D345-D564-463C-AFF1-A69D9E530F96}',
            'win_beta': '{8A69D345-D564-463C-AFF1-A69D9E530F96}',
            'win_dev': '{8A69D345-D564-463C-AFF1-A69D9E530F96}',
            'win_canary': '{4EA16AC7-FD5A-47C3-875B-DBF4A2008C20}'
        }
        self.aplist = {
            'win_stable_x86': '-multi-chrome',
            'win_stable_x64': 'x64-stable-multi-chrome',
            'win_beta_x86': '1.1-beta',
            'win_beta_x64': 'x64-beta-multi-chrome',
            'win_dev_x86': '2.0-dev',
            'win_dev_x64': 'x64-dev-multi-chrome',
            'win_canary_x86': '',
            'win_canary_x64': 'x64-canary'
        }
        self.version = '0.0.0.0'
        self.branch = 'Stable'
        self.structure = 'x86'
        self.downloadUrl = []
    def getInfo(self, branch, structure):
        ver = self.verlist['win']
        appid = self.appidlist['win_'+branch.lower()]
        ap = self.aplist['win_'+branch.lower()+'_'+structure.lower()]
        postData = "<?xml version='1.0' encoding='UTF-8'?><request protocol='3.0' version='1.3.23.9' shell_version='1.3.21.103' ismachine='0' sessionid='{3597644B-2952-4F92-AE55-D315F45F80A5}' installsource='ondemandcheckforupdate' requestid='{CD7523AD-A40D-49F4-AEEF-8C114B804658}' dedup='cr'><hw sse='1' sse2='1' sse3='1' ssse3='1' sse41='1' sse42='1' avx='1' physmemory='12582912' /><os platform='win' version='"+ver+"' arch='"+structure.lower()+"'/><app appid='"+appid+"' ap='"+ap+"' version='' nextversion='' lang='' brand='GGLS' client=''><updatecheck/></app></request>"
        res = weblib().query(self.url, 'POST', postData)
        self.version = findstr('<manifest version="(\d*?\.\d*?\.\d*?\.\d*?)">', res)[0]
        self.filename = findstr('event="install" run="(.*?)"/>', res)[0]
        downloadUrl = findstr('<url codebase="(.*?)"/>', res)
        for dUrl in downloadUrl:
            self.downloadUrl.append(dUrl+self.filename)

def main():
    current = utillib()
    new = utillib()
    current.loadcfg()
    new.branch = current.branch
    new.structure = current.structure
    updater = chrome()
    updater.getInfo(new.branch.lower(), new.structure.lower())
    print('checking new version...')
    new.version = updater.version
    new.url = updater.downloadUrl
    new.filename = updater.filename
    if current.older(new.version):
        print('Branch: '+current.branch+'  Structure: '+current.structure)
        print('A newer version found, '+current.version+' -> '+new.version)
        input("Please close chrome and press enter to continue.")
        new.download()
        new.extract()
        new.gc()
        new.patch()
        current.clean()
        current.replaced(new.version)
    else:
        print('No updates.')

if __name__ == '__main__':
    main()
