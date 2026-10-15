import json
import re

from agent.message import Message_Control
from agent.send import Send
from agent.tools.get_sql import tool
from agent.tools.var import var
from agent.navel.tool.re_role_chapter import re_role_chapter as new_role_chapter


class Chapter(Send):

    def __init__(self, _Message: Message_Control = None, category: str = "navel"):
        super().__init__(_Message=_Message or Message_Control(), category=category)
        self.chapter = 0

        with open(r"D:\Seed\firm\agent\navel\输出物\角色卡\角色2.json", mode="r", encoding="utf-8") as f:
            self.role_pool: dict = json.load(f)
        with open(r"D:\Seed\firm\agent\navel\输出物\角色卡\场景.json", mode="r", encoding="utf-8") as f:
            self.scene_pool: dict = json.load(f)

        with open(r"D:\Seed\firm\agent\navel\输出物\大纲.txt", mode="r", encoding="utf-8") as _f:
            self.outline = _f.read()
            times = re.search(r"&:-=总章节=-:&(.+)", self.outline).group(1).strip()
            self.times = re.match(r"\d+", times).group(0)
        with open(r"D:\Seed\firm\agent\navel\输出物\世界观.txt", mode="r", encoding="utf-8") as _f:
            self.world_ground = _f.read()

    def re_role_chapter(self, msg: str):
        _role_chapter = new_role_chapter(msg)
        for _ in _role_chapter.keys():
            if _ in self.role_pool.keys():
                if _role_chapter[_]["当前事件是否击破该角色价值观"] != "False":
                    self.role_pool[_] = self.role_pool[_] | json.loads(_role_chapter[_]["当前事件是否击破该角色价值观"])
                self.role_pool[_] = _role_chapter[_] | self.role_pool[_]
        with open(r"D:\Seed\firm\agent\navel\输出物\角色卡\角色.json", mode="w", encoding="utf-8") as f:
            json.dump(self.role_pool, f, indent=2, ensure_ascii=False)

    def template(self, path: str = r"D:\Seed\firm\agent\navel\template\章节.txt", key=None):
        self.chapter += 1
        if key is None:
            key = {"字数": "800-1200",
                   "第几章": str(self.chapter),
                   "角色池": str(self.role_pool.keys()),
                   "场景池": str(self.scene_pool.keys())}
        self.add_system(var(path, key))

    def run_(self) -> str:
        self.template()
        self.add_ask(self.outline)
        self.add_ask(self.world_ground)
        text = self.send().text
        result = json.loads(text)["choices"][0]["message"]["content"]
        with open(rf"D:\Seed\firm\agent\navel\输出物\章节\第{self.chapter}章.txt", mode="w", encoding="utf-8") as f:
            f.write(result)
        self.re_role_chapter(result)
        self.clean_message()
        return text

    def while_run_(self, times: int = 3):
        for _ in range(min(times, int(self.times))):
            print(self.times)
            self.run_()


@tool("navel")
def character_pool(name: str):
    """
    角色状态池
    :param name: 角色名（真名-角色候选池中的名称），不接受绰号或者别名
    :return: 角色状态
    """
    with open(r"D:\Seed\firm\agent\navel\输出物\角色卡\角色.json", mode="r", encoding="utf-8") as f:
        chapter: dict = json.load(f)
    if name in chapter.keys():
        return chapter[name]
    else:
        return "False", "不存在该角色"


@tool("navel")
def scene(name: str):
    """
    场景池
    :param name: 场景名（真名-场景候选池中的名称），不接受绰号或者别名
    :return: 场景描述
    """
    with open(r"D:\Seed\firm\agent\navel\输出物\角色卡\场景.json", mode="r", encoding="utf-8") as f:
        chapter: dict = json.load(f)
    if name in chapter.keys():
        return chapter[name]
    else:
        return "False", "不存在该名称场景"


if __name__ == "__main__":
    Chapter().while_run_()
