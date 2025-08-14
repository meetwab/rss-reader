#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS 阅读器使用示例
演示如何使用 RSSReader 类的各个功能
"""

from rss_reader import RSSReader
import sys

def demo_rss_reader():
    """演示 RSS 阅读器的基本功能"""
    
    print("🎯 RSS 阅读器功能演示")
    print("=" * 50)
    
    # 创建 RSS 阅读器实例
    reader = RSSReader()
    
    # 示例 RSS 源
    demo_feeds = {
        "少数派": "https://sspai.com/feed",
        "阮一峰的网络日志": "http://www.ruanyifeng.com/blog/atom.xml",
        "V2EX": "https://www.v2ex.com/index.xml"
    }
    
    print("\n1️⃣ 添加示例订阅源...")
    for name, url in demo_feeds.items():
        print(f"正在添加: {name}")
        success = reader.add_subscription(name, url)
        if not success:
            print(f"跳过: {name} (可能网络问题)")
            continue
    
    print("\n2️⃣ 查看订阅源列表...")
    reader.list_subscriptions()
    
    print("\n3️⃣ 获取第一个订阅源的文章...")
    if reader.subscriptions:
        first_subscription = list(reader.subscriptions.keys())[0]
        first_url = reader.subscriptions[first_subscription]
        
        print(f"正在获取 {first_subscription} 的文章...")
        articles = reader.fetch_articles(first_url, limit=3)
        
        if articles:
            reader.display_articles(articles)
        else:
            print("❌ 无法获取文章，可能是网络问题")
    
    print("\n4️⃣ 演示完成!")
    print("💡 现在你可以运行 'python rss_reader.py' 来使用完整的交互界面")

if __name__ == "__main__":
    try:
        demo_rss_reader()
    except KeyboardInterrupt:
        print("\n\n👋 演示被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 演示过程中出错: {e}")
        sys.exit(1)
