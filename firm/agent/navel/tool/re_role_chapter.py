import re


def re_role_chapter(msg: str):
    read = re.search(r"&:-=标准分隔符号=-:&([\s\S]*)", msg)
    state = re.findall(r"-(.+)", read.group(1))
    print(state)
    return list_yield(state)


def list_yield(state: list, n=9):
    result = {}
    for _ in range(0, len(state), n):
        name = re.sub(r"角色名[:： ]", "", state[_])
        new = {name: {
            "心理状态": re.match("心理状态[:：](.+)", state[_ + 1].strip()).group(1),
            "身体状态": re.match("身体状态[:：](.+)", state[_ + 2].strip()).group(1),
            "当前物品": re.match("当前物品[:：](.+)", state[_ + 3].strip()).group(1),
            "物品状态": re.match("物品状态[:：](.+)", state[_ + 4].strip()).group(1),
            "新增技能": re.match("新增技能[:：](.+)", state[_ + 5].strip()).group(1),
            "新增物品": re.match("新增物品[:：](.+)", state[_ + 6].strip()).group(1),
            "与其他角色的关系": re.match("与其他角色的关系[:：](.+)", state[_ + 7].strip()).group(1),
            "当前事件是否击破该角色价值观": re.match("当前事件是否击破该角色价值观[:：](.+)",
                                                     state[_ + 8].strip()).group(1)
        }}
        result = result | new
    return result


if __name__ == "__main__":
    with open(r"D:\Seed\firm\agent\navel\输出物\章节\第1章.txt", mode="r", encoding="utf-8") as f:
        print(re_role_chapter(f.read()))
