from agent.navel.base import Base_navel
from agent.navel.tool.open import Open_path


class Just_role(Base_navel):

    def __init__(self):
        super().__init__()
        self.template = r"D:\Seed\firm\agent\navel\template\角色卡片.txt"

    def key(self) -> dict:
        key = {"世界观": Open_path().world_background}
        return key

    def write_(self):
        self._open.write_role(self.auto_send())
        return self


if __name__ == "__main__":
    A = Just_role().auto_template().send_message
    print(A)
