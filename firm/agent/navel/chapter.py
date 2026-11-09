from agent.navel.base import Base_navel
from agent.navel.tool.get_msg import get_scene_sipy, get_main_role


class Chapter(Base_navel):

    def __init__(self):
        super().__init__()
        self.chapter = 0
        self.template = r"D:\Seed\firm\agent\navel\template\章节.txt"

    def key(self):
        msg = str(self._open.chapter(self.chapter_number()-1)) if self.chapter > 0 else "null"
        key = {"主要角色池": str(list(get_main_role().keys())),
               "场景池": str(get_scene_sipy()),
               "章节骨架": str(self._open.even.get("已发生事件")[self.chapter_number()]),
               "上一章内容": msg }
        return key

    def chapter_number(self, number: int = None, clean: bool = False):
        if isinstance(number, int) and number is not None:
            if number < 0 or number > len(self._open.even.get("已发生事件")):
                raise "没有该事件"
            self.chapter = number
        if clean is True:
            self.chapter = 0
        return self.chapter

    def write_(self):
        self._open.chapter(number=self.chapter_number(), content=self.auto_send())
        return self


if __name__ == "__main__":
    a = Chapter().auto_template().send_message
    print(a)
