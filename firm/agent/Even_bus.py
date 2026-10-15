"""监听器"""


class EventBus:
    """事件广播类"""

    _instance = None  # 类变量，存唯一实例

    def __new__(cls):
        if cls._instance is None:  # 还没创建过
            cls._instance = super().__new__(cls)  # 创建
            cls._instance._listeners = {}  # 初始化
        return cls._instance  # 返回唯一实例

    def on(self, category: str, obj: object):
        if category not in self._listeners:
            self._listeners[category] = []

        if obj not in self._listeners[category]:
            self._listeners[category].append(obj)

    def emit(self, category: str, *args, **kwargs):
        if category in self._listeners:
            for obj in self._listeners[category]:
                obj(*args, **kwargs)


def event_on(category: str):
    """
    事件监听器注册装饰函数
    :param category: 注册名称
    :return: None
    """

    def event(func):
        EventBus().on(category=category, obj=func)

        return func
    return event


def event_emit(*, category: str, result_name: str, **data):
    """
    事件监听器的执行函数，接受任意赋值
    :param result_name: 结果名称
    :param category: 类型名称
    :return: func(*arges, **kwargs)
    """

    def event(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            kwargs[result_name] = result
            kwargs = kwargs | data
            EventBus().emit(category=category, *args, **kwargs)
            return result

        return wrapper

    return event
