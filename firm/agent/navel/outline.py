from agent.navel.base import Base_navel

from agent.navel.tool.get_msg import get_outline


class Outline_creat(Base_navel):

    def __init__(self):
        super().__init__()
        self.template = r"D:\Seed\firm\agent\navel\template\大纲.txt"

    def key(self) -> dict:
        key = {"世界观": self._open.world_background, "角色卡片": self._open.main_role}
        return key

    def write_(self, outline=None):
        if outline is None:
            outline = self.auto_send()
        self._open.write_outline(outline, Merge=True)
        return self


if __name__ == "__main__":
    A = Outline_creat().auto_template().send_message
    print(A)
