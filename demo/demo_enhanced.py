# -*- coding: utf-8 -*-
"""
这是一个美化后的 RSS 订阅管理脚本。
主要功能包括：
- 添加新的 RSS 订阅源
- 将订阅源信息（标题和链接）保存到本地的 JSON 文件中
- 加载并显示所有已保存的订阅源
- 通过命令行与用户交互，实现订阅的添加和查看
- 使用 rich 库美化界面显示
- 使用 BeautifulSoup 优化 HTML 内容清理

美化特性：
- 彩色面板和表格展示
- 美观的文章格式显示
- 更好的错误和成功消息展示
- 优化的文本换行处理
"""
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
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            print(f"读取订阅文件 {filename} 时发生错误：{e}")
            return {}
    
    @staticmethod
    def save_subscriptions(filename: str, subscriptions: Dict[str, str]) -> bool:
        """
        将订阅列表保存到指定的 JSON 文件中。

        Args:
            filename (str): 存储订阅信息的 JSON 文件名。
            subscriptions (Dict[str, str]): 要保存的订阅字典。

        Returns:
            bool: 保存是否成功。
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(subscriptions, file, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"保存订阅文件 {filename} 时发生错误：{e}")
            return False

class RssParser:
    """RSS 解析器，负责网络请求和 RSS 源解析"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.console = Console()
    
    def fetch_feed_info(self, url: str) -> Tuple[Optional[str], bool]:
        """
        获取 RSS 源的标题信息

        Args:
            url (str): RSS 源链接

        Returns:
            Tuple[Optional[str], bool]: (标题，是否成功)
        """
        try:
            with self.console.status("[bold green]正在获取 RSS 源信息..."):
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()

                feed = feedparser.parse(response.content)
                
                if feed.bozo:
                    warning_panel = Panel(
                        f"[yellow]⚠️  链接 {url} 可能不是一个有效的 RSS/Atom 源\n错误：{feed.bozo_exception}[/yellow]",
                        style="yellow",
                        border_style="yellow"
                    )
                    self.console.print(warning_panel)

                title = feed.feed.get("title")
                if not title:
                    warning_panel = Panel(
                        "[yellow]⚠️  无法从链接中获取标题，将使用默认名称[/yellow]",
                        style="yellow",
                        border_style="yellow"
                    )
                    self.console.print(warning_panel)
                    title = f"未命名订阅_{datetime.now():%Y%m%d%H%M%S}"
                
                success_panel = Panel(
                    f"[bold green]✅ 成功获取标题：{title}[/bold green]",
                    style="green",
                    border_style="green"
                )
                self.console.print(success_panel)
                return title, True

        except requests.exceptions.RequestException as e:
            error_panel = Panel(
                f"[red]❌ 网络请求错误：{e}[/red]",
                style="red",
                border_style="red"
            )
            self.console.print(error_panel)
            return None, False
        except Exception as e:
            error_panel = Panel(
                f"[red]❌ 处理订阅时发生未知错误：{e}[/red]",
                style="red",
                border_style="red"
            )
            self.console.print(error_panel)
            return None, False
    
    def fetch_articles(self, url: str, count: int = 3) -> List[Dict[str, str]]:
        """
        获取 RSS 源的最新文章

        Args:
            url (str): RSS 源链接
            count (int): 获取文章数量

        Returns:
            List[Dict[str, str]]: 文章列表
        """
        try:
            with self.console.status("[bold cyan]正在获取最新文章..."):
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()

                feed = feedparser.parse(response.content)

                if not feed.entries:
                    warning_panel = Panel(
                        f"[yellow]⚠️  链接 {url} 没有找到任何文章[/yellow]",
                        style="yellow",
                        border_style="yellow"
                    )
                    self.console.print(warning_panel)
                    return []

                articles = []
                for entry in feed.entries[:count]:
                    article = {
                        'title': entry.get("title", "无标题"),
                        'link': entry.get("link", "无链接"),
                        'summary': self._clean_html(entry.get("summary", "无摘要")),
                        'published': entry.get("published", "未知时间")
                    }
                    articles.append(article)

                return articles

        except requests.exceptions.RequestException as e:
            error_panel = Panel(
                f"[red]❌ 网络请求错误：{e}[/red]",
                style="red",
                border_style="red"
            )
            self.console.print(error_panel)
            return []
        except Exception as e:
            error_panel = Panel(
                f"[red]❌ 处理文章时发生未知错误：{e}[/red]",
                style="red",
                border_style="red"
            )
            self.console.print(error_panel)
            return []
    
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
        添加新订阅

        Args:
            url (str): RSS 链接

        Returns:
            bool: 是否添加成功
        """
        # 获取 RSS 源的标题信息
        title, success = self.rss_parser.fetch_feed_info(url)
        if not success or not title:
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
        删除指定序号的订阅

        Args:
            number (int): 订阅序号

        Returns:
            bool: 是否删除成功
        """
        subscriptions = self.file_handler.load_subscriptions(self.filename)
        
        if not subscriptions:
            warning_panel = Panel(
                "[yellow]⚠️  订阅列表为空，无法删除[/yellow]",
                style="yellow",
                border_style="yellow"
            )
            self.console.print(warning_panel)
            return False
        
        if number < 1 or number > len(subscriptions):
            error_panel = Panel(
                f"[red]❌ 无效的订阅序号：{number}。请提供有效的序号[/red]",
                style="red",
                border_style="red"
            )
            self.console.print(error_panel)
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
        """获取所有订阅"""
        return self.file_handler.load_subscriptions(self.filename)
    
    def get_subscription_by_index(self, index: int) -> Tuple[Optional[str], Optional[str]]:
        """
        根据索引获取订阅

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
        self.console = Console()
    
    def show_main_menu(self):
        """显示美化的主菜单"""
        main_menu = Panel(
            """[bold cyan]📰 RSS 订阅管理[/bold cyan]

[bold white]1.[/bold white] [green]添加新的订阅[/green]
[bold white]2.[/bold white] [blue]查看所有订阅[/blue]  
[bold white]0.[/bold white] [red]退出[/red]""",
            title="[bold yellow]主菜单[/bold yellow]",
            border_style="bright_blue",
            padding=(1, 2)
        )
        self.console.print(main_menu)
    
    def show_subscriptions_menu(self, subscriptions: Dict[str, str]):
        """显示美化的订阅列表菜单"""
        # 创建订阅列表表格
        table = Table(title="[bold cyan]📚 您已保存的订阅[/bold cyan]", show_header=True, header_style="bold magenta")
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

[bold white][d][/bold white] [red]删除订阅[/red]
[bold white][1-{len(subscriptions)}][/bold white] [blue]进入对应订阅查看文章[/blue]
[bold white][0][/bold white] [yellow]返回首页[/yellow]"""
        
        options_panel = Panel(
            operations,
            title="[bold cyan]操作指南[/bold cyan]",
            border_style="green",
            padding=(0, 1)
        )
        self.console.print(options_panel)
    
    def show_articles_menu(self, articles: List[Dict[str, str]]):
        """显示美化的文章列表菜单"""
        if articles:
            operations = f"""[bold green]🔧 操作选项：[/bold green]

[bold white][r][/bold white] [cyan]刷新文章列表[/cyan]
[bold white][b][/bold white] [blue]返回订阅列表[/blue]
[bold white][0][/bold white] [yellow]返回首页[/yellow]
[bold white][1-{len(articles)}][/bold white] [green]查看对应文章详情[/green]"""
        else:
            operations = """[bold green]🔧 操作选项：[/bold green]

[bold white][r][/bold white] [cyan]刷新文章列表[/cyan]
[bold white][b][/bold white] [blue]返回订阅列表[/blue]
[bold white][0][/bold white] [yellow]返回首页[/yellow]
[dim]暂无文章可查看[/dim]"""
        
        options_panel = Panel(
            operations,
            title="[bold cyan]操作指南[/bold cyan]",
            border_style="green",
            padding=(0, 1)
        )
        self.console.print(options_panel)

    def display_articles(self, articles: List[Dict[str, str]], subscription_name: str):
        """
        使用 rich 库美化显示文章列表

        Args:
            articles (List[Dict[str, str]]): 文章列表
            subscription_name (str): 订阅名称
        """
        # 创建标题面板
        title_panel = Panel(
            f"[bold cyan]{subscription_name}[/bold cyan] 的最新文章",
            style="bright_blue",
            border_style="blue"
        )
        self.console.print(title_panel)
        
        if not articles:
            warning_panel = Panel(
                "[yellow]⚠️  未能获取到文章，可能是网络问题或链接失效[/yellow]",
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
            if len(summary) > 300:
                summary = summary[:297] + "..."
            
            # 使用 textwrap 为长摘要添加适当的换行
            wrapped_summary = textwrap.fill(summary, width=80)
            
            # 添加发布时间（如果有的话）
            time_info = ""
            if 'published' in article and article['published'] != "未知时间":
                time_info = f"\n\n[bold blue]📅 发布时间:[/bold blue] [dim]{article['published']}[/dim]"
            
            # 创建文章内容
            article_content = f"""[bold blue]🔗 链接:[/bold blue] [link={article['link']}]{article['link']}[/link]

[bold green]📄 摘要:[/bold green]
{wrapped_summary}{time_info}"""
            
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
        return input(f"\n{prompt}").strip()
    
    def handle_subscriptions_view(self) -> NavigationAction:
        """处理订阅列表视图"""
        while True:
            # 获取所有订阅
            subscriptions = self.subscription_manager.get_subscriptions()
            
            if not subscriptions:
                info_panel = Panel(
                    "[blue]📝 您的订阅列表为空，请先添加订阅[/blue]",
                    style="blue",
                    border_style="blue"
                )
                self.console.print(info_panel)
                return NavigationAction.BACK_TO_HOME
            
            # 显示订阅列表菜单
            self.show_subscriptions_menu(subscriptions)
            
            try:
                choice = self.get_user_input("请选择操作：")
                
                if choice == "0":
                    return NavigationAction.BACK_TO_HOME
                
                if choice.lower() == "d":
                    try:
                        number = int(self.get_user_input("请输入要删除的订阅序号："))
                        self.subscription_manager.delete_subscription(number)
                    except ValueError:
                        error_panel = Panel(
                            "[red]❌ 无效的序号，请输入数字[/red]",
                            style="red",
                            border_style="red"
                        )
                        self.console.print(error_panel)
                    continue

                choice_num = int(choice)
                if 1 <= choice_num <= len(subscriptions):
                    selected_name, selected_url = self.subscription_manager.get_subscription_by_index(choice_num)
                    if selected_name and selected_url:
                        action = self.handle_single_subscription_view(selected_name, selected_url)
                        if action == NavigationAction.BACK_TO_HOME:
                            return NavigationAction.BACK_TO_HOME
                else:
                    error_panel = Panel(
                        "[red]❌ 无效的选择，请输入正确的序号[/red]",
                        style="red",
                        border_style="red"
                    )
                    self.console.print(error_panel)
                    
            except ValueError:
                error_panel = Panel(
                    "[red]❌ 请输入有效的数字序号[/red]",
                    style="red",
                    border_style="red"
                )
                self.console.print(error_panel)
            except Exception as e:
                error_panel = Panel(
                    f"[red]❌ 发生错误：{e}[/red]",
                    style="red",
                    border_style="red"
                )
                self.console.print(error_panel)
    
    def handle_single_subscription_view(self, subscription_name: str, subscription_url: str) -> NavigationAction:
        """处理单个订阅视图"""
        while True:
            articles = self.rss_parser.fetch_articles(subscription_url)
            self.display_articles(articles, subscription_name)
            # 无论是否有文章，都显示菜单
            self.show_articles_menu(articles)
            
            choice = self.get_user_input("请选择操作：").lower()
            
            if choice == "b":
                return NavigationAction.BACK_TO_LIST
            elif choice == "0":
                return NavigationAction.BACK_TO_HOME
            elif choice == "r":
                refresh_panel = Panel(
                    "[cyan]🔄 正在刷新...[/cyan]",
                    style="cyan",
                    border_style="cyan"
                )
                self.console.print(refresh_panel)
                continue
            elif choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(articles):
                    # 调用浏览器打开文章链接
                    article = articles[choice_num - 1]
                    info_panel = Panel(
                        f"[green]🌐 正在打开文章：{article['title']}\n{article['link']}[/green]",
                        style="green",
                        border_style="green"
                    )
                    self.console.print(info_panel)
                    try:
                        webbrowser.open(article['link'])
                    except Exception as e:
                        error_panel = Panel(
                            f"[red]❌ 无法打开链接：{e}[/red]",
                            style="red",
                            border_style="red"
                        )
                        self.console.print(error_panel)
                else:
                    error_panel = Panel(
                        "[red]❌ 无效的选择，请输入正确的文章序号[/red]",
                        style="red",
                        border_style="red"
                    )
                    self.console.print(error_panel)
            else:
                error_panel = Panel(
                    "[red]❌ 无效的选择，请重新输入[/red]",
                    style="red",
                    border_style="red"
                )
                self.console.print(error_panel)

class RssApp:
    """RSS 应用主控制器，协调各个组件"""
    
    def __init__(self):
        self.ui = UserInterface()
        self.console = Console()
    
    def run(self):
        """运行应用程序主循环"""
        # 显示欢迎消息
        welcome_panel = Panel(
            """[bold magenta]欢迎使用 RSS 订阅管理器！[/bold magenta]

✨ 特色功能：
• [green]美观的界面显示[/green]
• [blue]优化的文章格式[/blue]
• [yellow]智能的 HTML 内容清理[/yellow]
• [cyan]丰富的交互体验[/cyan]""",
            title="[bold red]🎉 RSS 阅读器增强版[/bold red]",
            border_style="magenta",
            padding=(1, 2)
        )
        self.console.print(welcome_panel)
        
        while True:
            self.ui.show_main_menu()
            choice = self.ui.get_user_input("请选择操作（输入数字）：")
            
            if choice == "1":
                self._handle_add_subscription()
            elif choice == "2":
                self._handle_view_subscriptions()
            elif choice == "0":
                goodbye_panel = Panel(
                    "[bold green]感谢使用 RSS 订阅管理器，再见！👋[/bold green]",
                    style="green",
                    border_style="green"
                )
                self.console.print(goodbye_panel)
                sys.exit(0)
            else:
                error_panel = Panel(
                    "[red]❌ 无效的选择，请输入 1、2 或 0[/red]",
                    style="red",
                    border_style="red"
                )
                self.console.print(error_panel)
    
    def _handle_add_subscription(self):
        """处理添加订阅"""
        url = self.ui.get_user_input("请输入 RSS 订阅链接：")
        if url.strip():
            self.ui.subscription_manager.add_subscription(url.strip())
        else:
            error_panel = Panel(
                "[red]❌ 链接不能为空[/red]",
                style="red",
                border_style="red"
            )
            self.console.print(error_panel)
    
    def _handle_view_subscriptions(self):
        """处理查看订阅"""
        self.ui.handle_subscriptions_view()


if __name__ == "__main__":
    app = RssApp()
    app.run()
