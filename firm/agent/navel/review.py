from agent.navel.base import Base_navel


class Review_creat(Base_navel):

    def __init__(self):
        super().__init__()
        self.template = r"D:\Seed\firm\agent\navel\template\事件审核.txt"
        self._key = None

    def set_key(self, even=None, outline=None):
        if outline is None:
            outline = self._open.outline
        if even is None:
            even = self._open.even
        self._key = {"世界观": self._open.world_background, "细化事件": even, "大事件": outline}
        return self

    def key(self) -> dict:
        if not self._key:
            self._key = {"世界观": self._open.world_background, "细化事件": self._open.even, "大事件":  self._open.outline}
        return self._key

    def write_(self, result=None):
        if result is None:
            result = self.auto_send()
        self._open.write_rewrite_advice(result)
        return self


if __name__ == "__main__":
    A = Review_creat().auto_template().send_message
    print(A)
