import json

from agent.message import Message_Control
from agent.send import Send
from agent.tools.var import var


class Outline_creat(Send):

    def __init__(self, _Message: Message_Control = None, category: str = None):
        super().__init__(_Message=_Message or Message_Control(), category=category)

    def template(self, path: str = r"D:\Seed\firm\agent\navel\template\大纲.txt", key=None):
        with open(r"D:\Seed\firm\agent\navel\输出物\世界观.txt", mode="r", encoding="utf-8") as ff:
            world = ff.read()
            key["世界观"] = world
        with open(r"D:\Seed\firm\agent\navel\输出物\角色卡\初始角色.json", mode="r", encoding="utf-8") as ff:
            world = ff.read()
            key["角色卡片"] = world
        self.add_ask(var(path, key))

    def run_(self) -> str:
        self.template()
        text = self.send().text
        result = json.loads(text)["choices"][0]["message"]["content"]
        with open(r"D:\Seed\firm\agent\navel\输出物\大纲.txt", mode="w", encoding="utf-8") as f:
            try:
                json.dump(json.loads(result), f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(e)
                f.seek(0)
                f.write(result)
        return result


if __name__ == "__main__":
    Outline_creat().run_()
