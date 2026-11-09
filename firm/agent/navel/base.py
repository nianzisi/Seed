from agent.message import Message_Control
from agent.send import Send
from agent.tools.var import var

from agent.navel.tool import llm_tool
from agent.navel.tool.open import Open_path


class Base_navel(Send):
    template: str = None

    def __init__(self, _Message: Message_Control = None, category: str = "navel"):
        super().__init__(_Message=_Message or Message_Control(), category=category)
        self._open = Open_path()

    def key(self) -> dict:
        raise NotImplementedError("子类必须实现 key 方法")

    def auto_template(self):
        self.add_ask(var(path=self.template, key=self.key()))
        return self

    def auto_send(self) -> str:
        self.auto_template()
        return self.send()

