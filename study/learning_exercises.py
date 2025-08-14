# -*- coding: utf-8 -*-
"""
RSS 阅读器 - Python 学习练习
基于原项目的扩展练习，帮助掌握 Python 核心概念
"""

import json
import requests
import feedparser
from datetime import datetime
from typing import List, Dict
import re

class RSSReaderLearning:
    """
    扩展练习版本的 RSS 阅读器
    用于学习 Python 编程概念
    """
    
    def __init__(self):
        self.config_file = "rss_subscriptions.json"
        self.favorites_file = "rss_favorites.json"
        self.history_file = "search_history.json"
        
        self.subscriptions = {}
        self.favorites = []
        self.search_history = []
        
        self.load_subscriptions()
        self.load_favorites()
        self.load_search_history()
    
    # 练习1：添加收藏功能
    def add_to_favorites(self, article: Dict) -> bool:
        """
        学习要点：
        - 字典操作和列表操作
        - 数据去重逻辑
        - 文件持久化
        """
        try:
            # 检查是否已收藏
            for fav in self.favorites:
                if fav['link'] == article['link']:
                    print("⚠️  文章已在收藏夹中")
                    return False
            
            # 添加收藏时间
            article['favorited_at'] = datetime.now().isoformat()
            self.favorites.append(article)
            self.save_favorites()
            print("⭐ 文章已添加到收藏夹")
            return True
            
        except Exception as e:
            print(f"❌ 收藏失败: {e}")
            return False
    
    def save_favorites(self):
        """保存收藏到文件"""
        try:
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(self.favorites, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  收藏保存失败: {e}")
    
    def load_favorites(self):
        """从文件加载收藏"""
        try:
            with open(self.favorites_file, 'r', encoding='utf-8') as f:
                self.favorites = json.load(f)
        except FileNotFoundError:
            self.favorites = []
        except Exception as e:
            print(f"⚠️  收藏加载失败: {e}")
            self.favorites = []
    
    # 练习2：搜索历史功能
    def add_to_search_history(self, keyword: str):
        """
        学习要点：
        - 列表操作（去重、限制长度）
        - 数据结构设计
        """
        try:
            # 如果关键词已存在，先移除
            if keyword in self.search_history:
                self.search_history.remove(keyword)
            
            # 添加到开头
            self.search_history.insert(0, keyword)
            
            # 限制历史记录数量
            if len(self.search_history) > 10:
                self.search_history = self.search_history[:10]
            
            self.save_search_history()
            
        except Exception as e:
            print(f"⚠️  搜索历史保存失败: {e}")
    
    def save_search_history(self):
        """保存搜索历史"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.search_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  搜索历史保存失败: {e}")
    
    def load_search_history(self):
        """加载搜索历史"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.search_history = json.load(f)
        except FileNotFoundError:
            self.search_history = []
        except Exception as e:
            print(f"⚠️  搜索历史加载失败: {e}")
            self.search_history = []
    
    # 练习3：文章统计功能
    def get_statistics(self) -> Dict:
        """
        学习要点：
        - 数据统计和计算
        - 字典操作
        - 列表推导式
        """
        stats = {
            'total_subscriptions': len(self.subscriptions),
            'total_favorites': len(self.favorites),
            'recent_searches': len(self.search_history)
        }
        
        # 统计收藏文章的来源分布（如果有的话）
        if self.favorites:
            sources = {}
            for article in self.favorites:
                # 从链接提取域名
                domain = self.extract_domain(article.get('link', ''))
                sources[domain] = sources.get(domain, 0) + 1
            stats['favorite_sources'] = sources
        
        return stats
    
    def extract_domain(self, url: str) -> str:
        """
        学习要点：
        - 正则表达式
        - 字符串处理
        """
        try:
            import re
            pattern = r'https?://([^/]+)'
            match = re.search(pattern, url)
            return match.group(1) if match else 'unknown'
        except:
            return 'unknown'
    
    # 练习4：高级搜索功能
    def advanced_search(self, articles: List[Dict], **kwargs) -> List[Dict]:
        """
        学习要点：
        - **kwargs 可变关键字参数
        - 复合条件筛选
        - 日期处理
        """
        filtered = articles[:]
        
        # 标题关键词搜索
        if 'title_keyword' in kwargs:
            keyword = kwargs['title_keyword'].lower()
            filtered = [a for a in filtered if keyword in a['title'].lower()]
        
        # 摘要关键词搜索
        if 'summary_keyword' in kwargs:
            keyword = kwargs['summary_keyword'].lower()
            filtered = [a for a in filtered if keyword in a['summary'].lower()]
        
        # 日期范围搜索（这里简化处理）
        if 'date_from' in kwargs:
            # 实际应用中需要解析日期字符串
            pass
        
        return filtered
    
    # 练习5：文章导出功能
    def export_articles(self, articles: List[Dict], format: str = 'markdown') -> str:
        """
        学习要点：
        - 文件格式处理
        - 字符串模板
        - 条件分支
        """
        if format.lower() == 'markdown':
            return self.export_to_markdown(articles)
        elif format.lower() == 'html':
            return self.export_to_html(articles)
        else:
            raise ValueError(f"不支持的格式: {format}")
    
    def export_to_markdown(self, articles: List[Dict]) -> str:
        """导出为 Markdown 格式"""
        md_content = "# RSS 文章导出\n\n"
        md_content += f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for i, article in enumerate(articles, 1):
            md_content += f"## {i}. {article['title']}\n\n"
            md_content += f"**链接**: {article['link']}\n\n"
            md_content += f"**发布时间**: {article.get('published', '未知')}\n\n"
            md_content += f"**摘要**: {article.get('summary', '无摘要')}\n\n"
            md_content += "---\n\n"
        
        return md_content
    
    def export_to_html(self, articles: List[Dict]) -> str:
        """导出为 HTML 格式"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>RSS 文章导出</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .article { border-bottom: 1px solid #ccc; padding: 20px 0; }
                .title { color: #333; font-size: 18px; font-weight: bold; }
                .link { color: #0066cc; }
                .date { color: #666; font-size: 14px; }
                .summary { margin-top: 10px; }
            </style>
        </head>
        <body>
            <h1>RSS 文章导出</h1>
        """
        
        for article in articles:
            html_content += f"""
            <div class="article">
                <div class="title">{article['title']}</div>
                <div class="date">发布时间: {article.get('published', '未知')}</div>
                <div class="link"><a href="{article['link']}" target="_blank">查看原文</a></div>
                <div class="summary">{article.get('summary', '无摘要')}</div>
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        return html_content
    
    # 从原项目继承的基础方法
    def load_subscriptions(self):
        """加载订阅源"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.subscriptions = json.load(f)
        except FileNotFoundError:
            self.subscriptions = {}
        except Exception as e:
            print(f"⚠️  配置加载失败: {e}")
            self.subscriptions = {}


def main():
    """
    主函数 - 演示各种功能
    学习要点：
    - 程序入口点设计
    - 用户交互流程
    """
    reader = RSSReaderLearning()
    
    print("🎓 RSS 阅读器 - Python 学习版")
    print("=" * 40)
    
    # 显示统计信息
    stats = reader.get_statistics()
    print(f"📊 统计信息:")
    print(f"   订阅源数量: {stats['total_subscriptions']}")
    print(f"   收藏文章: {stats['total_favorites']}")
    print(f"   搜索历史: {stats['recent_searches']}")
    
    # 显示搜索历史
    if reader.search_history:
        print(f"\n🔍 最近搜索: {', '.join(reader.search_history[:5])}")


if __name__ == "__main__":
    main()
