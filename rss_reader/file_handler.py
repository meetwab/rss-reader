"""
File handling operations for JSON data persistence.
"""

import json
import os
from typing import Dict, List


class FileHandler:
    """文件操作处理器，负责 JSON 文件的读写操作"""
    
    @staticmethod
    def load_subscriptions(filename: str) -> Dict[str, str]:
        """
        从指定的 JSON 文件中加载订阅列表。

        Args:
            filename (str): 存储订阅信息的 JSON 文件名。

        Returns:
            Dict[str, str]: 一个字典，键是订阅标题，值是订阅链接。
                            如果文件不存在或文件内容损坏，则返回一个空字典。
        """
        if not os.path.exists(filename):
            return {}

        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print(f" 警告：无法解析 {filename} 或文件不存在，将返回空订阅列表。")
            return {}
    
    @staticmethod
    def save_subscriptions(filename: str, subscriptions: Dict[str, str]) -> bool:
        """
        将订阅列表保存到 JSON 文件

        Args:
            filename (str): 文件名
            subscriptions (Dict[str, str]): 订阅字典

        Returns:
            bool: 保存是否成功
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(subscriptions, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f" 保存文件时发生错误：{e}")
            return False
    
    @staticmethod
    def load_articles_history(filename: str) -> Dict[str, List[Dict]]:
        """
        从 articles_history.json 中加载订阅源的文章。

        Args:
            filename (str): 存储文章历史的 JSON 文件名。

        Returns:
            Dict[str, List[Dict]]: 一个字典，键是订阅 URL，值是文章列表。
        """
        if not os.path.exists(filename):
            return {}

        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print(f" 警告：无法解析 {filename} 或文件不存在，将返回空文章历史。")
            return {}
    
    @staticmethod
    def save_articles_history(filename: str, articles_history: Dict[str, List[Dict]]) -> bool:
        """
        把订阅源的文章保存到 articles_history.json 文件中。

        Args:
            filename (str): 文件名
            articles_history (Dict[str, List[Dict]]): 文章历史字典

        Returns:
            bool: 保存是否成功
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(articles_history, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f" 保存文章历史时发生错误：{e}")
            return False
