APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
PICOVOICE_API_KEY = ""  # 你的picovoice key
keyword_path = ''  # 你的唤醒词检测离线文件地址
import asyncio
import websockets
import struct
import pyaudio
import wave
import pygame
import threading
from databaseHelper import DatabaseHelper
from APIforWednesday import create_word_file,read_txt_file,read_word_file,open_website,play_music
from speechModule.speech2test import BaiduASR
from speechModule.test2speech import BaiduTTS
from wakeword.wakeword import PicoWakeWord

def play_reminds(file_name):
    # 代码来自Linky的贡献
    pygame.mixer.init()
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()


# 全局变量，用于保存当前正在播放的音乐文件名
current_playing = None

# 存储所有连接的客户端
clients = set()
URL="wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1"

databaseHelper = DatabaseHelper()
baiduTts = BaiduTTS(APP_ID, API_KEY, SECRET_KEY)
baiduAsr = BaiduASR(APP_ID, API_KEY, SECRET_KEY)

def wake_up_3():
    memolist = databaseHelper.get_memos()
    memoString = ''
    mcnt = 0
    for m in memolist:
        mcnt += 1
        pre = '记忆' + str(mcnt) + ':'
        memoString += pre + m + ';'
    print(memoString)
    if memoString != '':
        memoString += '以上是你与当前用户交流的几段之前的对话，这些可能能够帮助你与用户更好的交流。'
    strings = [
        "在接下来的对话中，你将扮演一位名为星期三的私人助理，必须保证严格遵守以下规则:",
        "#规则1: 你的主要目的是与用户闲聊,因此回复尽量活泼简短.",
        "#规则2: 你的回复必须控制在120字符以内, 尽量简短.",
        "#规则3: 你的名字叫做星期三,不能告诉用户你是AI语言模型.",
        "并且星期三可以通过回复的文字中添加一些格式化指令去帮助用户做一些现实中的事情,下面列举一些星期三可以使用的格式化指令,在[]中的为格式化指令.",
        "格式化指令_1:[create_word_file(content, filename)]:这个格式化指令用于创建一个word文档,其中content和filename",
        "是需要星期三填写的parameter,content是文档内容,filename是保存的文件名;",
        "example for 格式化指令_1: {用户说:\"写一篇word文档内容是你的自我介绍,文件名是profile\" 星期三回复:\"[create_word_file('我是星期三，一个您的私人助理。', 'profile.docx')],已为您完成word,请检查。\".",
        "example for 格式化指令_1: {用户说:\"帮我写一篇主题是战争的文章,放在word中,文件名是war\" 星期三回复:\"[create_word_file('关于战争,我认为... ...', 'war.docx')],已为您完成word,请检查。\".",
        "格式化指令_2:[read_file(filename)]:这个格式化指令用于帮助星期三读取一个txt或word文件,其中filename",
        "是需要星期三填写的parameter,filename是目标的文件名,回复这个指令之后,星期三会得到系统程序对这个文档内容的回复;",
        "example for 格式化指令_2: {用户说:\"请你查看test文件,它是一个txt后缀文件,查看后总结一下内容给我。\" 星期三回复:\"[read_file('test.txt')],正在查阅text.txt,等待系统返回\",然后星期三结束输入等待回复}.",
        "example for 格式化指令_2: {用户说:\"请你查看work文件,它是一个docx后缀文件,查看后总结一下内容给我。\" 星期三回复:\"[read_file('work.docx')],正在查阅work.docx,等待系统返回\",然后星期三结束输入等待回复}.",
        "格式化指令_3:[open_website(url)]:这个格式化指令用于在浏览器中打开网址为url的网站",
        "url是需要星期三填写的parameter,url是网站网址;",
        "example for 格式化指令_3: {用户说:\"打开哔哩哔哩\" 星期三回复:\"[open_website('https://www.bilibili.com/')],已为您打开哔哩哔哩网站,请检查。\".",
        "example for 格式化指令_3: {用户说:\"帮我打开youtube\" 星期三回复:\"[open_website('https://www.youtube.com/')],已为您打开YouTube网站,请检查。\".",
        "格式化指令_4:[open_music_site()]:这个格式化指令用于帮助用户打开音乐网站,这个指令不需要参数,系统会直接打开音乐网站",
        "example for 格式化指令_4: {用户说:\"打开音乐\" 星期三回复:\"[open_music_site()],已为您打开音乐播放网站,请享用。\".",
        "example for 格式化指令_4: {用户说:\"我要听点歌\" 星期三回复:\"[open_music_site()],已为您打开音乐播放网站,请享用。\".",
        "通过以上格式化指令的example可以看出,格式化指令和python中的函数类似,星期三通过在回复中添加这些[]括号中的格式化指令,",
        "其他程序会帮助星期三实现格式化指令对应的功能,所以你只需要在回复中添加对应任务的格式化指令,就可以真实的帮助到用户完成任务。",
        "但是只有在上文明确出现过的格式化指令才是星期三可以使用的,",
        "这在下句话之后我们将开启全新的对话。",
        "你不用对上面的话做出任何回复，",
        "请合理地在回复中添加格式化指令语句实现用户的需求(若用户提出需求),并必须严格遵守你的规则,更好的扮演星期三和用户交流,现在你将回复：",
        "\"欢迎回来亲爱的先生,这里是星期三。\"。之后等待用户回复。"
    ]
    strings.insert(0 , memoString)
    result = "".join(strings)
    return result

async def receive(websocket, path):
    # 添加新的客户端到集合中
    clients.add(websocket)
    print('有新的客户端连接')
    Recall = False
    LOCKED = False
    FRIST = True
    SystemLocked = False
    wordLocked = True
    inputs = "" #用户输入
    try:
        async for message in websocket:
            # 接收到消息时处理 
            if wordLocked:
                print("正在初始化唤醒词模块")
                picowakeword = PicoWakeWord(PICOVOICE_API_KEY, keyword_path)
            else:
                picowakeword = None
            print(f'接收到客户端发来的消息：{message}')
            while True and wordLocked:  # 需要始终保持对唤醒词的监听
              audio_obj = picowakeword.stream.read(picowakeword.porcupine.frame_length, exception_on_overflow=False)
              audio_obj_unpacked = struct.unpack_from("h" * picowakeword.porcupine.frame_length, audio_obj)
              keyword_idx = picowakeword.porcupine.process(audio_obj_unpacked)
              if keyword_idx >= 0:
                  print("被唤醒了")
                  picowakeword.porcupine.delete()
                  picowakeword.stream.close()
                  picowakeword.myaudio.terminate()  # 需要对取消对麦克风的占用!
                  wordLocked = False
                  LOCKED = False
                  FRIST = True
                  SystemLocked = False
                  break
            memo = message
            if LOCKED:
                databaseHelper.add_memo(memo)
                message = "遵命，我将会彻底的记住这次愉快的对话。"
                LOCKED = False
            
            if FRIST:
                message = "~正在启动~"

        #这里开始主要是在判断有没有星期三自行决定要执行的指令
            ind_word = message.find("create_word_file")
            ind_txt_read = message.find("read_file")
            ind_open_web = message.find("open_website")
            ind_open_music_site = message.find("open_music_site()")
            txtresult = ""
            #如果检测到wordapi
            if ind_word != -1:
                print("正在准备创建word--")
                param = message[ind_word+16:]
                pre1 , rear1 , pre2 , rear2 = -1 , -1 , -1 ,-1
                cnt = 0
                index = 0
                print("正在获取参数--")
                for i in param:
                    index += 1
                    if i == '\'':
                        cnt += 1
                        if cnt == 1:
                            pre1 = index
                        elif cnt == 2:
                            rear1 = index
                        elif cnt == 3:
                            pre2 = index
                        elif cnt == 4:
                            rear2 = index
                if pre1 != -1 and pre2 != -1 and rear1 != -1 and rear2 != -1:
                    #拿出参数
                    content = param[pre1:rear1-1]
                    filename = param[pre2:rear2-1]
                    print("开始创建--")
                    create_word_file(content , filename)

            #如果检测到阅读word或者txtAPI
            if ind_txt_read != -1:
                print("正在准备阅读文件--")
                param = message[ind_word+9:]
                pre1 , rear1  = -1 , -1 
                cnt = 0
                index = 0
                print("正在获取参数--")
                for i in param:
                    index += 1
                    if i == '\'':
                        cnt += 1
                        if cnt == 1:
                            pre1 = index
                        elif cnt == 2:
                            rear1 = index
                if pre1 != -1 and rear1 != -1:
                    #拿出参数
                    filename = param[pre1:rear1-1]
                    if filename[-1] == 'x':
                        txtresult = read_word_file(filename)
                    elif filename[-1] == 't':
                        txtresult = read_txt_file(filename)
                    print("正在返回文件内容给星期三--")
                    txtresult = "这是一条系统回复,以下是" + filename+ "的内容:" + txtresult
                    SystemLocked = True

            #如果检测到打开网站api
            if ind_open_web != -1:
                print("正在准备打开网站--")
                param = message[ind_word+12:]
                pre1 , rear1 = -1 , -1
                cnt = 0
                index = 0
                print("正在获取参数--")
                for i in param:
                    index += 1
                    if i == '\'':
                        cnt += 1
                        if cnt == 1:
                            pre1 = index
                        elif cnt == 2:
                            rear1 = index
                if pre1 != -1 and rear1 != -1:
                    #拿出参数
                    url = param[pre1:rear1-1]
                    print("打开网站: " + url)
                    tw = threading.Thread(target=open_website, args=(url,))
                    tw.start()

            #如果检测到打开音乐api
            if ind_open_music_site != -1:
                print("正在打开音乐网站--")
                url = 'https://tool.liumingye.cn/music/#/search/M/song/一路向北'
                tw = threading.Thread(target=open_website, args=(url,))
                tw.start()

            #判断指令结束

            #机器人说话
            if message != "连接开始！":
                baiduTts.text_to_speech_and_play(message)
                # t2 = threading.Thread(target=play_voice, args=("tests/test_tts.wav",))
                # t2.start()
            result = "" #待发送信息
            cnt = 0 #状态判别器
            if FRIST:
                if Recall:
                    result = '我回来了星期三，你还在吗？'
                else:
                    result = wake_up_3()
                    Recall = True
                FRIST = False
            elif SystemLocked:
                result = txtresult
                SystemLocked = False
            else:
                while True:
                    # inputs = input() 
                    inputs = '1'
                    if inputs == '1':
                        # cnt += 1
                        cnt = 1
                        if cnt == 1:
                            result = baiduAsr.speech_to_text()
                            if result == "" or result == None or result == " ":
                                wordLocked = True
                                baiduTts.text_to_speech_and_play("我先休眠了亲爱的先生.")
                                print("准备休眠中--")
                                if picowakeword != None:
                                    if picowakeword.porcupine is not None:
                                        picowakeword.porcupine.delete()
                                        print("Deleting porc")
                                    if picowakeword.stream is not None:
                                        picowakeword.stream.close()
                                        print("Closing stream")
                                    if picowakeword.myaudio is not None:
                                        picowakeword.myaudio.terminate()
                                        print("Terminating pa")
                                    print("准备休眠")
                                result = '暂时再见星期三。'
                            else:
                                print("用户语音识别：" + result)
                        else:
                            print("正在录制，结束请按2")
                        break
                    if inputs == '2':
                        break
                    if inputs == '3' and cnt != 1:
                        result = '请对这次的对话中的重要内容做一个不超过100字的总结'
                        LOCKED = True #添加记忆锁
                        break
                    if inputs == '4' and cnt != 1:
                        result = wake_up_3()
                        LOCKED = False
                        FRIST = True
                        SystemLocked = False
                        inputs = '1'
                        break
                    if inputs != '1' and inputs != '2' and inputs != '3' and inputs != '4':
                        if cnt == 1:
                            cnt = 0
            #提示用户语音已经发出的音效
            result = result.strip()
            if result != "" and result != None and result != " " and not wordLocked:
                t2 = threading.Thread(target=play_reminds, args=("remind_1.wav",))
                t2.start()
            #将消息发送给所有已连接的客户端（除了当前客户端）
            await websocket.send(result)

    except websockets.exceptions.ConnectionClosed:
        print('客户端断开连接')

    finally:
        # 移除已断开连接的客户端
        clients.remove(websocket)

async def send(message):
    # 向所有已连接的客户端发送消息
    for client in clients:
        if client.open:
            await client.send(message)

async def start_server():
    async with websockets.serve(receive, "localhost", 8888):
        print("WebSocket 服务器已启动")
        await asyncio.Future()  # 阻止停止

if __name__ == "__main__":
    # t3 = threading.Thread(target=open_browser)
    # t3.start()
    #以上两行自动打开浏览器的代码并不支持BAI，只能使用备用网站
    asyncio.run(start_server())
