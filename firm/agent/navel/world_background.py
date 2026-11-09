from agent.navel.base import Base_navel


class World_creat(Base_navel):
    """
    世界观生产
    """

    def __init__(self, category: str = "navel.ask"):
        super().__init__(category=category)
        self.template = r"D:\Seed\firm\agent\navel\template\世界背景生成.txt"

    def key(self):
        return None

    def write_(self):
        self.add_ask(input("输入世界观"))
        self._open.write_world_background(self.auto_send())
        return self


if __name__ == "__main__":
    print(World_creat().auto_template().write_().send_message)
