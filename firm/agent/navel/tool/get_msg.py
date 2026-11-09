from agent.navel.tool.open import Open_path


def get_main_role() -> dict:
    return {name.get("姓名"): name for name in Open_path().main_role.get("主要角色")}


def get_sence() -> dict:
    role_values = Open_path().scene.values()
    result = {}
    for _value in role_values:
        for __ in _value:
            result[__["地名"]] = __
    return result


def get_just_role() -> dict:
    read = Open_path().just_role
    if isinstance(read, dict) and not read:
        return {"次要角色": "null"}
    role_values = read.values()
    result = {}
    for _value in role_values:
        for __ in _value:
            result[__["姓名"]] = __
    return result


def get_outline() -> list[dict]:
    return Open_path().outline.get("事件")


def get_scene_sipy() -> list[dict]:
    scene = []
    for _ in get_sence().values():
        scene.append({"地名": _["地名"],
                      "地形": _["地形"]})
    return scene


def get_main_even():
    even: list[dict] = Open_path().even.get("已发生事件")
    return even


def get_advise():
    advise: dict = Open_path().advice
    if advise.get("细化事件重写").get("是否重写") == "是" and advise.get("大事件重写").get("是否重写") != "是":
        return "细化事件重写", advise.get("细化事件重写")
    elif advise.get("大事件重写").get("是否重写") == "是" and advise.get("细化事件重写").get("是否重写") != "是":
        return "大事件重写", advise.get("大事件重写")
    else:
        return "无 or 冲突"

if __name__ == "__main__":
    print(get_main_role())
