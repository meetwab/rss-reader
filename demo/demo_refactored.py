
import json
import os
import html
import sys
import textwrap
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests
import feedparser
import re
from enum import Enum, auto
import webbrowser
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.markdown import Markdown
from bs4 import BeautifulSoup

class NavigationAction(Enum):
    """定义用户在视图之间导航的动作，以替代"魔术字符串"。"""
    BACK_TO_LIST = auto()
    BACK_TO_HOME = auto()

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
        从指定的 JSON 文件中加载订阅源的历史文章。

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
        将订阅源的历史文章保存到 JSON 文件

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

class ArticleManager:
    """文章管理器，负责文章历史数据的存储、检索和管理"""
    
    def __init__(self, articles_history_file: str = "articles_history.json"):
        self.articles_history_file = articles_history_file
        self.file_handler = FileHandler()
    
    def get_articles_history(self, url: str, page_size: int = 5, page: int = 1) -> Tuple[List[Dict[str, str]], bool, int, int]:
        """
        1. 获取 RSS 订阅源的历史文章；
        2. 通过 页码 与 每页文章数量 进行分页，找出当前页面应该显示的文章；

        Args:
            url (str): RSS 源链接
            page_size (int): 每页文章数量
            page (int): 页码（从 1 开始）

        Returns:
            Tuple[List[Dict[str, str]], bool, int, int]: (当前页的文章列表，是否有下一页，当前页码，总页数)
        """
        articles_history = self.file_handler.load_articles_history(self.articles_history_file)
        all_articles = articles_history.get(url, [])
        
        # 按获取时间倒序排列，最新的在前面
        all_articles.sort(key=lambda x: x.get('fetch_time', ''), reverse=True)
        
        # 计算总页数
        total_articles = len(all_articles)
        total_pages = (total_articles + page_size - 1) // page_size if total_articles > 0 else 1
        
        # 计算当前页面的起始和结束索引，获取当前页面的文章
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_articles = all_articles[start_idx:end_idx]
        
        # 检查是否有更多页
        has_more = end_idx < len(all_articles)
        
        return page_articles, has_more, page, total_pages
    
    def update_articles_history(self, url: str, new_articles: List[Dict[str, str]]):
        """
        1. 把最新的 RSS 订阅源的文章添加到 articles_history.json 文件中;
        2. 如果文章链接已存在，则不重复添加。

        Args:
            url (str): RSS 源链接
            new_articles (List[Dict[str, str]]): 新获取的文章列表
        """
        # 加载现有历史记录
        articles_history = self.file_handler.load_articles_history(self.articles_history_file)
        
        # 获取该订阅的现有文章
        existing_articles = articles_history.get(url, [])
        # 创建一个集合用于快速查找现有文章链接
        existing_links = {article['link'] for article in existing_articles}
        
        # 只添加新文章（通过链接去重）
        for article in new_articles:
            if article['link'] not in existing_links:
                existing_articles.append(article)
                existing_links.add(article['link'])
        
        # 更新历史记录
        articles_history[url] = existing_articles
        
        # 保存到文件
        self.file_handler.save_articles_history(self.articles_history_file, articles_history)

class RssParser:
    """RSS 解析器，负责网络请求和 RSS 源解析"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.console = Console()
        self.article_manager = ArticleManager()
    
    def fetch_feed_info(self, url: str) -> Tuple[Optional[str], bool]:
        """
        获取 RSS 源的标题信息

        Args:
            url (str): RSS 源链接

        Returns:
            Tuple[Optional[str], bool]: (标题，是否成功)
        """
        try:
            print(f"正在请求链接：{url}")
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            feed = feedparser.parse(response.content)
            
            if feed.bozo:
                print(f" 警告：链接 {url} 可能不是一个有效的 RSS/Atom 源。错误：{feed.bozo_exception}")

            title = feed.feed.get("title")
            if not title:
                print(" 无法从链接中获取标题，将使用默认名称。")
                title = f"未命名订阅_{datetime.now():%Y%m%d%H%M%S}"
            
            print(f"成功获取标题：{title}")
            return title, True

        except requests.exceptions.SSLError:
            print(" ❌ SSL 连接错误：无法建立安全连接，可能是网站证书问题")
            return None, False
        except requests.exceptions.Timeout:
            print(" ⏰ 连接超时：网络响应过慢，请稍后重试")
            return None, False
        except requests.exceptions.ConnectionError:
            print(" 🌐 连接错误：无法连接到服务器，请检查网络连接")
            return None, False
        except requests.exceptions.HTTPError as e:
            print(f" 🚫 HTTP 错误：服务器返回错误状态码 {e.response.status_code}")
            return None, False
        except requests.exceptions.RequestException:
            print(" 📡 网络请求失败：连接或传输过程中发生问题")
            return None, False
        except Exception:
            print(" ❓ 处理订阅时发生未知错误，请稍后重试")
            return None, False
    
    def fetch_articles(self, url: str, count: int = 3) -> List[Dict[str, str]]:
        """
        获取 RSS 源的最新文章（纯获取功能，不涉及数据持久化）

        Args:
            url (str): RSS 源链接
            count (int): 获取文章数量

        Returns:
            List[Dict[str, str]]: 文章列表
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            feed = feedparser.parse(response.content)

            if not feed.entries:
                print(f" 警告：链接 {url} 没有找到任何文章。")
                return []

            # 获取新文章
            new_articles = []
            for entry in feed.entries[:count]:
                article = {
                    'title': entry.get("title", "无标题"),
                    'link': entry.get("link", "无链接"),
                    'summary': self._clean_html(entry.get("summary", "无摘要")),
                    'published': entry.get("published", ""),
                    'fetch_time': datetime.now().isoformat()
                }
                new_articles.append(article)
            
            return new_articles

        except requests.exceptions.SSLError:
            print(" ❌ SSL 连接错误：无法建立安全连接，可能是网站证书问题")
            return []
        except requests.exceptions.Timeout:
            print(" ⏰ 连接超时：网络响应过慢，请稍后重试")
            return []
        except requests.exceptions.ConnectionError:
            print(" 🌐 连接错误：无法连接到服务器，请检查网络连接")
            return []
        except requests.exceptions.HTTPError as e:
            print(f" 🚫 HTTP 错误：服务器返回错误状态码 {e.response.status_code}")
            return []
        except requests.exceptions.RequestException as e:
            print(" 📡 网络请求失败：连接或传输过程中发生问题")
            return []
        except Exception as e:
            print(" ❓ 处理文章时发生未知错误，请稍后重试")
            return []
    
    def fetch_and_save_articles(self, url: str, count: int = 3) -> List[Dict[str, str]]:
        """
        1. 获取 RSS 源的最新文章并保存到 articles_history.json 文件中。

        Args:
            url (str): RSS 源链接
            count (int): 获取文章数量

        Returns:
            List[Dict[str, str]]: 文章列表
        """
        # 获取新文章
        new_articles = self.fetch_articles(url, count)
        
        # 如果获取成功，则更新历史记录
        if new_articles:
            self.article_manager.update_articles_history(url, new_articles)
        
        return new_articles
    
    def _clean_html(self, text: str) -> str:
        """使用 BeautifulSoup 清理 HTML 标签，保留文本内容"""
        if not text:
            return text
        
        try:
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(text, 'html.parser')
            
            # 移除 script 和 style 标签
            for script in soup(["script", "style"]):
                script.decompose()
            
            # 获取纯文本
            clean_text = soup.get_text()
            
            # 清理多余的空白字符
            clean_text = re.sub(r'\s+', ' ', clean_text)
            clean_text = html.unescape(clean_text)
            
            return clean_text.strip()
        except Exception:
            # 如果 BeautifulSoup 解析失败，回退到原始方法
            clean_text = re.sub(r'<[^>]+>', '', text)
            clean_text = re.sub(r'\s+', ' ', clean_text)
            clean_text = html.unescape(clean_text)
            return clean_text.strip()

class SubscriptionManager:
    """订阅管理器，负责订阅的增删改查"""
    
    def __init__(self, filename: str = "subscriptions.json"):
        self.filename = filename
        self.file_handler = FileHandler()
        self.rss_parser = RssParser()
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
        if not success:
            return False
        
        # 加载现有订阅
        subscriptions = self.file_handler.load_subscriptions(self.filename)
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
    
    def delete_subscription(self, number: int) -> bool:
        """
        1. 删除指定的 RSS 订阅源；
        2. 从 subscriptions.json 文件中删除订阅信息。

        Args:
            number (int): 订阅序号

        Returns:
            bool: 是否删除成功
        """
        subscriptions = self.file_handler.load_subscriptions(self.filename)
        
        if not subscriptions:
            warning_panel = Panel(
                "[yellow]⚠️  订阅列表为空，无法删除 [/yellow]",
                style="yellow",
                border_style="yellow"
            )
            self.console.print(warning_panel)
            return False
        
        if number < 1 or number > len(subscriptions):
            print(f" 无效的订阅序号：{number}。请提供有效的序号。")
            return False
        
        # 获取订阅名称
        subscription_name = list(subscriptions.keys())[number - 1]
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

class UserInterface:
    """用户界面处理器，负责用户交互和界面显示"""
    
    def __init__(self):
        self.subscription_manager = SubscriptionManager()
        self.rss_parser = RssParser()
        self.article_manager = ArticleManager()
        self.console = Console()
    
    def show_main_menu(self):
        """显示美化的主菜单"""
        main_menu = Panel(
            """[bold cyan]📰 RSS 订阅管理 [/bold cyan]

1. [green] 添加新的订阅 [/green]
2. [blue] 查看所有订阅 [/blue]  
0. [red] 退出 [/red]""",
            title="[bold yellow] 主菜单 [/bold yellow]",
            border_style="bright_blue",
            padding=(1, 2)
        )
        self.console.print(main_menu)
    
    def show_subscriptions_menu(self, subscriptions: Dict[str, str]):
        """显示美化的订阅列表菜单"""
        # 创建订阅列表表格
        table = Table(title="[bold cyan]📚 您已保存的订阅 [/bold cyan]", show_header=True, header_style="bold magenta")
        table.add_column("序号", style="bold blue", justify="center", width=6)
        table.add_column("订阅名称", style="bold white", min_width=20)
        table.add_column("RSS 链接", style="dim blue", overflow="fold")
        
        for i, (name, url) in enumerate(subscriptions.items(), 1):
            # 限制 URL 显示长度
            display_url = url if len(url) <= 60 else url[:57] + "..."
            table.add_row(str(i), name, display_url)
        
        self.console.print(table)
        
        # 操作选项面板
        operations = f"""[bold green]🔧 操作选项：[/bold green]

[d] [red] 删除订阅 [/red]
[1-{len(subscriptions)}] [blue] 进入对应订阅查看文章 [/blue]
[0] [yellow] 返回首页 [/yellow]"""
        
        options_panel = Panel(
            operations,
            title="[bold cyan] 操作指南 [/bold cyan]",
            border_style="green",
            padding=(0, 1)
        )
        self.console.print(options_panel)
    
    def show_articles_menu(self, articles: List[Dict[str, str]], current_page: int = 1, total_pages: int = 1):
        """显示文章列表菜单"""
        print("\n操作选项：")
        print("[0] 返回首页")
        print("[b] 返回订阅列表") 
        print("[r] 刷新文章列表")
        
        if articles:
            print(f"[1-{len(articles)}] 查看对应文章详情")
        else:
            print("暂无文章可查看")

        # 分页导航
        if current_page > 1:
            print("[p] 上一页")
        if current_page < total_pages:
            print("[n] 下一页")
            
        # 显示页码信息
        if total_pages > 1:
            print(f"\n📄 当前第 {current_page}/{total_pages} 页")
        print()    

    def display_articles(self, articles: List[Dict[str, str]], subscription_name: str, current_page: int = 1, total_pages: int = 1):
        """
        显示文章列表

        Args:
            articles (List[Dict[str, str]]): 文章列表
            subscription_name (str): 订阅名称
            current_page (int): 当前页码
            total_pages (int): 总页数
        """
        # 创建标题面板
        page_info = f" (第{current_page}/{total_pages}页)" if total_pages > 1 else ""
        title_panel = Panel(
            f"[bold cyan]{subscription_name}{page_info}[/bold cyan]",
            style="bright_blue",
            border_style="blue"
        )
        self.console.print(title_panel)
        
        if not articles:
            warning_panel = Panel(
                "[yellow]⚠️  未能获取到文章，可能是网络问题或链接失效 [/yellow]",
                style="yellow",
                border_style="yellow"
            )
            self.console.print(warning_panel)
            return
        
        # 为每篇文章创建美化的显示
        for i, article in enumerate(articles, 1):
            # 文章标题
            title_text = Text()
            title_text.append(f"{i}. ", style="bold magenta")
            title_text.append(article['title'], style="bold white")
            
            # 处理摘要文本，确保换行美观
            summary = article['summary']
            if len(summary) > 400:
                summary = summary[:397] + "..."
            
            # 使用 textwrap 为长摘要添加适当的换行
            wrapped_summary = textwrap.fill(summary, width=80)
            
            # 创建文章内容，添加时间信息
            article_content = f"""[bold blue]🔗 链接:[/bold blue] [link={article['link']}]{article['link']}[/link]"""
            
            # 添加发布时间（如果有的话）
            if article.get('published'):
                article_content += f"\n[bold yellow]📅 发布时间:[/bold yellow] {article['published']}"
            
            # 添加获取时间（如果有的话）
            if article.get('fetch_time'):
                try:
                    fetch_datetime = datetime.fromisoformat(article['fetch_time'])
                    fetch_time_str = fetch_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    article_content += f"\n[bold green]⏰ 获取时间:[/bold green] {fetch_time_str}"
                except ValueError:
                    pass
            
            article_content += f"\n\n[bold green]📄 摘要:[/bold green]\n{wrapped_summary}"
            
            # 创建文章面板
            article_panel = Panel(
                article_content,
                title=title_text,
                title_align="left",
                border_style="dim",
                padding=(0, 1)
            )
            
            self.console.print(article_panel)
            self.console.print()  # 添加空行分隔
    
    def get_user_input(self, prompt: str) -> str:
        """获取用户输入"""
        return input(prompt).strip()
    
    def handle_subscriptions_view(self) -> NavigationAction:
        """处理订阅列表视图"""
        while True:
            # 获取所有订阅
            subscriptions = self.subscription_manager.get_subscriptions()
            
            if not subscriptions:
                info_panel = Panel(
                    "[blue]📝 您的订阅列表为空，请先添加订阅 [/blue]",
                    style="blue",
                    border_style="blue"
                )
                self.console.print(info_panel)
                return NavigationAction.BACK_TO_HOME
            
            # 显示订阅列表菜单
            self.show_subscriptions_menu(subscriptions)
            
            try:
                choice = self.get_user_input("\n请选择操作：")
                
                # 返回首页
                if choice == "0":
                    return NavigationAction.BACK_TO_HOME
                
                # 删除订阅源
                if choice.lower() == "d":
                    try:
                        number = int(self.get_user_input("请输入要删除的订阅序号："))
                        self.subscription_manager.delete_subscription(number)
                    except ValueError:
                        print(" 无效的序号，请输入数字。")
                    continue

                # 把用户输入转换为整数
                choice_num = int(choice)
                # 检查用户输入的序号是否在有效范围内：1～len(subscriptions)
                if 1 <= choice_num <= len(subscriptions):
                    # 获取指定订阅源的信息：name 和 url
                    selected_name, selected_url = self.subscription_manager.get_subscription_by_index(choice_num)
                    # 如果获取成功，则进入 "单个订阅视图"
                    if selected_name and selected_url:
                        action = self.handle_single_subscription_view(selected_name, selected_url)
                        # 根据用户在 "单个订阅视图" 中的操作，返回相应的导航动作
                        if action == NavigationAction.BACK_TO_HOME:
                            return NavigationAction.BACK_TO_HOME
                else:
                    print(" 无效的选择，请输入正确的序号。")
                    
            except ValueError:
                print(" 请输入有效的数字序号。")
            except Exception as e:
                print(f" 发生错误：{e}")
    
    def handle_single_subscription_view(self, subscription_name: str, subscription_url: str) -> NavigationAction:
        """
        1. 单个订阅文章视图的 "总控制器";
        2. 负责处理文章的获取、显示和用户交互。
        """
        current_page = 1
        page_message = None  # 用于存储需要在文章列表后显示的消息
        
        # 首次进入时获取最新文章并保存到历史记录
        print("\n🔄 正在获取最新文章...")
        self.rss_parser.fetch_and_save_articles(subscription_url)
        
        while True:
            # 获取当前订阅源的历史文章，分页展示
            articles, has_more, current_page, total_pages = self.article_manager.get_articles_history(
                subscription_url, page_size=5, page=current_page
            )
            
            # 显示文章
            self.display_articles(articles, subscription_name, current_page, total_pages)
            
            # 显示菜单
            self.show_articles_menu(articles, current_page, total_pages)
            
            # 在菜单后显示上一轮操作的提示消息（如已在首页/末页）。
            # 这种延迟显示的设计可以确保用户在看到提示时，界面已刷新为当前页，用户体验更佳。
            message_map = {
                "first_page": "[yellow]😊 已经是第一页啦~ [/yellow]",
                "last_page": "[yellow]😊 已经是最后一页啦~ [/yellow]",
            }
            if page_message in message_map:
                info_panel = Panel(
                    message_map[page_message],
                    style="yellow",
                    border_style="yellow"
                )
                self.console.print(info_panel)
            
            # 每次循环后重置消息状态，确保提示只显示一次
            page_message = None
            
            choice = self.get_user_input("\n请选择操作：").lower()
            
            if choice == "b":
                return NavigationAction.BACK_TO_LIST
            elif choice == "0":
                return NavigationAction.BACK_TO_HOME
            elif choice == "r":
                print("\n🔄 正在刷新...")
                # 获取最新文章并保存到历史记录
                self.rss_parser.fetch_and_save_articles(subscription_url)
                current_page = 1  # 刷新后回到第一页
                continue
            elif choice == "p":
                # 上一页
                if current_page > 1:
                    current_page -= 1
                else:
                    # 设置标志，在显示文章后显示提示
                    page_message = "first_page"
                continue
            elif choice == "n":
                # 下一页
                if current_page < total_pages:
                    current_page += 1
                else:
                    # 设置标志，在显示文章后显示提示
                    page_message = "last_page"
                continue
            elif choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(articles):
                    # 调用浏览器打开文章链接
                    article = articles[choice_num - 1]
                    print(f"正在打开文章：{article['title']} ({article['link']})")
                    try:
                        webbrowser.open(article['link'])
                    except Exception as e:
                        print(f" 无法打开链接：{e}")
            else:
                print(" 无效的选择，请重新输入。")

class RssApp:
    """RSS 应用主控制器，协调各个组件"""
    
    def __init__(self):
        self.ui = UserInterface()
    
    def run(self):
        """运行应用程序主循环"""
        while True:
            self.ui.show_main_menu()
            choice = self.ui.get_user_input("请选择操作（输入数字）：")
            
            if choice == "1":
                self._handle_add_subscription()
            elif choice == "2":
                self._handle_view_subscriptions()
            elif choice == "0":
                print("感谢使用，再见！")
                sys.exit(0)
            else:
                print("无效的选择，请输入 1、2 或 0。")
    
    def _handle_add_subscription(self):
        """处理添加订阅"""
        url = self.ui.get_user_input("请输入 RSS 订阅链接：")
        self.ui.subscription_manager.add_subscription(url)
    
    def _handle_view_subscriptions(self):
        """处理查看订阅"""
        self.ui.handle_subscriptions_view()


if __name__ == "__main__":
    app = RssApp()
    app.run()
