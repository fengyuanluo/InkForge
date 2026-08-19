from __future__ import annotations

from typing import TypeAlias

from app.novel_research.adapters.fanqie import FanqieAdapter
from app.novel_research.adapters.jjwxc import JjwxcAdapter
from app.novel_research.adapters.qidian import QidianAdapter
from app.novel_research.adapters.zongheng import ZonghengAdapter
from app.novel_research.common import Adapter

AdapterType: TypeAlias = type[Adapter]

ADAPTERS: dict[str, AdapterType] = {
    "qidian": QidianAdapter,
    "fanqie": FanqieAdapter,
    "jjwxc": JjwxcAdapter,
    "zongheng": ZonghengAdapter,
}

__all__ = ["ADAPTERS", "AdapterType"]
