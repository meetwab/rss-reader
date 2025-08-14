#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS项目练习题参考答案
包含各个难度级别的练习题解答
"""

import json
import os
import requests
import feedparser
from datetime import datetime
from typing import List, Dict, Optional, Set
import re
import time


# ============================================================================
# 🟢 初级练习答案
# ============================================================================

class EnhancedRSSReader:
    """增强版RSS阅读器 - 包含练习题解答"""
    
    def __init__(self):
        self.config_file = "rss_subscriptions.json"
        self.subscriptions = {}
        self.load_subscriptions()
    
    # 练习1答案：修改界面文字
    def custom_messages(self):
        """自定义提示信息样式"""
        messages = {
            'success_add': "🎉 太棒了！新的RSS源已经添加成功！",
            'loading': "⏳ 正在努力获取最新内容，请稍候...",
            'error': "😱 糟糕！出现了一些问题",
            'welcome': "🌟 欢迎使用超级RSS阅读器！",
            'goodbye': "👋 感谢使用，期待下次见面！"
        }
        return messages
    
    def show_welcome(self):
        """显示欢迎信息"""
        print("=" * 60)
        print("🌟 欢迎使用超级RSS阅读器！")
        print("📖 您的个人信息管家")
        print("=" * 60)
    
    # 练习2答案：添加统计功能
    def enhanced_main_menu(self):
        """增强版主菜单 - 包含统计信息"""
        print("\n" + "=" * 50)
        print("📊 当前状态统计:")
        print(f"   📚 订阅源数量: {len(self.subscriptions)}")
        print(f"   📅 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if self.subscriptions:
            # 计算订阅源的平均名称长度（示例统计）
            avg_name_length = sum(len(name) for name in self.subscriptions.keys()) / len(self.subscriptions)
            print(f"   📐 订阅源平均名称长度: {avg_name_length:.1f} 字符")
        print("=" * 50)
        
        print("\n🎯 请选择操作:")
        print("1. 📋 查看所有订阅源")
        print("2. ➕ 添加新订阅源")
        print("3. ❌ 删除订阅源") 
        print("4. 📖 阅读指定订阅源")
        print("5. 📈 查看详细统计")
        print("0. 👋 退出程序")
    
    def show_detailed_statistics(self):
        """显示详细统计信息"""
        if not self.subscriptions:
            print("📭 暂无订阅源，无法显示统计信息")
            return
        
        print("\n📈 详细统计信息:")
        print("-" * 40)
        
        # 基本统计
        total_feeds = len(self.subscriptions)
        print(f"📚 总订阅源数量: {total_feeds}")
        
        # 域名统计
        domains = {}
        for url in self.subscriptions.values():
            domain = self.extract_domain(url)
            domains[domain] = domains.get(domain, 0) + 1
        
        print(f"🌐 涉及域名数量: {len(domains)}")
        print("🏆 热门域名排行:")
        for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {domain}: {count} 个订阅源")
        
        # 名称长度统计
        name_lengths = [len(name) for name in self.subscriptions.keys()]
        if name_lengths:
            print(f"📏 订阅源名称长度 - 最长: {max(name_lengths)}, 最短: {min(name_lengths)}")
    
    def extract_domain(self, url: str) -> str:
        """从URL提取域名"""
        import re
        pattern = r'https?://([^/]+)'
        match = re.search(pattern, url)
        return match.group(1) if match else 'unknown'


# 练习3答案：简化版RSS阅读器
class SimpleRSS:
    """简化版RSS阅读器"""
    
    def __init__(self):
        self.feeds = {}
        print("🎯 简化版RSS阅读器已启动！")
    
    def add_feed(self, name: str, url: str) -> bool:
        """添加RSS源"""
        if not name or not url:
            print("❌ 名称和URL都不能为空")
            return False
        
        # 简单的URL验证
        if not (url.startswith('http://') or url.startswith('https://')):
            print("❌ URL格式不正确，必须以http://或https://开头")
            return False
        
        self.feeds[name] = url
        print(f"✅ 添加成功: {name}")
        return True
    
    def list_feeds(self):
        """列出所有RSS源"""
        if not self.feeds:
            print("📭 还没有添加任何RSS源")
            return
        
        print("\n📚 当前RSS源列表:")
        print("-" * 30)
        for i, (name, url) in enumerate(self.feeds.items(), 1):
            print(f"{i}. {name}")
            print(f"   🔗 {url}")
        print("-" * 30)
    
    def read_feed(self, name: str):
        """阅读指定RSS源"""
        if name not in self.feeds:
            print(f"❌ 未找到RSS源: {name}")
            return
        
        url = self.feeds[name]
        print(f"📖 正在读取: {name}")
        
        try:
            # 简化的文章获取
            response = requests.get(url, timeout=10)
            feed = feedparser.parse(response.content)
            
            if not feed.entries:
                print("📭 该RSS源暂无文章")
                return
            
            print(f"\n📰 最新文章 (显示前3篇):")
            for i, entry in enumerate(feed.entries[:3], 1):
                title = entry.get('title', '无标题')
                link = entry.get('link', '无链接')
                print(f"\n{i}. {title}")
                print(f"   🔗 {link}")
                
        except Exception as e:
            print(f"❌ 读取失败: {e}")
    
    def simple_menu(self):
        """简单的菜单系统"""
        while True:
            print("\n🎯 简化版RSS阅读器")
            print("1. 添加RSS源")
            print("2. 查看RSS源列表") 
            print("3. 阅读RSS源")
            print("0. 退出")
            
            choice = input("\n请选择 (0-3): ").strip()
            
            if choice == '0':
                print("👋 再见！")
                break
            elif choice == '1':
                name = input("请输入RSS源名称: ").strip()
                url = input("请输入RSS源URL: ").strip()
                self.add_feed(name, url)
            elif choice == '2':
                self.list_feeds()
            elif choice == '3':
                if not self.feeds:
                    print("📭 请先添加RSS源")
                    continue
                self.list_feeds()
                name = input("请输入要阅读的RSS源名称: ").strip()
                self.read_feed(name)
            else:
                print("❌ 无效选择")


# ============================================================================
# 🟡 中级练习答案
# ============================================================================

class IntermediateRSSReader(EnhancedRSSReader):
    """中级功能RSS阅读器"""
    
    def __init__(self):
        super().__init__()
        self.backup_dir = "rss_backups"
        self.create_backup_directory()
    
    def create_backup_directory(self):
        """创建备份目录"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    # 练习4答案：配置备份功能
    def backup_config(self) -> str:
        """创建配置文件备份"""
        try:
            if not os.path.exists(self.config_file):
                print("⚠️  配置文件不存在，无法备份")
                return ""
            
            # 生成带时间戳的备份文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"rss_config_backup_{timestamp}.json"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # 复制配置文件
            import shutil
            shutil.copy2(self.config_file, backup_path)
            
            print(f"✅ 配置备份成功: {backup_path}")
            return backup_path
            
        except Exception as e:
            print(f"❌ 备份失败: {e}")
            return ""
    
    def restore_config(self, backup_file: str) -> bool:
        """从备份恢复配置"""
        try:
            if not os.path.exists(backup_file):
                print(f"❌ 备份文件不存在: {backup_file}")
                return False
            
            # 备份当前配置
            if os.path.exists(self.config_file):
                current_backup = f"{self.config_file}.before_restore"
                import shutil
                shutil.copy2(self.config_file, current_backup)
                print(f"🔄 当前配置已备份为: {current_backup}")
            
            # 恢复配置
            import shutil
            shutil.copy2(backup_file, self.config_file)
            
            # 重新加载配置
            self.load_subscriptions()
            
            print("✅ 配置恢复成功")
            return True
            
        except Exception as e:
            print(f"❌ 恢复失败: {e}")
            return False
    
    def list_backups(self):
        """列出所有备份文件"""
        try:
            backup_files = [f for f in os.listdir(self.backup_dir) 
                           if f.startswith('rss_config_backup_') and f.endswith('.json')]
            
            if not backup_files:
                print("📭 暂无备份文件")
                return
            
            backup_files.sort(reverse=True)  # 最新的在前
            
            print("📋 可用备份文件:")
            for i, backup_file in enumerate(backup_files, 1):
                # 从文件名提取时间戳
                timestamp = backup_file.replace('rss_config_backup_', '').replace('.json', '')
                formatted_time = datetime.strptime(timestamp, '%Y%m%d_%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
                print(f"{i}. {backup_file} (创建时间: {formatted_time})")
                
        except Exception as e:
            print(f"❌ 列出备份文件失败: {e}")
    
    # 练习5答案：文章搜索功能
    def search_articles(self, keyword: str) -> List[Dict]:
        """在所有文章中搜索关键词"""
        if not keyword:
            print("❌ 搜索关键词不能为空")
            return []
        
        print(f"🔍 正在搜索包含 '{keyword}' 的文章...")
        results = []
        
        for feed_name, feed_url in self.subscriptions.items():
            try:
                print(f"   搜索中: {feed_name}")
                articles = self.fetch_articles(feed_url, limit=20)  # 获取更多文章用于搜索
                
                for article in articles:
                    # 在标题和摘要中搜索关键词（不区分大小写）
                    title_match = keyword.lower() in article['title'].lower()
                    summary_match = keyword.lower() in article.get('summary', '').lower()
                    
                    if title_match or summary_match:
                        article['source'] = feed_name  # 添加来源信息
                        results.append(article)
                        
            except Exception as e:
                print(f"   ⚠️  搜索 {feed_name} 时出错: {e}")
                continue
        
        print(f"✅ 搜索完成，找到 {len(results)} 篇相关文章")
        return results
    
    def display_search_results(self, results: List[Dict]):
        """显示搜索结果"""
        if not results:
            print("📭 没有找到匹配的文章")
            return
        
        print(f"\n🎯 搜索结果 (共 {len(results)} 篇):")
        print("=" * 60)
        
        for i, article in enumerate(results, 1):
            print(f"\n[{i}] {article['title']}")
            print(f"📰 来源: {article.get('source', '未知')}")
            print(f"📅 发布: {article.get('published', '未知时间')}")
            
            # 显示摘要的前100个字符
            summary = article.get('summary', '无摘要')
            if len(summary) > 100:
                summary = summary[:100] + "..."
            print(f"📝 摘要: {summary}")
            print(f"🔗 链接: {article['link']}")
            print("-" * 60)
    
    # 练习6答案：文章去重功能  
    def remove_duplicate_articles(self, articles: List[Dict]) -> List[Dict]:
        """去除重复的文章"""
        if not articles:
            return []
        
        seen_links = set()
        unique_articles = []
        duplicates_count = 0
        
        for article in articles:
            link = article.get('link', '')
            if link and link not in seen_links:
                seen_links.add(link)
                unique_articles.append(article)
            else:
                duplicates_count += 1
        
        if duplicates_count > 0:
            print(f"🔄 已去除 {duplicates_count} 篇重复文章")
        
        return unique_articles
    
    def fetch_articles(self, url: str, limit: int = 5) -> List[Dict]:
        """获取文章并自动去重"""
        try:
            print(f"📡 正在获取最新文章...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            articles = []
            
            for entry in feed.entries[:limit * 2]:  # 获取更多文章，然后去重
                article = {
                    'title': entry.get('title', '无标题'),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', entry.get('description', '无摘要')),
                    'published': entry.get('published', '未知日期')
                }
                articles.append(article)
            
            # 自动去重
            unique_articles = self.remove_duplicate_articles(articles)
            
            # 限制返回数量
            return unique_articles[:limit]
            
        except Exception as e:
            print(f"❌ 获取文章失败: {e}")
            return []
    
    def load_subscriptions(self):
        """加载订阅配置"""
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
        """保存订阅配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.subscriptions, f, ensure_ascii=False, indent=2)
            print("💾 订阅源配置已保存")
        except Exception as e:
            print(f"❌ 保存失败: {e}")


# ============================================================================  
# 🔴 高级练习答案
# ============================================================================

# 练习8答案：文章分类系统
class ArticleClassifier:
    """文章分类器"""
    
    def __init__(self):
        self.categories = {
            '技术': ['python', 'programming', 'code', 'development', 'software', 'tech', '编程', '开发', '技术'],
            '新闻': ['news', 'breaking', 'report', 'update', '新闻', '报道', '更新'],
            '生活': ['life', 'lifestyle', 'health', 'food', 'travel', '生活', '健康', '美食', '旅行'],
            '商业': ['business', 'finance', 'economy', 'market', 'money', '商业', '金融', '经济', '市场'],
            '科学': ['science', 'research', 'study', 'discovery', '科学', '研究', '发现'],
            '娱乐': ['entertainment', 'movie', 'music', 'game', '娱乐', '电影', '音乐', '游戏']
        }
    
    def classify_article(self, article: Dict) -> str:
        """对文章进行分类"""
        title = article.get('title', '').lower()
        summary = article.get('summary', '').lower()
        content = (title + ' ' + summary).lower()
        
        category_scores = {}
        
        # 计算每个分类的匹配得分
        for category, keywords in self.categories.items():
            score = 0
            for keyword in keywords:
                # 标题中的关键词权重更高
                if keyword in title:
                    score += 3
                if keyword in summary:
                    score += 1
            category_scores[category] = score
        
        # 找到得分最高的分类
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            if category_scores[best_category] > 0:
                return best_category
        
        return '其他'  # 默认分类
    
    def classify_articles(self, articles: List[Dict]) -> Dict[str, List[Dict]]:
        """对文章列表进行分类"""
        classified = {}
        
        for article in articles:
            category = self.classify_article(article)
            if category not in classified:
                classified[category] = []
            classified[category].append(article)
        
        return classified
    
    def display_classified_articles(self, classified_articles: Dict[str, List[Dict]]):
        """显示分类后的文章"""
        for category, articles in classified_articles.items():
            if articles:  # 只显示非空分类
                print(f"\n📂 {category} ({len(articles)} 篇):")
                print("-" * 30)
                for i, article in enumerate(articles[:3], 1):  # 每个分类最多显示3篇
                    print(f"{i}. {article['title']}")


class AdvancedRSSReader(IntermediateRSSReader):
    """高级功能RSS阅读器"""
    
    def __init__(self):
        super().__init__()
        self.classifier = ArticleClassifier()
        self.reading_history = []
    
    def get_classified_articles(self, feed_name: str = None):
        """获取分类后的文章"""
        all_articles = []
        
        if feed_name and feed_name in self.subscriptions:
            # 获取指定订阅源的文章
            url = self.subscriptions[feed_name]
            articles = self.fetch_articles(url, limit=10)
            all_articles.extend(articles)
        else:
            # 获取所有订阅源的文章
            for name, url in self.subscriptions.items():
                try:
                    articles = self.fetch_articles(url, limit=5)
                    for article in articles:
                        article['source'] = name
                    all_articles.extend(articles)
                except Exception as e:
                    print(f"⚠️  获取 {name} 的文章失败: {e}")
        
        # 去重
        unique_articles = self.remove_duplicate_articles(all_articles)
        
        # 分类
        classified = self.classifier.classify_articles(unique_articles)
        
        return classified
    
    def show_classified_articles(self):
        """显示分类后的文章"""
        print("🔄 正在获取和分类文章...")
        classified = self.get_classified_articles()
        
        if not any(classified.values()):
            print("📭 没有找到任何文章")
            return
        
        print("\n🏷️  文章分类结果:")
        print("=" * 50)
        
        self.classifier.display_classified_articles(classified)
        
        # 显示分类统计
        print(f"\n📊 分类统计:")
        for category, articles in classified.items():
            if articles:
                print(f"   {category}: {len(articles)} 篇")


# ============================================================================
# 🚀 示例用法和测试
# ============================================================================

def test_simple_rss():
    """测试简化版RSS阅读器"""
    print("🧪 测试简化版RSS阅读器")
    print("=" * 40)
    
    rss = SimpleRSS()
    
    # 添加测试数据
    rss.add_feed("Python官网", "https://www.python.org/news/")
    rss.add_feed("GitHub博客", "https://github.blog/feed/")
    
    # 显示列表
    rss.list_feeds()
    
    print("\n🧪 测试完成")

def test_intermediate_features():
    """测试中级功能"""
    print("🧪 测试中级功能")
    print("=" * 40)
    
    reader = IntermediateRSSReader()
    
    # 测试备份功能
    print("\n1. 测试备份功能:")
    backup_path = reader.backup_config()
    
    if backup_path:
        reader.list_backups()
    
    # 测试搜索功能（需要有订阅源才能测试）
    if reader.subscriptions:
        print("\n2. 测试搜索功能:")
        results = reader.search_articles("python")
        reader.display_search_results(results[:3])  # 只显示前3个结果
    
    print("\n🧪 中级功能测试完成")

def test_advanced_features():
    """测试高级功能"""
    print("🧪 测试高级功能")
    print("=" * 40)
    
    reader = AdvancedRSSReader()
    
    # 测试文章分类
    if reader.subscriptions:
        print("测试文章自动分类功能:")
        reader.show_classified_articles()
    else:
        print("⚠️  需要先添加订阅源才能测试分类功能")
    
    print("\n🧪 高级功能测试完成")

def main():
    """主函数 - 演示所有功能"""
    print("🎓 RSS项目练习题答案演示")
    print("=" * 60)
    
    while True:
        print("\n📚 请选择要测试的功能:")
        print("1. 🟢 初级练习 - 简化版RSS阅读器")
        print("2. 🟡 中级练习 - 备份和搜索功能")
        print("3. 🔴 高级练习 - 文章分类系统")
        print("4. 📊 统计功能演示")
        print("0. 退出")
        
        choice = input("\n请选择 (0-4): ").strip()
        
        if choice == '0':
            print("👋 再见！")
            break
        elif choice == '1':
            test_simple_rss()
        elif choice == '2':
            test_intermediate_features()
        elif choice == '3':
            test_advanced_features()
        elif choice == '4':
            reader = EnhancedRSSReader()
            reader.show_detailed_statistics()
        else:
            print("❌ 无效选择")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()
