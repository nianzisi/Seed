from agent.navel.base import Base_navel


class Scene(Base_navel):

    def __init__(self):
        super().__init__()
        self.template = r"D:\Seed\firm\agent\navel\template\场景.txt"

    def key(self):
        key = {"大纲": self._open.outline, "世界观": self._open.world_background}
        return key

    def write_(self, content: str = None):
        if content and isinstance(content, str):
            msg = content
        else:
            msg = self.auto_send()
        self._open.write_scene(msg, Merge=True)
        return self


if __name__ == "__main__":
    print(Scene().auto_template().send_message)
