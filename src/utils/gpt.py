import os
import qianfan
import asyncio


class ChatHistory:
    def __init__(self, max_bytes=1024):
        self.history = []
        self.max_bytes = max_bytes

    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.history.append(message)
        self._ensure_within_limit()

    def _ensure_within_limit(self):
        total_bytes = sum(len(m["content"].encode('utf-8')) for m in self.history)
        while total_bytes > self.max_bytes:
            self.history.pop(0)
            total_bytes = sum(len(m["content"].encode('utf-8')) for m in self.history)

    def get_history(self):
        return self.history


def chat_with_qianfan(user_input):
    chat_comp = qianfan.ChatCompletion()

    # 添加用户输入到对话历史
    chat_history.add_message("user", user_input)

    # 发送请求到千帆
    response = chat_comp.do(model="ERNIE-3.5-8K", messages=chat_history.get_history(), system="你是一只可爱的小熊，回复要非常简短。")

    # 获取AI回复并添加到对话历史
    ai_reply = response["result"]
    chat_history.add_message("assistant", ai_reply)

    return ai_reply


# 初始化对话历史
chat_history = ChatHistory()


# # 示例调用
# async def main():
#     user_input = "你好"
#     reply = await chat_with_qianfan(user_input)
#     print(reply)
#
#     user_input = "北京有哪些美食"
#     reply = await chat_with_qianfan(user_input)
#     print(reply)
#
#
# # 运行异步任务
# asyncio.run(main())
