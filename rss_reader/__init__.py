"""
RSS Reader Package

A modular RSS reader application with subscription management,
article caching, and a rich console interface.
"""

__version__ = "1.0.0"
__author__ = "RSS Reader Team"

from .models import NavigationAction
from .file_handler import FileHandler
from .article_manager import ArticleManager
from .rss_parser import RssParser
from .subscription_manager import SubscriptionManager
from .ui import UserInterface
from .main import RssApp

__all__ = [
    "NavigationAction",
    "FileHandler", 
    "ArticleManager",
    "RssParser",
    "SubscriptionManager", 
    "UserInterface",
    "RssApp"
]
