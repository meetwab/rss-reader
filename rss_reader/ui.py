"""
User interface handling and display logic.
"""

import textwrap
import webbrowser
from datetime import datetime
from typing import Dict, List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .models import NavigationAction
from .subscription_manager import SubscriptionManager
from .rss_parser import RssParser
from .article_manager import ArticleManager


class UserInterface:
    """用户界面处理器，负责用户交互和界面显示"""
    
    def __init__(self):
        self.article_manager = ArticleManager()
        self.subscription_manager = SubscriptionManager(article_manager=self.article_manager)
        self.rss_parser = RssParser(article_manager=self.article_manager)
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
        
        # 操作选项
        print("\n操作选项：")
        print(f"[1-{len(subscriptions)}] 进入对应订阅查看文章")
        print("[d]  删除订阅")
        print("[0]  返回首页")
    
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
    
    def confirm_delete_subscription(self, subscription_name: str, subscription_url: str) -> bool:
        """
        显示删除确认信息并获取用户确认

        Args:
            subscription_name (str): 订阅名称
            subscription_url (str): 订阅链接

        Returns:
            bool: 用户是否确认删除
        """
        # 显示要删除的订阅信息
        print(f"\n准备删除订阅：")
        print(f"  名称：{subscription_name}")
        print(f"  链接：{subscription_url}")

        confirm = input("\n确认删除？(y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("已取消删除操作。")
            return False
        return True
    
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
                    number_input = self.get_user_input("请输入要删除的订阅序号：")
                    try:
                        number = int(number_input)
                    except ValueError:
                        print(" 无效的序号，请输入数字。")
                        continue
                    subscription_name, subscription_url = self.subscription_manager.get_subscription_info(number)
                    if not (subscription_name and subscription_url):
                        print(" 无效的订阅序号，请输入正确的序号。")
                        continue
                    if not self.confirm_delete_subscription(subscription_name, subscription_url):
                        continue
                    self.subscription_manager.delete_subscription(number)
                    continue

                # 把用户输入转换为整数
                choice_num = int(choice)
                
                # 获取指定订阅源的信息，get_subscription_by_index 会处理无效序号
                selected_name, selected_url = self.subscription_manager.get_subscription_by_index(choice_num)
                
                # 如果获取成功，则进入 "单个订阅视图"
                if selected_name and selected_url:
                    action = self.handle_single_subscription_view(selected_name, selected_url)
                    # 如果用户从文章列表视图选择返回首页，则直接退出当前循环
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
            articles, _, current_page, total_pages = self.article_manager.get_paginated_articles(
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
