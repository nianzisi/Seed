import json
import os


class Open_path:
    """
    文件读写管理
    """
    is_exist = None
    _world_background = None
    _main_role = None
    _outline = None
    _scene = None
    _just_role = None
    _even = None
    _advice = None

    _BASE = r"D:\Seed\firm\agent\navel\输出物"
    _P_WORLD = _BASE + r"\世界观.json"
    _P_MAIN = _BASE + r"\角色卡\初始角色.json"
    _P_OUTLINE = _BASE + r"\大纲.json"
    _P_SCENE = _BASE + r"\角色卡\场景.json"
    _P_JUST = _BASE + r"\角色卡\次要角色.json"
    _P_EVEN = _BASE + r"\小大纲.json"
    _P_CHAPTER = _BASE + r"\章节"
    _P_ADVICE = _BASE + r"\重写建议.json"

    def __new__(cls, *args, **kwargs):
        if cls.is_exist is None:
            cls.is_exist = super().__new__(cls)
        return cls.is_exist

    @staticmethod
    def _read_json(path) -> dict:
        """
        读取内容
        :param path: 地址
        :return: 不存在和为空时返回 {}
        """
        if not os.path.isfile(path):
            return {}
        with open(path, mode="r", encoding="utf-8") as f:
            text = f.read().strip()
        return json.loads(text) if text else {}

    @staticmethod
    def _write_json(path, data) -> None:
        """
        写
        :param path: 地址
        :param data: 内容
        :return: None
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, mode="w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def as_text(obj) -> str:
        return json.dumps(obj, ensure_ascii=False, indent=2)

    @property
    def world_background(self) -> dict:
        """
        读世界观
        :return: dict
        """
        if self._world_background is None:
            self._world_background = self._read_json(self._P_WORLD)
        return self._world_background

    @property
    def main_role(self) -> dict:
        """
        读主要角色，会将even中的状态一起捕获
        :return: dict
        """
        if self._main_role is None:
            base = self._read_json(self._P_MAIN).get("主要角色", [])
            state = self._latest_state("主要角色")
            _list = [{**dna, **state.get(dna.get("姓名"), {})} for dna in base]
            self._main_role = {"主要角色": _list} if _list or base else {"主要角色": []}

        return self._main_role

    def _latest_state(self, role: str) -> dict:
        """
        捕获even的角色状态
        :param role: 哪一类角色
        :return: dict
        """
        state = {}
        for ev in self.even.get("已发生事件", []):
            people = ev.get("人物变化", {})
            for p in people.get(role, []):
                name = p.get("姓名")
                if name:
                    state[name] = p  # 后发生的覆盖先前的
        return state

    @property
    def outline(self) -> dict:
        if self._outline is None:
            self._outline = self._read_json(self._P_OUTLINE)
        return self._outline

    @property
    def scene(self) -> dict:
        if self._scene is None:
            self._scene = self._read_json(self._P_SCENE)
        return self._scene

    @property
    def just_role(self) -> dict:
        """
        读次要角色，会将even中的状态一起捕获
        :return: dict
        """
        if self._just_role is None:
            base = self._read_json(self._P_JUST).get("次要角色", [])
            state = self._latest_state("次要角色")
            _list = [{**dna, **state.get(dna.get("姓名"), {})} for dna in base]
            self._just_role = {"次要角色": _list} if _list or base else {"次要角色": []}
        return self._just_role

    @property
    def even(self) -> dict:
        if self._even is None:
            self._even = self._read_json(self._P_EVEN)
        return self._even

    @property
    def advice(self) -> dict:
        if self._advice is None:
            self._advice = self._read_json(self._P_ADVICE)
        return self._advice

    def chapter(self, number: int, content=None):
        """
        读取和写入，content默认读
        :param number: 第几章
        :param content: 写入内容
        :return: 读：读取内容 | 写：self
        """
        path = rf"{self._P_CHAPTER}\第{number}章.txt"
        if content is None:
            if not os.path.isfile(path):
                return "null"
            with open(path, mode="r", encoding="utf-8") as f:
                return f.read()
        if not isinstance(content, str):
            raise ValueError("chapter content 必须为 str")
        os.makedirs(self._P_CHAPTER, exist_ok=True)
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(content)
        return self

    def write_world_background(self, content):
        data = json.loads(content) if isinstance(content, str) else content
        self._write_json(self._P_WORLD, data)
        self._world_background = None
        return self

    def write_role(self, content, Merge: bool = False):
        data = json.loads(content) if isinstance(content, str) else content
        if not isinstance(data, dict):
            raise Exception("非dict格式的str（json）/非dict对象")
        who = list(data.keys())[0]
        if "主要" in who and isinstance(who, str):
            who = "主要"
            _p_path = self._P_MAIN
            self._main_role = None
        elif "次要" in who and isinstance(who, str):
            who = "次要"
            _p_path = self._P_JUST
            self._just_role = None
        else:
            raise Exception("未表明输入主要/次要角色")
        if Merge:
            old = {p.get("姓名"): p for p in self._read_json(self._P_MAIN).get(f"{who}角色", [])}
            new = {p.get("姓名"): p for p in data.get(f"{who}角色", [])}
            data = {f"{who}角色": list({**old, **new}.values())}
        self._write_json(_p_path, data)
        return self

    def write_mini_outline(self, content, Merge: bool = False):
        data = json.loads(content) if isinstance(content, str) else content
        if Merge:
            old = self.even.get("已发生事件", [])
            new = data.get("已发生事件", [])
            data = {"已发生事件": old + new}
        self._write_json(self._P_EVEN, data)
        self._even = None
        self._main_role = None
        self._just_role = None
        return self

    def write_scene(self, content, Merge: bool = False):
        data = json.loads(content) if isinstance(content, str) else content
        if Merge:
            old = {_.get("id"): _ for _ in self.scene.get("场景", [])}
            new = {_.get("id"): _ for _ in data.get("场景", [])}
            data = {"场景": list({**old, **new}.values())}
        self._write_json(self._P_SCENE, data)
        self._scene = None
        return self

    def write_outline(self, content, Merge: bool = False):
        data = json.loads(content) if isinstance(content, str) else content
        if Merge:
            old = {_.get("id"): _ for _ in self.outline.get("事件", [])}
            new = {_.get("id"): _ for _ in data.get("事件", [])}
            data = {"事件": list({**old, **new}.values())}
        self._write_json(self._P_OUTLINE, data)
        self._outline = None
        return self

    def write_rewrite_advice(self, content):
        data = json.loads(content) if isinstance(content, str) else content
        self._write_json(self._P_ADVICE, data)
        self._advice = None
        return self

    def invalidate(self):
        self._world_background = None
        self._main_role = None
        self._outline = None
        self._scene = None
        self._just_role = None
        self._even = None
        self._advice = None
        return self


if __name__ == "__main__":
    print(Open_path().main_role)
