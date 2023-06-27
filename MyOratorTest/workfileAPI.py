import os
import sys
import subprocess
import shutil

# 显示工作区树形结构函数，接受一个文件夹路径和一个缩进级别作为参数
def show_file_tree(path, level=0):
    # 定义一个空字符串，用来存储树形结构
    tree = ""
    # 如果路径是一个文件，就把文件名和缩进加到字符串上
    if os.path.isfile(path):
        tree += " " * level + "|--" + os.path.basename(path) + "\n"
    # 如果路径是一个文件夹，就把文件夹名和缩进加到字符串上，并递归调用函数处理子文件夹
    elif os.path.isdir(path):
        tree += " " * level + "|--" + os.path.basename(path) + "/\n"
        for sub_path in os.listdir(path):
            tree += show_file_tree(os.path.join(path, sub_path), level + 4)
    # 返回树形结构字符串
    return tree


# 创建文件夹函数，接受一个文件夹名作为参数
def create_folder(father_folder_name , new_folder_name):
    # 拼接要创建的文件夹路径
    folder_path = os.path.join(father_folder_name, new_folder_name)
    # 判断文件夹是否已经存在，如果不存在，就创建
    if not os.path.exists(folder_path):
        # 使用os.makedirs方法创建文件夹，可以自动创建多层目录
        os.makedirs(folder_path)
        # 打印出成功创建的信息
        print("成功创建文件夹：" + folder_path)
        return "成功创建文件夹：" + folder_path
    else:
        # 如果文件夹已经存在，就打印出提示信息
        print("文件夹已经存在：" + folder_path)
        return "文件夹已经存在：" + folder_path


# 创建文件函数，接受一个文件名作为参数
def create_file(father_folder_name , file_name):
    # 拼接要创建的文件路径
    file_path = os.path.join(father_folder_name, file_name)
    # 使用open函数以"x"模式创建文件，如果文件已存在则返回错误
    try:
        f = open(file_path, "x")
        # 关闭文件
        f.close()
        # 打印出成功创建的信息
        print("成功创建文件：" + file_path)
        return "成功创建文件：" + file_path
    except FileExistsError:
        # 如果文件已存在，就打印出提示信息
        print("文件已经存在：" + file_path)
        return "文件已经存在：" + file_path


# 写入函数，接受一个文件名和一个字符串作为参数
def write_file(file_name, content_string):
    # 使用try...except语句来尝试写入文件
    try:
        # 使用open函数以"w"模式打开文件，如果文件不存在，则创建文件
        with open(file_name, "w", encoding="utf-8") as f:
            # 使用write方法将字符串写入文件
            f.write(content_string)
            # 打印出成功写入的信息
            print("成功写入文件：" + file_name)
            return "成功写入文件：" + file_name
    # 如果发生异常，就捕获并打印出异常信息
    except:
        # 获取异常类型和值
        e_type, e_value = sys.exc_info()[:2]
        # 打印出失败写入的信息和异常信息
        print("写入文件失败：" + file_name)
        print("异常类型：" + str(e_type))
        print("异常信息：" + str(e_value))
        return "写入文件失败：" + file_name + "\n" + "失败类型：" + str(e_type) + "\n" + "失败信息：" + str(e_value)

# 读出文件函数，接受一个文件名作为参数
def read_file(file_name):
    # 使用try...except语句来尝试读取文件
    try:
        # 使用open函数以"r"模式打开文件，如果文件不存在，则抛出异常
        with open(file_name, "r") as f:
            # 使用read方法读取文件内容，并赋值给一个变量
            content = f.read()
            # 返回文件内容
            return "以下是文件中的内容: " + "\n"+ content
    # 如果发生异常，就捕获并打印出异常信息
    except:
        # 获取异常类型和值
        e_type, e_value = sys.exc_info()[:2]
        # 打印出失败读取的信息和异常信息
        print("读取文件失败：" + file_name)
        print("异常类型：" + str(e_type))
        print("异常信息：" + str(e_value))
        return "读取文件失败：" + file_name + "\n" + "失败类型：" + str(e_type) + "\n" + "失败信息：" + str(e_value)


# 运行PY文件函数，接受一个文件名作为参数
def run_file(file_name):
    # 使用subprocess.Popen方法创建一个子进程，执行python命令，并传入文件名
    # 设置stdout和stderr参数为subprocess.PIPE，表示将标准输出和标准错误重定向到管道
    p = subprocess.Popen(["python", file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 使用communicate方法等待子进程结束，并获取标准输出和标准错误的字符串
    output, error = p.communicate()
    # 判断标准错误是否为空，如果为空，表示运行成功，否则表示运行失败
    if error == b"":
        # 打印出成功运行的信息和标准输出
        # print("成功运行：" + file_name)
        print(output.decode())
        return "成功运行：" + file_name + "\n" + output.decode()
    else:
        # 打印出失败运行的信息和标准错误
        print("运行失败：" + file_name)
        print(error.decode())
        return "运行失败：" + file_name + "\n" + error.decode()



# 删除文件函数，接受一个文件名作为参数
def delete_file(file_name):
    # 使用try...except语句来尝试删除文件
    try:
        # 使用os.remove或os.unlink方法删除文件，两者功能相同
        os.remove(file_name)
        # 或者
        # os.unlink(file_name)
        # 打印出成功删除的信息
        print("成功删除文件：" + file_name)
        return "成功删除文件：" + file_name
    # 如果发生异常，就捕获并打印出异常信息
    except Exception as e:
        # 打印出失败删除的信息和异常信息
        print("删除文件失败：" + file_name)
        print("异常信息：" + str(e))
        return "删除文件失败：" + file_name + "\n" + "失败信息：" + str(e)

# 删除文件夹函数，接受一个文件夹名作为参数
def delete_folder(folder_name):
    # 使用try...except语句来尝试删除文件夹
    try:
        # 如果文件夹是空的，就使用os.rmdir方法删除
        os.rmdir(folder_name)
        # 打印出成功删除的信息
        print("成功删除空文件夹：" + folder_name)
        return "成功删除空文件处：" + folder_name
    except OSError:
        # 如果文件夹不是空的，就使用shutil.rmtree方法删除
        try:
            shutil.rmtree(folder_name)
            # 打印出成功删除的信息
            print("成功删除非空文件夹：" + folder_name)
            return "成功删除非空文件夹：" + folder_name
        except Exception as e:
            # 如果遇到其他错误，就打印出失败删除的信息和异常信息
            print("删除文件夹失败：" + folder_name)
            print("异常信息：" + str(e))
            return "删除文件夹失败：" + folder_name + "\n" + "异常信息：" + str(e)
