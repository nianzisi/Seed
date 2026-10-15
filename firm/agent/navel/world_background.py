import json

from agent.message import Message_Control
from agent.send import Send
from agent.tools.get_sql import tool
from agent.tools.var import var


class World_creat(Send):

    def __init__(self, _Message: Message_Control = None, category: str = "navel"):
        super().__init__(_Message=_Message or Message_Control(), category=category)

    def template(self, path: str = r"D:\Seed\firm\agent\navel\template\世界背景生成.txt", key=None):
        if key is None:
            key = {"字数": None}
        self.add_system(var(path, key))

    def run_(self) -> str:
        with open(r"D:\Seed\firm\agent\navel\输出物\世界观.txt", mode="w", encoding="utf-8") as f:
            self.template()
            self.add_ask(input("输入:"))
            text = self.send().text
            result = json.loads(text)["choices"][0]["message"]["content"]
            f.write(result)
        return result


@tool("navel")
def ask_user(msg: str):
    """
    向用户提问
    :param msg: 提问内容
    :return: 返回用户的回答
    """
    print(f"询问:{msg}")
    return input()


if __name__ == "__main__":
    World_creat().run_()