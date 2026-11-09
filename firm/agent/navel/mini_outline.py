from agent.navel.base import Base_navel
from agent.navel.tool.get_msg import get_scene_sipy, get_main_role, get_just_role, get_outline, get_main_even


class Mini_outline_creat(Base_navel):

    def __init__(self):
        super().__init__()
        self.chapter = 0
        self.template = r"D:\Seed\firm\agent\navel\template\小大纲.txt"

    def key(self):
        key = {"世界观": self._open.world_background,
               "主要角色池": str(list(get_main_role().keys())),
               "次要角色池": str(list(get_just_role().keys())),
               "场景池": str(get_scene_sipy()),
               "事件": get_outline()[self.chapter] if isinstance(self.chapter, int) else self.chapter,
               "已发生事件": str(get_main_even())}
        return key

    def write_(self, result=None):
        if result is None:
            result = self.auto_send()
        self._open.write_mini_outline(result, Merge=True)
        return self


if __name__ == "__main__":
    a = Mini_outline_creat()
    a.auto_template()
    print(a.send_message)
