#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS 终端阅读器
一个简单易用的终端 RSS 订阅管理和阅读工具
"""

import json
import os
import sys
import webbrowser
from datetime import datetime
from typing import Dict, List, Optional

try:
    import requests1
    import feedparser
except ImportError:
    print("❌ 缺少必要的依赖库！")
    print("请运行以下命令安装：")
    print("pip install requests feedparser")
    sys.exit(1)


class RSSReader:
    def __init__(self):
        """初始化 RSS 阅读器"""
        self.config_file = "rss_subscriptions.json"
        self.subscriptions = {}
        self.load_subscriptions()
    
    def load_subscriptions(self):
        """从本地文件加载订阅源"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.subscriptions = json.load(f)
                print(f"✅ 已加载 {len(self.subscriptions)} 个订阅源")
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"⚠️  配置文件读取错误: {e}")
                self.subscriptions = {}
        else:
            print("🆕 首次使用，将创建新的订阅配置")
            self.subscriptions = {}
    
    def save_subscriptions(self):
        """保存订阅源到本地文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.subscriptions, f, ensure_ascii=False, indent=2)
            print("💾 订阅源已保存")
        except Exception as e:
            print(f"❌ 保存失败: {e}")
    
    def add_subscription(self, name: str, url: str) -> bool:
        """添加新的订阅源"""
        try:
            # 验证 RSS 链接是否有效
            print(f"🔍 正在验证 RSS 链接: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # 尝试解析 RSS 内容
            feed = feedparser.parse(response.content)
            if not feed.entries:
                print("⚠️  该链接似乎不是有效的 RSS 源或暂无内容")
                return False
            
            # 获取 RSS 源的标题（如果用户没有自定义名称）
            feed_title = feed.feed.get('title', name)
            if name.strip() == '':
                name = feed_title
            
            self.subscriptions[name] = url
            self.save_subscriptions()
            print(f"✅ 成功添加订阅源: {name}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求失败: {e}")
            return False
        except Exception as e:
            print(f"❌ 添加订阅源失败: {e}")
            return False
    
    def remove_subscription(self, name: str) -> bool:
        """删除订阅源"""
        if name in self.subscriptions:
            del self.subscriptions[name]
            self.save_subscriptions()
            print(f"🗑️  已删除订阅源: {name}")
            return True
        else:
            print(f"❌ 未找到订阅源: {name}")
            return False
    
    def list_subscriptions(self):
        """列出所有订阅源"""
        if not self.subscriptions:
            print("📭 暂无订阅源，请先添加一些订阅")
            return
        
        print("\n📚 当前订阅源列表:")
        print("-" * 50)
        for i, (name, url) in enumerate(self.subscriptions.items(), 1):
            print(f"[{i}] {name}")
            print(f"    🔗 {url}")
        print("-" * 50)
    
    def fetch_articles(self, url: str, limit: int = 5) -> List[Dict]:
        """获取指定 RSS 源的文章列表"""
        try:
            print(f"📡 正在获取最新文章...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            articles = []
            
            for entry in feed.entries[:limit]:
                article = {
                    'title': entry.get('title', '无标题'),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', entry.get('description', '无摘要')),
                    'published': entry.get('published', '未知日期')
                }
                articles.append(article)
            
            return articles
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求失败: {e}")
            return []
        except Exception as e:
            print(f"❌ 解析失败: {e}")
            return []
    
    def display_articles(self, articles: List[Dict]):
        """展示文章列表"""
        if not articles:
            print("📭 暂无文章")
            return
        
        print(f"\n📰 最新文章 (共 {len(articles)} 篇):")
        print("=" * 70)
        
        for i, article in enumerate(articles, 1):
            print(f"\n[{i}] {article['title']}")
            print(f"📅 {article['published']}")
            
            # 截取摘要
            summary = article['summary']
            if len(summary) > 200:
                summary = summary[:200] + "..."
            
            # 清理 HTML 标签
            import re
            summary = re.sub(r'<[^>]+>', '', summary)
            print(f"📝 {summary}")
            print(f"🔗 {article['link']}")
            print("-" * 70)
    
    def read_feed(self, subscription_name: str):
        """阅读指定订阅源的文章"""
        if subscription_name not in self.subscriptions:
            print(f"❌ 未找到订阅源: {subscription_name}")
            return
        
        url = self.subscriptions[subscription_name]
        print(f"\n📖 正在阅读: {subscription_name}")
        
        articles = self.fetch_articles(url)
        if not articles:
            return
        
        self.display_articles(articles)
        
        while True:
            print("\n🔧 操作选项:")
            print("  [1-{}] 在浏览器中打开对应文章".format(len(articles)))
            print("  [r] 刷新文章列表")
            print("  [b] 返回主菜单")
            
            choice = input("\n请选择操作: ").strip().lower()
            
            if choice == 'b':
                break
            elif choice == 'r':
                print("\n🔄 刷新中...")
                articles = self.fetch_articles(url)
                if articles:
                    self.display_articles(articles)
            elif choice.isdigit():
                article_num = int(choice)
                if 1 <= article_num <= len(articles):
                    article = articles[article_num - 1]
                    print(f"🌐 正在打开: {article['title']}")
                    webbrowser.open(article['link'])
                else:
                    print("❌ 无效的文章编号")
            else:
                print("❌ 无效的选择，请重新输入")
    
    def main_menu(self):
        """主菜单"""
        print("\n🎉 欢迎使用 RSS 终端阅读器!")
        
        while True:
            print("\n" + "=" * 50)
            print("📱 主菜单")
            print("=" * 50)
            print("[1] 查看订阅源列表")
            print("[2] 添加订阅源")
            print("[3] 删除订阅源")
            print("[4] 阅读订阅")
            print("[5] 退出程序")
            print("=" * 50)
            
            choice = input("请选择操作 (1-5): ").strip()
            
            if choice == '1':
                self.list_subscriptions()
                
            elif choice == '2':
                print("\n➕ 添加新订阅源")
                name = input("请输入订阅源名称 (留空将自动获取): ").strip()
                url = input("请输入 RSS 链接: ").strip()
                
                if not url:
                    print("❌ RSS 链接不能为空")
                    continue
                
                self.add_subscription(name, url)
                
            elif choice == '3':
                if not self.subscriptions:
                    print("📭 暂无订阅源可删除")
                    continue
                
                self.list_subscriptions()
                name = input("\n请输入要删除的订阅源名称: ").strip()
                self.remove_subscription(name)
                
            elif choice == '4':
                if not self.subscriptions:
                    print("📭 暂无订阅源，请先添加一些订阅")
                    continue
                
                self.list_subscriptions()
                print("\n📖 选择要阅读的订阅源:")
                
                # 创建编号到订阅源名称的映射
                subscription_list = list(self.subscriptions.keys())
                choice_input = input("请输入订阅源编号或名称: ").strip()
                
                # 处理数字输入
                if choice_input.isdigit():
                    sub_num = int(choice_input)
                    if 1 <= sub_num <= len(subscription_list):
                        subscription_name = subscription_list[sub_num - 1]
                        self.read_feed(subscription_name)
                    else:
                        print("❌ 无效的编号")
                else:
                    # 处理名称输入
                    if choice_input in self.subscriptions:
                        self.read_feed(choice_input)
                    else:
                        print("❌ 未找到该订阅源")
                
            elif choice == '5':
                print("👋 感谢使用，再见!")
                sys.exit(0)
                
            else:
                print("❌ 无效的选择，请输入 1-5")


def main():
    """主函数"""
    try:
        reader = RSSReader()
        reader.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断，再见!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
