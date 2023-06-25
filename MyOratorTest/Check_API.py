from workfileAPI import *
import re
import string
from functools import reduce
import re
import string

def ch_str2en_str(s):
    mappings = {
        '，': ',',
        '。': '.',
        '：': ':',
        '（': '(',
        '）': ')',
        '‘': '\'',
        '’': '\'',
        '“': '"',
        '”': '"'
    }
    return reduce(lambda x, y: x.replace(y, mappings[y]), mappings, s)



def check_API(message):
            #这里开始主要是在判断有没有星期三自行决定要执行的指令
            if message.find("<API>") != -1:
              show_file_tree_ind = message.find("show_file_tree")
              #检测到ls命令
              if show_file_tree_ind != -1:
                  return show_file_tree('./bot_work_place')

              create_folder_ind = message.find("create_folder")
              #检测创建文件夹命令
              if create_folder_ind != -1:
                  pattern = r"create_folder\(~(.*?)~,~(.*?)~\)"
                  result = re.findall(pattern, message[message.find("<API>")+5:message.find("</API>")])
                  p1 , p2 = result[0][0] , result[0][1]
                  return create_folder(p1,p2)

              create_file_ind = message.find("create_file")
              #检测创建文件命令
              if create_file_ind != -1:
                    pattern = r"create_file\(~(.*?)~,~(.*?)~\)"
                    result = re.findall(pattern, message[message.find("<API>")+5:message.find("</API>")])
                    p1, p2 = result[0][0], result[0][1]
                    return create_file(p1,p2)
              
              write_file_ind = message.find("write_file")
              #检测写文件命令
              if write_file_ind != -1:
                    pattern = r"write_file\(~(.*?)~,~(.*?)~\)"
                    result = re.findall(pattern, message[message.find("<API>")+5:message.find("</API>")])
                    p1 , p2 = result[0][0] , result[0][1]
                    p1 = ch_str2en_str(p1)
                    p2 = ch_str2en_str(p2)
                    return write_file(p1,p2)

              read_file_ind = message.find("read_file")
              #检测读文件命令
              if read_file_ind != -1:
                    pattern = r"read_file\(~(.*?)~\)"
                    result = re.findall(pattern, message[message.find("<API>")+5:message.find("</API>")])
                    p1 = result[0]
                    return read_file(p1)

              run_file_ind = message.find("run_file")
              #检测运行py文件命令
              if run_file_ind != -1:
                    pattern = r"run_file\(~(.*?)~\)"
                    result = re.findall(pattern, message[message.find("<API>")+5:message.find("</API>")])
                    print("result: "+ str(result))
                    p1 = result[0]
                    print("p1: " + p1)
                    return run_file(p1)