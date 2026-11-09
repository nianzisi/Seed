import json
from pathlib import Path
import pytest
from agent.navel.for_all import Run
from agent.navel.tool.open import Open_path


class FakeResponse:
    def __init__(self, content: str):
        self.text = json.dumps(
            {"choices": [{"message": {"role": "assistant", "content": content}}]},
            ensure_ascii=False,
        )


def _route(payload: dict, script: dict) -> str:
    text = " ".join(str(m.get("content", "")) for m in payload["messages"])
    if "世界观设计师" in text:
        return script["world"]
    if "角色档案设计师" in text:
        return script["roles"]
    if "大纲的设计师" in text:
        return script["outline"]
    if "生成大纲中出现的场景" in text:
        return script["scene"]
    if "细节事件的设计师" in text:
        return script["mini"]
    if "一致性审核员" in text:
        return script["review_pass"] if "重写内容" in text else script["review_retry"]
    if "小说编辑" in text:
        return script["chapter"]
    raise AssertionError("未识别的模板")


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setattr(Open_path, "_BASE", str(tmp_path))
    monkeypatch.setattr(Open_path, "_P_WORLD", str(tmp_path / "世界观.json"))
    monkeypatch.setattr(Open_path, "_P_MAIN", str(tmp_path / "角色卡" / "初始角色.json"))
    monkeypatch.setattr(Open_path, "_P_OUTLINE", str(tmp_path / "大纲.json"))
    monkeypatch.setattr(Open_path, "_P_SCENE", str(tmp_path / "角色卡" / "场景.json"))
    monkeypatch.setattr(Open_path, "_P_JUST", str(tmp_path / "角色卡" / "次要角色.json"))
    monkeypatch.setattr(Open_path, "_P_EVEN", str(tmp_path / "小大纲.json"))
    monkeypatch.setattr(Open_path, "_P_CHAPTER", str(tmp_path / "章节"))
    monkeypatch.setattr(Open_path, "_P_ADVICE", str(tmp_path / "重写建议.json"))
    Open_path().invalidate()
    yield tmp_path
    Open_path().invalidate()


def test_for_all_smoke(env, monkeypatch):
    script = {
        "world": json.dumps({"地理": {"世界形态": "测试大陆"}, "硬约束": {}}, ensure_ascii=False),
        "roles": json.dumps({"主要角色": [{"姓名": "甲", "核心目标": "g", "价值观": "v"}]}, ensure_ascii=False),
        "outline": json.dumps({"事件": [{"id": "e1", "名称": "事件一", "事件发动的目的": "p",
                                         "事件类型": "普通事件", "事件影响": "r", "参与角色": "甲"}],
                               "主线": {"最终目的": "m"}}, ensure_ascii=False),
        "scene": json.dumps({"场景": [{"id": "s1", "地名": "测试地", "地形": "平原"}]}, ensure_ascii=False),
        "mini": json.dumps({"已发生事件": [{"id": "d1", "名称": "细节一", "父类": "事件一",
                                            "阶段": "开端", "角色": "甲", "发展": "发生", "伏笔": "",
                                            "人物变化": {"主要角色": [{"姓名": "甲", "当前心理状态": "平静"}],
                                                         "次要角色": []}},
                                           {"id": "d2", "名称": "细节2", "父类": "事件2",
                                            "阶段": "开端", "角色": "甲", "发展": "发生", "伏笔": "",
                                            "人物变化": {"主要角色": [{"姓名": "甲", "当前心理状态": "平静"}],
                                                         "次要角色": []}}
                                           ]}, ensure_ascii=False),
        "review_pass": json.dumps(
            {"细化事件重写": {"是否重写": "否", "理由": "无", "修改建议": "无", "保留建议": "无", "其余": ""},
             "大事件重写": {"是否重写": "否", "理由": "无", "修改建议": "无", "保留建议": "无", "其余": ""}},
            ensure_ascii=False),
        "review_retry": json.dumps(
            {"细化事件重写": {"是否重写": "是", "理由": "逻辑冲突", "修改建议": "无", "保留建议": "无", "其余": ""},
             "大事件重写": {"是否重写": "否", "理由": "无", "修改建议": "无", "保留建议": "无", "其余": ""}},
            ensure_ascii=False),
        "chapter": "测试正文",
    }

    def fake_request(**kwargs):
        return FakeResponse(_route(kwargs["json"], script))

    monkeypatch.setattr("agent.send.requests.request", fake_request)
    monkeypatch.setattr("builtins.input", lambda *_: "种子")

    Run().run()

    op = Open_path()
    assert op.world_background["地理"]["世界形态"] == "测试大陆"
    assert op.main_role["主要角色"][0]["姓名"] == "甲"
    assert op.outline["事件"][0]["名称"] == "事件一"
    assert op.scene["场景"][0]["地名"] == "测试地"
    assert len(op.even["已发生事件"]) == 2
    assert (env / "章节" / "第1章.txt").read_text(encoding="utf-8") == "测试正文"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
