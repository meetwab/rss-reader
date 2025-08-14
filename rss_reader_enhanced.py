#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS 终端阅读器 - 增强版
包含更多实用功能的版本
"""

import json
import os
import sys
import webbrowser
import time
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional
from urllib.parse import urlparse

try:
    import requests
    import feedparser
except ImportError:
    print("❌ 缺少必要的依赖库！")
    print("请运行以下命令安装：")
    print("pip install requests feedparser")
    sys.exit(1)


class RSSReaderEnhanced:
    def __init__(self):
        """初始化增强版 RSS 阅读器"""
        self.config_file = "rss_subscriptions.json"
        self.cache_file = "rss_cache.json"
        self.subscriptions = {}
        self.cache = {}
        self.load_subscriptions()
        self.load_cache()
        
        # 请求头，避免被某些网站拒绝
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/rss+xml, application/atom+xml, application/xml, text/xml'
        }
    
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
    
    def load_cache(self):
        """加载文章缓存"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.cache = {}
        else:
            self.cache = {}
    
    def save_cache(self):
        """保存文章缓存"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  缓存保存失败: {e}")
    
    def validate_url(self, url: str) -> bool:
        """验证 URL 格式"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def clean_html(self, text: str) -> str:
        """清理 HTML 标签和多余空白"""
        # 移除 HTML 标签
        text = re.sub(r'<[^>]+>', '', text)
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 解码 HTML 实体
        import html
        text = html.unescape(text)
        return text.strip()
    
    def format_date(self, date_str: str) -> str:
        """格式化日期显示"""
        if not date_str or date_str == '未知日期':
            return '未知日期'
        
        try:
            # 尝试解析多种日期格式
            import dateutil.parser
            dt = dateutil.parser.parse(date_str)
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return date_str
    
    def add_subscription(self, name: str, url: str) -> bool:
        """添加新的订阅源"""
        # 验证 URL 格式
        if not self.validate_url(url):
            print("❌ 无效的 URL 格式")
            return False
        
        try:
            # 验证 RSS 链接是否有效
            print(f"🔍 正在验证 RSS 链接: {url}")
            response = requests.get(url, timeout=15, headers=self.headers)
            response.raise_for_status()
            
            # 尝试解析 RSS 内容
            feed = feedparser.parse(response.content)
            if not hasattr(feed, 'entries') or not feed.entries:
                print("⚠️  该链接似乎不是有效的 RSS 源或暂无内容")
                return False
            
            # 获取 RSS 源的标题（如果用户没有自定义名称）
            feed_title = feed.feed.get('title', name).strip()
            if not name.strip():
                name = feed_title or url
            
            # 检查是否已存在
            if name in self.subscriptions:
                print(f"⚠️  订阅源 '{name}' 已存在，将更新其 URL")
            
            self.subscriptions[name] = url
            self.save_subscriptions()
            print(f"✅ 成功添加订阅源: {name}")
            print(f"   📊 包含 {len(feed.entries)} 篇文章")
            return True
            
        except requests.exceptions.Timeout:
            print("❌ 请求超时，请检查网络连接或稍后重试")
            return False
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
            # 同时清理缓存
            if name in self.cache:
                del self.cache[name]
                self.save_cache()
            self.save_subscriptions()
            print(f"🗑️  已删除订阅源: {name}")
            return True
        else:
            print(f"❌ 未找到订阅源: {name}")
            return False
    
    def list_subscriptions(self):
        """列出所有订阅源及其状态"""
        if not self.subscriptions:
            print("📭 暂无订阅源，请先添加一些订阅")
            return
        
        print(f"\n📚 当前订阅源列表 (共 {len(self.subscriptions)} 个):")
        print("-" * 60)
        for i, (name, url) in enumerate(self.subscriptions.items(), 1):
            print(f"[{i}] {name}")
            print(f"    🔗 {url}")
            
            # 显示缓存状态
            if name in self.cache:
                cache_time = self.cache[name].get('last_update', '未知')
                cache_count = len(self.cache[name].get('articles', []))
                print(f"    💾 缓存: {cache_count} 篇文章 (更新时间: {cache_time})")
            else:
                print(f"    💾 缓存: 无")
                
        print("-" * 60)
    
    def fetch_articles(self, url: str, limit: int = 10, use_cache: bool = True) -> List[Dict]:
        """获取指定 RSS 源的文章列表"""
        try:
            print(f"📡 正在获取最新文章...")
            
            response = requests.get(url, timeout=15, headers=self.headers)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            articles = []
            
            for entry in feed.entries[:limit]:
                # 处理发布日期
                published = entry.get('published', entry.get('updated', '未知日期'))
                
                article = {
                    'title': entry.get('title', '无标题'),
                    'link': entry.get('link', ''),
                    'summary': self.clean_html(entry.get('summary', entry.get('description', '无摘要'))),
                    'published': self.format_date(published),
                    'author': entry.get('author', ''),
                    'categories': [cat.get('term', '') for cat in entry.get('tags', [])]
                }
                articles.append(article)
            
            # 更新缓存
            if use_cache:
                subscription_name = None
                for name, sub_url in self.subscriptions.items():
                    if sub_url == url:
                        subscription_name = name
                        break
                
                if subscription_name:
                    self.cache[subscription_name] = {
                        'articles': articles,
                        'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    self.save_cache()
            
            return articles
            
        except requests.exceptions.Timeout:
            print("❌ 请求超时，请检查网络连接")
            return []
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求失败: {e}")
            return []
        except Exception as e:
            print(f"❌ 解析失败: {e}")
            return []
    
    def display_articles(self, articles: List[Dict], show_summary: bool = True):
        """展示文章列表"""
        if not articles:
            print("📭 暂无文章")
            return
        
        print(f"\n📰 最新文章 (共 {len(articles)} 篇):")
        print("=" * 80)
        
        for i, article in enumerate(articles, 1):
            print(f"\n[{i}] {article['title']}")
            print(f"📅 {article['published']}")
            
            if article.get('author'):
                print(f"👤 {article['author']}")
            
            if article.get('categories'):
                categories = ', '.join(article['categories'][:3])  # 最多显示3个分类
                print(f"🏷️  {categories}")
            
            if show_summary:
                summary = article['summary']
                if len(summary) > 300:
                    summary = summary[:300] + "..."
                print(f"📝 {summary}")
            
            print(f"🔗 {article['link']}")
            print("-" * 80)
    
    def search_articles(self, keyword: str, articles: List[Dict]) -> List[Dict]:
        """在文章中搜索关键词"""
        if not keyword.strip():
            return articles
        
        keyword = keyword.lower()
        filtered_articles = []
        
        for article in articles:
            title_match = keyword in article['title'].lower()
            summary_match = keyword in article['summary'].lower()
            
            if title_match or summary_match:
                filtered_articles.append(article)
        
        return filtered_articles
    
    def export_articles(self, articles: List[Dict], filename: str = None):
        """导出文章到 Markdown 文件"""
        if not articles:
            print("❌ 没有文章可导出")
            return
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"rss_articles_{timestamp}.md"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# RSS 文章导出\\n\\n")
                f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
                f.write(f"共 {len(articles)} 篇文章\\n\\n")
                f.write("---\\n\\n")
                
                for i, article in enumerate(articles, 1):
                    f.write(f"## {i}. {article['title']}\\n\\n")
                    f.write(f"**发布时间:** {article['published']}\\n\\n")
                    
                    if article.get('author'):
                        f.write(f"**作者:** {article['author']}\\n\\n")
                    
                    if article.get('categories'):
                        categories = ', '.join(article['categories'])
                        f.write(f"**分类:** {categories}\\n\\n")
                    
                    f.write(f"**摘要:** {article['summary']}\\n\\n")
                    f.write(f"**原文链接:** [{article['link']}]({article['link']})\\n\\n")
                    f.write("---\\n\\n")
            
            print(f"✅ 文章已导出到: {filename}")
            
        except Exception as e:
            print(f"❌ 导出失败: {e}")
    
    def read_feed(self, subscription_name: str):
        """阅读指定订阅源的文章"""
        if subscription_name not in self.subscriptions:
            print(f"❌ 未找到订阅源: {subscription_name}")
            return
        
        url = self.subscriptions[subscription_name]
        print(f"\\n📖 正在阅读: {subscription_name}")
        
        articles = self.fetch_articles(url)
        if not articles:
            return
        
        current_articles = articles.copy()
        
        while True:
            self.display_articles(current_articles)
            
            print("\\n🔧 操作选项:")
            print(f"  [1-{len(current_articles)}] 在浏览器中打开对应文章")
            print("  [r] 刷新文章列表")
            print("  [s] 搜索文章")
            print("  [e] 导出文章到 Markdown")
            print("  [c] 清空屏幕")
            print("  [b] 返回主菜单")
            
            choice = input("\\n请选择操作: ").strip().lower()
            
            if choice == 'b':
                break
            elif choice == 'r':
                print("\\n🔄 刷新中...")
                articles = self.fetch_articles(url)
                if articles:
                    current_articles = articles.copy()
                else:
                    print("❌ 刷新失败")
            elif choice == 's':
                keyword = input("请输入搜索关键词: ").strip()
                if keyword:
                    filtered = self.search_articles(keyword, articles)
                    if filtered:
                        current_articles = filtered
                        print(f"🔍 找到 {len(filtered)} 篇相关文章")
                    else:
                        print("❌ 没有找到相关文章")
                        current_articles = articles
                else:
                    current_articles = articles
                    print("🔄 显示全部文章")
            elif choice == 'e':
                self.export_articles(current_articles)
            elif choice == 'c':
                os.system('clear' if os.name == 'posix' else 'cls')
            elif choice.isdigit():
                article_num = int(choice)
                if 1 <= article_num <= len(current_articles):
                    article = current_articles[article_num - 1]
                    print(f"🌐 正在打开: {article['title']}")
                    webbrowser.open(article['link'])
                else:
                    print("❌ 无效的文章编号")
            else:
                print("❌ 无效的选择，请重新输入")
    
    def batch_update(self):
        """批量更新所有订阅源"""
        if not self.subscriptions:
            print("📭 暂无订阅源")
            return
        
        print(f"🔄 开始批量更新 {len(self.subscriptions)} 个订阅源...")
        
        updated_count = 0
        failed_feeds = []
        
        for i, (name, url) in enumerate(self.subscriptions.items(), 1):
            print(f"\\n[{i}/{len(self.subscriptions)}] 更新: {name}")
            articles = self.fetch_articles(url, limit=5, use_cache=True)
            
            if articles:
                updated_count += 1
                print(f"✅ 获取到 {len(articles)} 篇文章")
            else:
                failed_feeds.append(name)
                print(f"❌ 更新失败")
            
            # 避免请求过于频繁
            time.sleep(1)
        
        print(f"\\n📊 批量更新完成!")
        print(f"✅ 成功更新: {updated_count} 个")
        print(f"❌ 更新失败: {len(failed_feeds)} 个")
        
        if failed_feeds:
            print("失败的订阅源:")
            for feed in failed_feeds:
                print(f"  • {feed}")
    
    def main_menu(self):
        """主菜单"""
        print("\\n🎉 欢迎使用 RSS 终端阅读器 (增强版)!")
        
        while True:
            print("\\n" + "=" * 60)
            print("📱 主菜单")
            print("=" * 60)
            print("[1] 查看订阅源列表")
            print("[2] 添加订阅源")
            print("[3] 删除订阅源")
            print("[4] 阅读订阅")
            print("[5] 批量更新所有订阅")
            print("[6] 清理缓存")
            print("[7] 退出程序")
            print("=" * 60)
            
            choice = input("请选择操作 (1-7): ").strip()
            
            if choice == '1':
                self.list_subscriptions()
                
            elif choice == '2':
                print("\\n➕ 添加新订阅源")
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
                name = input("\\n请输入要删除的订阅源名称: ").strip()
                self.remove_subscription(name)
                
            elif choice == '4':
                if not self.subscriptions:
                    print("📭 暂无订阅源，请先添加一些订阅")
                    continue
                
                self.list_subscriptions()
                print("\\n📖 选择要阅读的订阅源:")
                
                subscription_list = list(self.subscriptions.keys())
                choice_input = input("请输入订阅源编号或名称: ").strip()
                
                if choice_input.isdigit():
                    sub_num = int(choice_input)
                    if 1 <= sub_num <= len(subscription_list):
                        subscription_name = subscription_list[sub_num - 1]
                        self.read_feed(subscription_name)
                    else:
                        print("❌ 无效的编号")
                else:
                    if choice_input in self.subscriptions:
                        self.read_feed(choice_input)
                    else:
                        print("❌ 未找到该订阅源")
            
            elif choice == '5':
                self.batch_update()
            
            elif choice == '6':
                if os.path.exists(self.cache_file):
                    os.remove(self.cache_file)
                    self.cache = {}
                    print("🗑️  缓存已清理")
                else:
                    print("💡 暂无缓存文件")
            
            elif choice == '7':
                print("👋 感谢使用，再见!")
                sys.exit(0)
                
            else:
                print("❌ 无效的选择，请输入 1-7")


def main():
    """主函数"""
    try:
        reader = RSSReaderEnhanced()
        reader.main_menu()
    except KeyboardInterrupt:
        print("\\n\\n👋 程序被用户中断，再见!")
        sys.exit(0)
    except Exception as e:
        print(f"\\n❌ 程序运行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
