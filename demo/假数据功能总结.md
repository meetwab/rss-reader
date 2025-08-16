#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS 阅读器假数据生成器
生成测试订阅和历史文章数据，方便测试各种功能
"""

import json
import os
import sys
from datetime import datetime, timedelta
import random

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from demo_refactored import FileHandler, RssParser

class FakeDataGenerator:
    """假数据生成器"""
    
    def __init__(self):
        self.file_handler = FileHandler()
        self.rss_parser = RssParser()
        
        # 预定义的假数据模板
        self.fake_blogs = [
            {
                "name": "科技前沿观察",
                "url": "https://tech-observer.com/rss",
                "topics": ["人工智能", "机器学习", "区块链", "云计算", "物联网", "5G 技术"]
            },
            {
                "name": "编程技术分享",
                "url": "https://coding-share.dev/rss", 
                "topics": ["Python", "JavaScript", "React", "Vue", "Node.js", "Docker"]
            },
            {
                "name": "数据科学日报",
                "url": "https://data-science-daily.com/rss",
                "topics": ["数据分析", "机器学习", "深度学习", "统计学", "数据可视化", "大数据"]
            },
            {
                "name": "创业投资资讯",
                "url": "https://startup-news.biz/rss",
                "topics": ["创业故事", "风险投资", "商业模式", "市场分析", "行业趋势", "融资新闻"]
            },
            {
                "name": "生活方式博客",
                "url": "https://lifestyle-blog.life/rss",
                "topics": ["健康生活", "美食烹饪", "旅行攻略", "家居装饰", "时尚搭配", "运动健身"]
            }
        ]
        
        # 文章标题模板
        self.title_templates = [
            "{topic}的最新发展趋势分析",
            "深入理解{topic}：从入门到精通",
            "2025 年{topic}技术栈完整指南",
            "{topic}实战案例分享与思考",
            "如何在{topic}领域获得突破",
            "关于{topic}你需要知道的 10 件事",
            "{topic}性能优化的最佳实践",
            "探索{topic}的未来发展方向",
            "{topic}常见问题解决方案",
            "从零开始学习{topic}的完整路线"
        ]
        
        # 摘要模板
        self.summary_templates = [
            "本文深入探讨了{topic}的核心概念和实际应用，通过详细的案例分析帮助读者理解相关技术原理。文章内容涵盖了基础知识、实践经验和未来发展趋势。",
            "这篇文章分享了作者在{topic}方面的实战经验，包括遇到的挑战、解决方案和最佳实践。适合有一定基础的读者进一步提升技能。",
            "文章从{topic}的历史发展讲起，分析了当前的技术现状和市场应用情况，并对未来的发展方向进行了预测和展望。",
            "作者通过具体的项目案例，详细介绍了{topic}在实际工作中的应用方法和注意事项，提供了很多实用的技巧和建议。",
            "这是一篇{topic}的入门指南，从基础概念开始，逐步深入到高级应用，适合初学者系统学习和掌握相关知识。"
        ]

    def generate_subscriptions(self, filename: str = "subscriptions.json", count: int = None):
        """
        生成假的订阅数据
        
        Args:
            filename: 保存文件名
            count: 生成订阅数量，默认使用全部预定义博客
        """
        print(f"🔨 生成假订阅数据...")
        
        if count is None:
            blogs_to_use = self.fake_blogs
        else:
            blogs_to_use = random.sample(self.fake_blogs, min(count, len(self.fake_blogs)))
        
        subscriptions = {}
        for blog in blogs_to_use:
            subscriptions[blog["name"]] = blog["url"]
        
        success = self.file_handler.save_subscriptions(filename, subscriptions)
        if success:
            print(f"✅ 成功生成 {len(subscriptions)} 个订阅：")
            for name, url in subscriptions.items():
                print(f"  📰 {name} - {url}")
        
        return subscriptions

    def generate_articles_history(self, subscriptions: dict, 
                                 articles_per_subscription: int = 15,
                                 days_range: int = 30):
        """
        生成假的文章历史数据
        
        Args:
            subscriptions: 订阅字典 {name: url}
            articles_per_subscription: 每个订阅生成的文章数量
            days_range: 文章时间范围（天数）
        """
        print(f"\n📚 生成假文章历史数据...")
        
        base_date = datetime.now() - timedelta(days=days_range)
        
        for blog_name, blog_url in subscriptions.items():
            print(f"  生成 {blog_name} 的文章...")
            
            # 找到对应的博客配置
            blog_config = next((blog for blog in self.fake_blogs if blog["name"] == blog_name), None)
            if not blog_config:
                continue
            
            articles = []
            for i in range(articles_per_subscription):
                # 随机选择主题和模板
                topic = random.choice(blog_config["topics"])
                title_template = random.choice(self.title_templates)
                summary_template = random.choice(self.summary_templates)
                
                # 生成文章数据
                article_date = base_date + timedelta(
                    days=random.randint(0, days_range),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                fetch_date = article_date + timedelta(
                    hours=random.randint(0, 2),
                    minutes=random.randint(0, 30)
                )
                
                article = {
                    'title': title_template.format(topic=topic),
                    'link': f"{blog_url.replace('/rss', '')}/article{i+1:03d}",
                    'summary': summary_template.format(topic=topic),
                    'published': article_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    'fetch_time': fetch_date.isoformat()
                }
                articles.append(article)
            
            # 按时间排序（最新的在前）
            articles.sort(key=lambda x: x['published'], reverse=True)
            
            # 保存到历史记录
            self.rss_parser._update_articles_history(blog_url, articles)
            print(f"    ✅ 生成了 {len(articles)} 篇文章")
        
        print(f"📖 文章历史数据生成完成！")

    def generate_sample_data(self, subscription_count: int = 3, 
                           articles_per_subscription: int = 12):
        """
        生成完整的示例数据集
        
        Args:
            subscription_count: 订阅数量
            articles_per_subscription: 每个订阅的文章数量
        """
        print("🎯 开始生成完整的示例数据集")
        print("=" * 50)
        
        # 生成订阅数据
        subscriptions = self.generate_subscriptions(count=subscription_count)
        
        # 生成文章历史数据
        self.generate_articles_history(subscriptions, articles_per_subscription)
        
        print("\n" + "=" * 50)
        print("🎉 示例数据生成完成！")
        print(f"📊 数据统计：")
        print(f"  - 订阅数量：{len(subscriptions)}")
        print(f"  - 每个订阅文章数：{articles_per_subscription}")
        print(f"  - 总文章数：{len(subscriptions) * articles_per_subscription}")
        
        return subscriptions

    def cleanup_data(self):
        """清理生成的测试数据"""
        files_to_clean = ["subscriptions.json", "articles_history.json"]
        cleaned_files = []
        
        for filename in files_to_clean:
            if os.path.exists(filename):
                os.remove(filename)
                cleaned_files.append(filename)
        
        if cleaned_files:
            print(f"🧹 已清理文件：{', '.join(cleaned_files)}")
        else:
            print("📝 没有找到需要清理的文件")

    def show_data_preview(self):
        """显示生成数据的预览"""
        print("\n📋 数据预览")
        print("=" * 50)
        
        # 显示订阅预览
        subscriptions = self.file_handler.load_subscriptions("subscriptions.json")
        if subscriptions:
            print("📰 订阅列表：")
            for i, (name, url) in enumerate(subscriptions.items(), 1):
                print(f"  {i}. {name}")
                print(f"     {url}")
        
        # 显示文章预览
        articles_history = self.file_handler.load_articles_history("articles_history.json")
        if articles_history:
            print(f"\n📚 文章历史 (共 {sum(len(articles) for articles in articles_history.values())} 篇):")
            for url, articles in list(articles_history.items())[:2]:  # 只显示前 2 个订阅的文章
                blog_name = next((name for name, blog_url in subscriptions.items() if blog_url == url), "未知博客")
                print(f"\n  📖 {blog_name} (最近 3 篇):")
                for article in articles[:3]:
                    print(f"    • {article['title']}")
                    print(f"      发布：{article.get('published', 'N/A')}")

def main():
    """主函数"""
    generator = FakeDataGenerator()
    
    print("🎲 RSS 阅读器假数据生成器")
    print("=" * 50)
    
    while True:
        print("\n📋 可用操作：")
        print("1. 生成少量示例数据 (3 个订阅，每个 12 篇文章)")
        print("2. 生成大量测试数据 (5 个订阅，每个 20 篇文章)")
        print("3. 自定义数据生成")
        print("4. 查看当前数据预览")
        print("5. 清理所有测试数据")
        print("0. 退出")
        
        choice = input("\n请选择操作 (0-5): ").strip()
        
        if choice == "1":
            generator.generate_sample_data(subscription_count=3, articles_per_subscription=12)
            generator.show_data_preview()
            
        elif choice == "2":
            generator.generate_sample_data(subscription_count=5, articles_per_subscription=20)
            generator.show_data_preview()
            
        elif choice == "3":
            try:
                sub_count = int(input("请输入订阅数量 (1-5): "))
                article_count = int(input("请输入每个订阅的文章数量 (5-30): "))
                
                if 1 <= sub_count <= 5 and 5 <= article_count <= 30:
                    generator.generate_sample_data(sub_count, article_count)
                    generator.show_data_preview()
                else:
                    print("❌ 输入范围错误，请重新选择")
            except ValueError:
                print("❌ 请输入有效的数字")
                
        elif choice == "4":
            generator.show_data_preview()
            
        elif choice == "5":
            confirm = input("确认清理所有测试数据？(y/n): ").strip().lower()
            if confirm == 'y':
                generator.cleanup_data()
            
        elif choice == "0":
            print("👋 再见！")
            break
            
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()
