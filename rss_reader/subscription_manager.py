"""
Subscription management functionality.
"""

from typing import Dict, Optional, Tuple
from rich.console import Console
from rich.panel import Panel

from .file_handler import FileHandler
from .article_manager import ArticleManager
from .rss_parser import RssParser


class SubscriptionManager:
    """订阅管理器，负责订阅的增删改查"""
    
    def __init__(self, article_manager: ArticleManager, ai_summarizer=None, filename: str = "subscriptions.json"):
        self.filename = filename
        self.file_handler = FileHandler()
        # 使用传入的AI摘要器创建RssParser，避免重复初始化
        self.rss_parser = RssParser(article_manager=article_manager, ai_summarizer=ai_summarizer)
        self.console = Console()
    
    def add_subscription(self, url: str) -> bool:
        """
        1. 添加新的 RSS 订阅源；
        2. 保存订阅信息到 subscriptions.json 文件。

        Args:
            url (str): RSS 链接

        Returns:
            bool: 是否添加成功
        """
        title, success = self.rss_parser.fetch_feed_info(url)
        if not success or not title:
            return False
        
        # 加载现有订阅
        subscriptions = self.file_handler.load_subscriptions(self.filename)
        
        # 检查是否已存在相同的 URL（避免重复订阅）
        if url in subscriptions.values():
            existing_name = next(name for name, existing_url in subscriptions.items() if existing_url == url)
            warning_panel = Panel(
                f"[yellow]⚠️  订阅已存在：'{existing_name}' [/yellow]",
                style="yellow",
                border_style="yellow"
            )
            self.console.print(warning_panel)
            return False
        
        # 检查标题重名，如果重名则添加序号
        original_title = title
        counter = 1
        while title in subscriptions:
            title = f"{original_title} ({counter})"
            counter += 1
        
        # 添加新订阅
        subscriptions[title] = url
        
        # 保存订阅到文件
        if self.file_handler.save_subscriptions(self.filename, subscriptions):
            success_panel = Panel(
                f"[bold green]🎉 订阅 '{title}' 已成功保存！[/bold green]",
                style="green",
                border_style="green"
            )
            self.console.print(success_panel)
            return True
        return False
    
    def get_subscription_info(self, number: int) -> Tuple[Optional[str], Optional[str]]:
        """
        获取指定序号的订阅信息，用于删除前的确认显示

        Args:
            number (int): 订阅序号

        Returns:
            Tuple[Optional[str], Optional[str]]: (订阅名称，订阅 URL)，如果序号无效返回 (None, None)
        """
        subscriptions = self.file_handler.load_subscriptions(self.filename)
        
        if not subscriptions or number < 1 or number > len(subscriptions):
            return None, None
        
        subscription_items = list(subscriptions.items())
        return subscription_items[number - 1]

    def delete_subscription(self, number: int) -> bool:
        """
        1. 通过指定序号 (number)，删除对应的 RSS 订阅源；
        2. 从 subscriptions.json 文件中删除订阅信息。

        Args:
            number (int): 订阅序号

        Returns:
            bool: 是否删除成功
        """
        # 从 subscriptions.json 文件中加载订阅列表
        subscriptions = self.file_handler.load_subscriptions(self.filename)
        
        if not subscriptions:
            warning_panel = Panel(
                "[yellow]⚠️  订阅列表为空，无法删除 [/yellow]",
                style="yellow",
                border_style="yellow"
            )
            self.console.print(warning_panel)
            return False
        
        # 检查序号是否有效
        if number < 1 or number > len(subscriptions):
            print(f" 无效的订阅序号：{number}。请提供有效的序号。")
            return False
        
        # 获取订阅列表，确保与显示时的顺序一致
        subscription_items = list(subscriptions.items())
        subscription_name, subscription_url = subscription_items[number - 1]
        
        # 从字典中删除订阅
        del subscriptions[subscription_name]
        
        # 保存更新后的订阅列表
        if self.file_handler.save_subscriptions(self.filename, subscriptions):
            success_panel = Panel(
                f"[bold green]🎉 订阅 '{subscription_name}' 已成功删除！[/bold green]",
                style="green",
                border_style="green"
            )
            self.console.print(success_panel)
            return True
        return False
    
    def get_subscriptions(self) -> Dict[str, str]:
        """
        1. 从 subscriptions.json 文件中加载 RSS 订阅源；
        """
        return self.file_handler.load_subscriptions(self.filename)
    
    def get_subscription_by_index(self, index: int) -> Tuple[Optional[str], Optional[str]]:
        """
        1. 从订阅列表中获取指定索引的订阅信息。

        Args:
            index (int): 订阅索引（从 1 开始）

        Returns:
            Tuple[Optional[str], Optional[str]]: (订阅名称，订阅 URL)
        """
        # 获取所有订阅
        subscriptions = self.get_subscriptions()
        # 检查索引是否有效
        if not subscriptions or index < 1 or index > len(subscriptions):
            return None, None
        # 获取订阅名称和 URL
        subscription_items = list(subscriptions.items())
        return subscription_items[index - 1]
