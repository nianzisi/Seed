import pytest
from agent.navel.base import Base_navel

def test_auto_send(monkeypatch):
    monkeypatch.setattr(Base_navel, "add_ask", "1")
    assert isinstance(Base_navel)