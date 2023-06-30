## 1.拥有一个独立文件夹并可自主操作的智能助手 可调试程序

B站的朋友直接clone下来，将MyOratorTest拖入您的IDE中

1.打开workgpt_service.py启动ws服务器

2.将newbing_service.js复制在newbing网页的控制台中，回车
成功复现视频中的实验程序

## 2.newbing驱动语音版助手星期三(唤醒词加连续对话)

在new_bing_service.py中

1. 将您的百度语音(免费的百度云服务)的，将以下填好
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
在picovoice官网获取一个您自己需要的唤醒词(免费)，替换掉对应的唤醒词文件 将以下填好
PICOVOICE_API_KEY = ""  # 你的picovoice key

2.启动newbing_service.py 等待1到两秒看到程序输出服务器启动

3.将newbing_service.js复制在newbing网页的控制台中，回车

4.此时控制台会初始化唤醒词模块，大约一秒后初始化成功，即可语音唤醒助手
