import json

from agent.message import Message_Control
from agent.send import Send
from agent.tools.var import var


class Chapter(Send):

    def __init__(self, _Message: Message_Control = None, category: str = None):
        super().__init__(_Message=_Message or Message_Control(), category=category)

    def template(self, path: str = r"D:\Seed\firm\agent\navel\template\场景.txt", key=None):
        self.add_system(var(path, key))

    def run_(self) -> str:
        self.template()
        with open(r"D:\Seed\firm\agent\navel\输出物\大纲.txt", mode="r", encoding="utf-8") as _f:
            outline = _f.read()
            self.add_ask(f"大纲:{outline}")
        with open(r"D:\Seed\firm\agent\navel\输出物\世界观.txt", mode="r", encoding="utf-8") as f:
            world = f.read()
            self.add_ask(f"世界观:{world}")
        text = self.send().text
        result = json.loads(text)["choices"][0]["message"]["content"]
        with open(rf"D:\Seed\firm\agent\navel\输出物\角色卡\场景.json", mode="w", encoding="utf-8") as f:
            json.dump(json.loads(result), f, indent=2, ensure_ascii=False)
        return result


if __name__ == "__main__":
    Chapter().run_()
