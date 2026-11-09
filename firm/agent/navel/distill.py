import json

from agent.message import Message_Control
from agent.send import Send


class Distill(Send):

    def __init__(self, _Message: Message_Control = None, category: str = None):
        super().__init__(_Message=_Message or Message_Control(), category=category)

    def run_(self, a_path: str, b_path: str, c_path: str) -> str:
        with open(a_path, mode="r", encoding="utf-8") as f:
            content = f.read()
        with open(b_path, mode="r", encoding="utf-8") as f:
            prompt = f.read()
        self.add_system(prompt)
        self.add_ask(content)
        result = self.send()
        with open(c_path, mode="w", encoding="utf-8") as f:
            f.write(result)
        return c_path


if __name__ == "__main__":
    Distill().run_(
        r"D:\Seed\firm\agent\navel\资料\待蒸馏.txt",
        r"D:\Seed\firm\agent\navel\template\蒸馏.txt",
        r"D:\Seed\firm\agent\navel\输出物\设定\风格.txt",
    )
