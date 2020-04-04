ChromeUpdater-Python
======
由于[shuax](https://www.shuax.com)写的ChromeUpdater已不再更新，且[TsungKang](https://csharp.love)写的[ChromeUpdaterCSharp](https://csharp.love/chrome_update_tool.html)需要.Net Framework 4.5及其以上版本，所以在看了TK的[代码](https://github.com/TkYu/ChromeUpdater)后写了一个Python版自用。

使用方法
------
下载后执行`chromeupdater.bat`即可。

如有需要启动浏览器时检查更新，请配置`GreenChrome.ini`文件末尾部分。

设置
------
修改`chromeupdater`目录下的`settings.json`即可。

`Branch`是分支，有`Stable`,`Beta`,`Dev`,`Canary`四个分支版本。

`Structure`是版本位数，分别为`x86`,`x64`。

`Version`是当前版本号，一般不推荐修改。

依赖/使用
------
[phuslu/pybuild3](https://github.com/phuslu/pybuild3)

[GreenChrome](https://github.com/shuax/GreenChrome)

[7-Zip](https://www.7-zip.org/)