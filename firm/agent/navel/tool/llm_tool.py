from agent.tools.get_sql import tool

from agent.navel.tool.get_msg import get_sence, get_main_role, get_just_role


@tool("navel")
def sence_sipy(name: str | list):
    """
    获取场景的详细信息
    :param name: 场景名称，接受str类型和list[str]类型
    :return: 场景的详细状态
    """
    role = get_sence()
    keys = role.keys()
    if isinstance(name, str):
        if name not in list(keys):
            return False, "不存在该场景"
        return role.get(name)
    elif isinstance(name, list):
        result = []
        for _ in name:
            if not isinstance(_, str):
                result.append({False, f"列表中{_}不是str的类型"})
                continue
            if _ not in list(keys):
                result.append({False, f"列表中{_}是不存在的场景"})
                continue
            result.append(role.get(_))
        return result
    else:
        return False, "不支持的类型"


@tool("navel")
def main_role_sipy(name: str | list):
    """
    获取主要角色的详细信息
    :param name: 主要角色名称，接受str类型和list[str]类型
    :return: 主要角色的详细状态 str|list
    """
    role = get_main_role()
    name_keys = role.keys()

    def del_some_main_role(msg: list[dict] | dict):
        if isinstance(msg, dict):
            msg = [msg]
        for _ in msg:
            del _["别名"], _["身份"], _["弱点"], _["样貌"], _["出场简介"]
        return msg

    if isinstance(name, str):
        if name not in name_keys:
            return False, "不存在该主要角色"
        return del_some_main_role(role.get(name))
    elif isinstance(name, list):
        result = []
        for _ in name:
            if not isinstance(_, str):
                result.append({False, f"列表中{_}不是str的类型"})
                continue
            if _ not in name_keys:
                result.append({False, f"列表中{_}是不存在的主要角色"})
                continue
            result.append(del_some_main_role(role.get(_)))
        return result
    else:
        return False, "不支持的类型"


@tool("navel")
def minor_role_sipy(name: str | list):
    """
    获取次要角色的详细信息
    :param name: 次要角色名称，接受str类型和list[str]类型
    :return: 次要角色详细信息 str|list
    """
    role = get_just_role()
    name_keys = role.keys()
    if isinstance(name, str):
        if name not in name_keys:
            return False, "不存在该次要角色"
        return role.get(name)
    elif isinstance(name, list):
        result = []
        for _ in name:
            if not isinstance(_, str):
                result.append({False, f"列表中{_}不是str类型"})
                continue
            if _ not in name_keys:
                result.append({False, f"列表中{_}是不存在的次要角色"})
                continue
            result.append(role.get(_))
        return result
    else:
        return False, "不支持的类型"


@tool("navel")
def worlds_explain(worlds: str | list) -> dict:
    """
    获取key字段的详细解释
    :param worlds: 单个key名或者列表key名
    :return: 返回字典。详细解释
    """
    pass


@tool("navel.ask")
def ask_user(msg: str):
    """
    向用户提问
    :param msg: 提问内容
    :return: 返回用户的回答
    """
    print(f"询问: {msg}")
    return input()


if __name__ == "__main__":
    print(minor_role_sipy(["沈渠", "北疆军屯灌渠"]))
