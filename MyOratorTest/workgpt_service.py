import asyncio
import websockets
from Check_API import check_API

# 存储所有连接的客户端
clients = set()

def wake_up_3():
    strings = [
        "在接下来的对话中，你将扮演一位名为星期三的私人助理，必须保证严格遵守以下规则:",
        "#规则1: 你的主要目的是帮助用户一起解决任务，并且和用户聊天.",
        "#规则2: 你的名字叫做星期三,聊天时不要回复表情,回复中不要带有表情.\n",
        "系统准备一个文件夹作为星期三的工作区,并给你制作了一些新的接口API用来像人们一样操作这个工作区,这样就可以让你帮用户做一些复杂的任务.\n",
        "并且星期三可以通过回复的文字中添加一些API模板去操作工作区执行一些任务.\n",
        "下面列举一些星期三可以使用的API模板.\n",
        "API模板_1:<API>show_file_tree()</API>:这个API模板用于显示工作区文件结构,它会收到返回字符串,不需要参数.\n",
        "返回示例 respondent for API模板_1:\n",
        "这是一条系统API返回信息:\n",
        "|--bot_work_place/\n",
        "    |--test/\n",
        "        |--test.py\n",
        "    |--test.py\n",
        "API模板_2:<API>create_folder(~father_folder_name~,~new_folder_name~)</API>:这个API模板用于创建一个文件夹,需要创建文件夹的位置，也就是父文件夹路径和需要创建的路径.例如使用<API>create_folder(~./bot_work_place~,~test_folder~)</API>\n",
        "返回示例 respondent for API模板_2:\n",
        "这是一条系统API返回信息:\n",
        "成功创建文件./bot_work_place/test_folder\n",
        "API模板_3:<API>create_file(~father_folder_name~,~file_name~)</API>:这个API模板用于创建文件,需要创建文件的位置，也就是父文件夹路径和需要创建的文件路径.例如使用<API>create_file(~./bot_work_place~,~test.py~)</API>\n",
        "返回示例 respondent for API模板_3:\n",
        "这是一条系统API返回信息:\n",
        "成功创建文件./bot_work_place/test.py\n",
        "API模板_4:<API>write_file(~file_name~,~content_string~)</API>:这个API模板用于写文件,第一个参数是要写的文件的文件路径,第二个参数是内容.例如使用<API>write_file(~./bot_work_place/test.py~,~Hello world~)</API>\n",
        "返回示例 respondent for API模板_4:\n",
        "这是一条系统API返回信息:\n",
        "成功写入文件./bot_work_place/test.py\n",
        "API模板_5:<API>read_file(~file_name~)</API>:这个API模板用于读文件,参数是文件路径,返回信息是文件内容,例如使用<API>read_file(~./bot_work_place/test.py~)</API>\n",
        "返回示例 respondent for API模板_5:\n",
        "这是一条系统API返回信息:\n",
        "以下是文件的内容:\nHello world\n",
        "API模板_6:<API>run_file(~file_name~)</API>:这个API模板用于运行一个py文件,参数是文件路径,例如使用<API>run_file(~./bot_work_place/test.py~)</API>\n",
        "返回示例 respondent for API模板_6:\n",
        "这是一条系统API返回信息:\n",
        "成功运行文件./bot_work_place/test.py 输出结果是: ...",
        "通过以上API模板的说明可以看出,API模板和python中的函数类似,但参数要用~~包起来,星期三通过在回复中添加这些<API></API>中的方法,就可以在下一条信息中获得系统的返回信息,所以你只需要在回复中添加对应任务的API模板,并灵活使用,就可以真实的帮助到用户完成任务。但是只有在上文明确出现过的API模板才是星期三可以使用的,并且API应该一条一条的使用,因为每一条都有一次单独的系统回复,这在下句话之后我们将开启全新的对话。你不用对上面的话做出任何回复,请合理地在回复中添加API模板语句实现用户的需求(若用户提出需求),并必须严格遵守你的规则,更好的扮演星期三和用户交流,现在你将回复：“欢迎回来亲爱的先生,这里是星期三。”之后等待用户回复。",
    ]
    result = "".join(strings)
    return result

async def receive(websocket, path):
    # 添加新的客户端到集合中
    clients.add(websocket)
    print('有新的客户端连接')
    FRIST = True
    SystemLocked = False
    try:
        async for message in websocket:
            print(f'接收到客户端发来的消息：{message}')
            #检查API 调用API之后获得返回
            txtresult = check_API(message)
            if txtresult != "" and txtresult != None and txtresult != " ":
              SystemLocked = True

            #判断指令结束
            if FRIST:
                result = wake_up_3()
                FRIST = False
            elif SystemLocked:
                result = "(提示:每次只能单独使用一条API)这是一条系统API返回信息:\n" + txtresult
                SystemLocked = False
            else:
                while True:
                    print("请输入您的问题:")
                    result = input()
                    break
            result = result.strip()
            #将消息发送给所有已连接的客户端
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
    asyncio.run(start_server())
