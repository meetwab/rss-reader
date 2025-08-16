# -*- coding: utf-8 -*-
"""
这是一个简单的 RSS 订阅管理脚本。
主要功能包括：
- 添加新的 RSS 订阅源。
- 将订阅源信息（标题和链接）保存到本地的 JSON 文件中。
- 加载并显示所有已保存的订阅源。
- 通过命令行与用户交互，实现订阅的添加和查看。
"""
import json
import os
import html
import sys
import webbrowser
from datetime import datetime
from typing import Dict, List
import requests
import feedparser
import re
from enum import Enum, auto

class NavigationAction(Enum):
    """定义用户在视图之间导航的动作，以替代“魔术字符串”。"""
    BACK_TO_LIST = auto()
    BACK_TO_HOME = auto()

class RssManager:
    """
    RSS 管理器类，负责处理 RSS 订阅的添加、查看和管理。
    
    方法：
        save_subscription(link: str): 保存新的 RSS 订阅。
        load_subscriptions(filename: str) -> Dict[str, str]: 加载已有的订阅列表。
        view_subscriptions(): 查看所有订阅。
        view_single_subscription_articles(subscription_name: str, subscription_url: str): 查看单个订阅的文章。
    """

    def __init__(self):
        self.article_fetcher = ArticleFetcher()

    def save_subscription(self, link: str):
        """
        根据给定的链接，获取 RSS 源的标题并保存到订阅文件中。

        执行流程：

        1. 使用 requests 库请求订阅链接，设置 10 秒超时。
        2. 使用 feedparser 库解析返回的 XML 内容。
        3. 从解析后的数据中提取 RSS 源的标题，如果标题不存在，则使用默认名。
        4. 调用 load_subscriptions 函数加载本地已有的订阅。
        5. 将新的订阅（标题：链接）添加到数据中。
        6. 将更新后的数据写回 'subscriptions.json' 文件。

        Args:
            link (str): 用户输入的 RSS 订阅链接。
        """
        try:
            # 步骤 1: 发送 HTTP GET 请求获取订阅源的 XML 内容
            print(f"正在请求链接：{link}")
            response = requests.get(link, timeout=10)
            # 确保请求成功
            response.raise_for_status()

            # 步骤 2: 解析 RSS/Atom 源
            feed = feedparser.parse(response.content)
            
            # 检查 feed 是否格式良好。feed.bozo 为 1 表示格式有问题。
            if feed.bozo:
                # feed.bozo_exception 包含了解析错误的具体信息
                print(f"⚠️  警告：链接 {link} 可能不是一个有效的 RSS/Atom 源。错误：{feed.bozo_exception}")
                # 即使格式错误，我们仍然尝试获取标题并添加，但给出警告

            # 步骤 3: 获取 feed 的标题，如果解析失败或没有标题，则提供一个默认值
            title = feed.feed.get("title")
            if not title:
                print(f"❌ 无法从链接中获取标题，将使用默认名称。")
                title = f"未命名订阅_{datetime.now():%Y%m%d%H%M%S}"
            print(f"成功获取标题：{title}")

            # 步骤 4: 加载本地已有的订阅数据
            subscriptions = self.load_subscriptions("subscriptions.json")
            
            # 步骤 5: 将新的订阅信息（标题作为键，链接作为值）存入字典
            subscriptions[title] = link
            
            # 步骤 6: 将更新后的字典保存到 JSON 文件
            with open("subscriptions.json", "w", encoding="utf-8") as f:
                # indent=2 使 JSON 文件格式化，更易读
                # ensure_ascii=False 确保中文字符能被正确写入
                json.dump(subscriptions, f, ensure_ascii=False, indent=2)
            print(f"🎉 订阅 '{title}' 已成功保存！")

        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求错误：{e}")
        except Exception as e:
            print(f"❌ 处理订阅时发生未知错误：{e}")


    def load_subscriptions(self, filename: str) -> Dict[str, str]:
        """
        从指定的 JSON 文件中加载订阅列表。

        Args:
            filename (str): 存储订阅信息的 JSON 文件名。

        Returns:
            Dict[str, str]: 一个字典，键是订阅标题，值是订阅链接。
                            如果文件不存在或文件内容损坏，则返回一个空字典。
        """
        # 检查订阅文件是否存在，如果不存在，则返回一个空字典表示没有订阅
        if not os.path.exists(filename):
            return {}

        try:
            # 使用 'with' 语句安全地打开文件
            with open(filename, "r", encoding="utf-8") as f:
                # 从 JSON 文件中读取并解析数据
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # 如果文件为空、内容不是有效的 JSON 格式或文件不存在，则捕获异常
            # 返回一个空字典，防止程序崩溃
            print(f"⚠️ 警告：无法解析 {filename} 或文件不存在，将返回空订阅列表。")
            return {}


    def view_subscriptions(self):
        """
        查看所有订阅，用户可以选择进入某个订阅查看文章或返回首页
        """
        while True:
            # 从文件中加载所有订阅
            subscriptions = self.load_subscriptions("subscriptions.json")
            
            # 检查是否有订阅
            if not subscriptions:
                print("\n📪 您的订阅列表为空，请先添加订阅。")
                return

            # 格式化并打印订阅列表
            print("\n--- 📚 您已保存的订阅 ---")
            # 使用 enumerate 为每个订阅添加序号
            for i, (name, url) in enumerate(subscriptions.items(), 1):
                print(f"{i}. 名称：{name}")
                print(f"   链接：{url}")
            print("-------------------------")
            
            # 提供操作选项
            print("\n操作选项：")
            print(f"[1-{len(subscriptions)}] 进入对应订阅查看文章")
            print("[0] 返回首页")
            
            try:
                choice = input("\n请选择操作：").strip()
                
                if choice == "0":
                    return  # 返回首页
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(subscriptions):
                    # 获取用户选择的订阅
                    selected_name = list(subscriptions.keys())[choice_num - 1]
                    selected_url = subscriptions[selected_name]
                    
                    # 进入查看该订阅的文章
                    action = self.view_single_subscription_articles(selected_name, selected_url)
                    
                    # 如果用户选择返回首页，则退出当前循环
                    if action == NavigationAction.BACK_TO_HOME:
                        return
                else:
                    print("❌ 无效的选择，请输入正确的序号。")
                    
            except ValueError:
                print("❌ 请输入有效的数字序号。")
            except Exception as e:
                print(f"❌ 发生错误：{e}")


    def view_single_subscription_articles(self, subscription_name: str, subscription_url: str) -> NavigationAction:
        """
        查看单个订阅的最新文章，提供返回选项
        
        Args:
            subscription_name (str): 订阅名称
            subscription_url (str): 订阅链接
        """
        while True:
            print(f"\n--- 📰 {subscription_name} 的最新文章 ---")
            
            # 获取最新文章
            articles = self.article_fetcher.fetch_latest_articles(subscription_url)
            
            if not articles:
                print("❌ 未能获取到文章，可能是网络问题或链接失效。")
            else:
                # 显示文章
                self.article_fetcher.display_articles(articles)
            
            # 提供操作选项
            print("\n操作选项：")
            print("[r] 刷新文章列表")
            print("[b] 返回订阅列表")
            print("[0] 返回首页")
            
            choice = input("\n请选择操作：").strip().lower()
            
            if choice == "b":
                return NavigationAction.BACK_TO_LIST
            elif choice == "0":
                return NavigationAction.BACK_TO_HOME
            elif choice == "r":
                print("\n🔄 正在刷新...")
                continue  # 重新循环，刷新文章
            else:
                print("❌ 无效的选择，请重新输入。")

class ArticleFetcher:
    """
    文章获取器类，负责从指定的 RSS 源获取最新文章。
    
    方法：
        fetch_latest_articles(url: str, count: int = 3) -> List[str]: 获取指定 RSS 源的最新文章。
        remove_html_tags(text: str) -> str: 移除 HTML 标签，保留纯文本内容。
        display_articles(articles: List[str]): 格式化展示文章列表。
    """
    

    def fetch_latest_articles(self, url: str, count: int = 3) -> List[str]:
        """
        1. 获取指定 RSS 源的最新文章；
        2. 返回文章标题、链接和内容摘要等信息；
        3. 如果链接无效或没有文章，则返回空列表。

        Args:
            url (str): RSS 源的链接。
            count (int): 要获取的最新文章数量，默认为 3。
        Returns:
            List[str]: 文章信息列表（标题、链接、内容摘要等）。
        """
        try:
            # 发送请求获取 RSS 源内容
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 确保请求成功

            # 使用 feedparser 解析 RSS 源
            feed = feedparser.parse(response.content)

            # 检查是否有条目
            if not feed.entries:
                print(f"⚠️ 警告：链接 {url} 没有找到任何文章。")
                return []

            # 获取最新的 count 篇文章
            articles = []
            for entry in feed.entries[:count]:
                title = entry.get("title", "无标题")
                link = entry.get("link", "无链接")
                summary = entry.get("summary", "无摘要")
                
                # 清理 HTML 标签，获取纯文本内容
                clean_summary = self.remove_html_tags(summary)
                
                articles.append(f"标题：{title}\n链接：{link}\n摘要：{clean_summary}\n")

            return articles

        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求错误：{e}")
            return []
        except Exception as e:
            print(f"❌ 处理文章时发生未知错误：{e}")
            return []

    def remove_html_tags(self, text: str) -> str:
        """
        移除 HTML 标签，保留纯文本内容
        
        Args:
            text (str): 包含 HTML 标签的文本
            
        Returns:
            str: 清理后的纯文本
        """
        if not text:
            return text
        
        # 使用正则表达式移除 HTML 标签
        clean_text = re.sub(r'<[^>]+>', '', text)
        
        # 清理多余的空白字符和换行符
        clean_text = re.sub(r'\s+', ' ', clean_text)
        
        # 解码 HTML 实体（如 &lt; &gt; &amp; 等）
        clean_text = html.unescape(clean_text)
        
        return clean_text.strip()

    def display_articles(self, articles: List[str]):
        """
        1. 格式化展示文章列表；
        2. 处理内容截取（前 200 个字符）；
        3. 美观的输出格式；

        Args:
            articles (List[str]): 文章信息列表。
        """
        if not articles:
            print("没有找到相关文章。")
            return
        print("\n--- 最新文章列表 ---")
        for i, article in enumerate(articles, 1):
            # 截取文章内容的前 200 个字符，避免过长
            content_preview = article[:200] + ("..." if len(article) > 200 else "")
            print(f"{i}. {content_preview}")
            print("---------------------")
    

if __name__ == "__main__":
    manager = RssManager()
    while True:
        print("\n--- RSS 订阅管理 ---")
        print("1. 添加新的订阅")
        print("2. 查看所有订阅")
        print("0. 退出")

        choice = input("请选择操作（输入数字）：")
        
        if choice == "1":
            link = input("请输入 RSS 订阅链接：")
            manager.save_subscription(link)
        elif choice == "2":
            manager.view_subscriptions()
        elif choice == "0":
            print("感谢使用，再见！")
            sys.exit(0)
        else:
            print("无效的选择，请输入 1、2 或 0。")
