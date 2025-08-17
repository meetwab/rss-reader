"""
Data models and enums for the RSS reader application.
"""

from enum import Enum, auto


class NavigationAction(Enum):
    """定义用户在视图之间导航的动作，以替代"魔术字符串"。"""
    BACK_TO_LIST = auto()
    BACK_TO_HOME = auto()
