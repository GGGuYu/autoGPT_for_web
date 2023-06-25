# 感谢Linky小伙伴对于Windows版本运行说明以及代码的贡献!
from aip import AipSpeech
# from playsound import playsound # windows环境下playsound运行可能不稳定
# pip install pygame
import pygame # 导入pygame，playsound报错或运行不稳定时直接使用
import asyncio


class BaiduTTS:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def text_to_speech_and_play(self, text=""):
        result = self.client.synthesis(text, 'zh', 1, {
            'spd': 6,  # 语速
            'vol': 10,  # 音量大小
            'per': 4  # 发声人 百度丫丫
        })  # 得到音频的二进制文件

        if not isinstance(result, dict):
            with open("./audio.mp3", "wb") as f:
                f.write(result)
        else:
            print("语音合成失败", result)
        # playsound('./audio.mp3')  # playsound无法运行时删去此行改用pygame，若正常运行择一即可
        self.play_audio_with_pygame('audio.mp3')  # 注意pygame只能识别mp3格式

    def play_audio_with_pygame(self, audio_file_path):
        # 代码来自Linky的贡献
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()

if __name__ == '__main__':
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''
    baidutts = BaiduTTS(APP_ID, API_KEY, SECRET_KEY)
    baidutts.text_to_speech_and_play('春天来了，每天的天气都很好！')