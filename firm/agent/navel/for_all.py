import json
import os.path
import traceback

from agent.navel.chapter import Chapter
from agent.navel.Initial_character import Just_role
from agent.navel.mini_outline import Mini_outline_creat
from agent.navel.outline import Outline_creat
from agent.navel.review import Review_creat
from agent.navel.scene import Scene
from agent.navel.tool.get_msg import get_outline, get_advise, get_main_even
from agent.navel.world_background import World_creat


class Run:

    def __init__(self):
        self.times = None
        self.number = 1
        self._world = World_creat()
        self._roles = Just_role()
        self._outline = Outline_creat()
        self._scene = Scene()
        self._review = Review_creat()
        self._evens = Mini_outline_creat()
        self._chapter = Chapter()

    def world(self):
        self._world.write_()
        return self._world

    def roles(self):
        self._roles.write_()
        return self._roles

    def outline(self):
        self._outline.write_()
        return self._outline

    def scenes(self):
        self._scene.write_()
        return self._scene

    def review(self):
        self._review.write_()
        return self._review

    def evens(self):
        self._evens.write_()
        return self._evens

    def chapter(self):
        self._chapter.write_()
        return self._chapter

    def run(self):
        self.world()
        self.roles()
        self.outline()
        self.scenes()
        for i in get_outline():
            self.times = 0
            self._evens.chapter = i
            self._evens.auto_template()
            even = self._evens.send()
            self._review.set_key(even=even, outline=json.dumps(i))
            self._review.write_()
            self.for_review(number=self.number, even=even, outline=json.dumps(i))
            main_even = get_main_even()
            for _ in main_even[self._chapter.chapter:]:
                self.chapter()
                self._chapter.chapter += 1

    def for_review(self, number: int, even, outline, advise: dict = None, re_even: bool = False,
                   re_outline: bool = False):
        if advise is None:
            advise = get_advise()
        if advise[0] == "细化事件重写" and self.times <= number:
            self._evens.add_ask(
                f"重写要求【{advise[1]}】仅需要重写该事件以及之后的事件，保持json输出格式，不要任何前言、解释、markdown标记、注释")
            re_write = self._evens.send()
            self._review.add_ask(
                f"重写内容【{re_write}】，你需要按照最初的要求再次审评，保持json输出格式，不要任何前言、解释、markdown标记、注释")
            re_advise = self._review.send()
            self._review.write_(re_advise)
            self.times += 1
            return self.for_review(number=number,
                                   even=re_write,
                                   outline=outline,
                                   re_even=True)
        elif advise[0] == "大事件重写" and self.times <= number:
            self._outline.add_ask(
                f"重写要求【{advise[1]}】仅需要重写该事件以及之后的事件，保持json输出格式，不要任何前言、解释、markdown标记、注释")
            re_write = self._outline.send()
            self._review.add_ask(
                f"大纲重写内容的【{re_write}】，你需要按照最初的要求再次审评，保持json输出格式，不要任何前言、解释、markdown标记、注释")
            re_advise = self._review.send()
            self._review.write_(re_advise)
            self.times += 1
            return self.for_review(number=number,
                                   even=even,
                                   outline=re_write,
                                   re_outline=True)
        else:
            if re_even:
                self._evens.write_(even)
            elif re_outline:
                self._outline.write_(outline)
                self._scene.add_ask(
                    f"根据新事件【{outline}】生产新场景，你需要按照最初的要求再次审评，保持json输出格式，不要任何前言、解释、markdown标记、注释")
                scene = self._scene.send()
                self._scene.write_(scene)
            self._scene.clean_message()
            return even


class Save(Run):
    """
    保存基础信息：世界观|大纲|初始角色|初始场景是否被创建。
    保存进度: 第几个事件，第几个章节
    """
    World_background = False
    Mian_roles = False

    Save_outline = 0
    Save_scene = 0

    Save_evens = 0
    Save_chapter = 0

    def save_world(self):
        if self.World_background:
            return None
        else:
            self.World_background = True
            print("正在生产世界观 ")
            self.world()
            return None

    def save_mian_roles(self):
        if self.Mian_roles:
            return None
        else:
            if not self.World_background:
                self.save_world()
            self.Mian_roles = True
            print("正在生产主要角色 ")
            self.roles()
            return None

    def save_outline(self):
        if self.Save_outline != 0:
            return None
        else:
            if not self.Mian_roles:
                self.save_mian_roles()
            self.Save_outline = 1
            print("正在生产初始大纲")
            self.outline()
            return None

    def save_scene(self):
        if self.Save_scene != 0:
            return None
        else:
            self.Save_scene = 1
            print("正在生产初始场景")
            self.scenes()
            return None

    def save_evens(self):
        i = get_outline()[self.Save_evens]
        self._evens.chapter = i
        self._evens.auto_template()
        even = self._evens.send()
        self._review.set_key(even=even, outline=json.dumps(i))
        self._review.write_()
        self.for_review(number=self.number, even=even, outline=json.dumps(i))
        self.Save_evens += 1

    def save_chapter(self):
        self._chapter.chapter = self.Save_chapter
        self.chapter()
        self.Save_chapter += 1

    def write_save_file(self):
        with open(r"D:\Seed\firm\agent\navel\输出物.json", mode="w", encoding="utf-8") as f:
            save_data = {
                "World_background": self.World_background,
                "Mian_roles": self.Mian_roles,
                "Save_outline": self.Save_outline,
                "Save_scene": self.Save_scene,
                "Save_evens": self.Save_evens,
                "Save_chapter": self.Save_chapter
            }
            json.dump(save_data, f, indent=2, ensure_ascii=False)

    def read_save_file(self):
        if os.path.isfile(r"D:\Seed\firm\agent\navel\输出物.json"):
            with open(r"D:\Seed\firm\agent\navel\输出物.json", mode="r", encoding="utf-8") as f:
                save_data: dict = json.loads(f.read().strip())
        else:
            save_data = {}
        self.World_background = save_data.get("World_background", False)
        self.Mian_roles = save_data.get("Mian_roles", False)
        self.Save_outline = save_data.get("Save_outline", 0)
        self.Save_scene = save_data.get("Save_scene", 0)
        self.Save_evens = save_data.get("Save_evens", 0)
        self.Save_chapter = save_data.get("Save_chapter", 0)

    def run(self):
        try:
            self.read_save_file()
            self.scenes()

            while len(get_outline()) > self.Save_evens:
                self.save_evens()
                while len(get_main_even()) > self.Save_chapter:
                    self.save_chapter()
        except Exception as e:
            print(e)
            traceback.print_exc()
        finally:
            self.write_save_file()


if __name__ == "__main__":
    pass
