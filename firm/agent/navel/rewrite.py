import json
import os

from agent.message import Message_Control
from agent.send import Send
from agent.tools.var import var


class Rewrite(Send):

    def __init__(self, _Message: Message_Control = None, category: str = None):
        super().__init__(_Message=_Message or Message_Control(), category=category)

    def template(self, path: str = r"D:\Seed\firm\agent\navel\template\重写.txt", key=None):
        self.add_system(var(path, key))

    def rewrite(self, style: str, prose: str) -> str:
        self.clean_message()
        self.template(key={"风格": style})
        self.add_ask(prose)
        text = self.send().text
        return json.loads(text)["choices"][0]["message"]["content"]

    def run_(self, style_path: str, src_dir: str, out_dir: str) -> str:
        with open(style_path, mode="r", encoding="utf-8") as f:
            style = f.read()
        os.makedirs(out_dir, exist_ok=True)
        for name in sorted(os.listdir(src_dir)):
            if not name.endswith(".txt"):
                continue
            with open(os.path.join(src_dir, name), mode="r", encoding="utf-8") as f:
                raw = f.read()
            prose, sep, state = raw.partition("&:-=标准分隔符号=-:&")
            rewritten = self.rewrite(style, prose.strip()).strip()
            with open(os.path.join(out_dir, name), mode="w", encoding="utf-8") as f:
                f.write(rewritten)
        return out_dir


if __name__ == "__main__":
    Rewrite().run_(
        r"D:\Seed\firm\agent\navel\输出物\设定\风格.txt",
        r"D:\Seed\firm\agent\navel\输出物\章节",
        r"D:\Seed\firm\agent\navel\输出物\章节_重写",
    )
