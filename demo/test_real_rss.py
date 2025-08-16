#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试实际RSS源的文章历史功能
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from demo_refactored import RssParser

def test_real_rss():
    """测试真实的RSS源"""
    print("🧪 测试真实RSS源的文章历史功能")
    print("="*50)
    
    parser = RssParser()
    
    # 使用一个可靠的RSS源进行测试
    test_url = "https://www.v2ex.com/index.xml"
    print(f"📡 测试RSS源: {test_url}")
    
    # 第一次获取文章
    print("\n1️⃣ 第一次获取文章...")
    articles1 = parser.fetch_articles(test_url, count=3)
    print(f"✅ 获取到 {len(articles1)} 篇文章")
    
    if articles1:
        print("📝 文章标题:")
        for i, article in enumerate(articles1, 1):
            print(f"  {i}. {article['title'][:50]}...")
    
    # 获取历史记录
    print("\n2️⃣ 检查历史记录...")
    history1, has_more1, page1, total_pages1 = parser.get_articles_history(test_url, page_size=10, page=1)
    print(f"📚 历史记录中有 {len(history1)} 篇文章")
    print(f"🔄 是否有更多: {has_more1}")
    print(f"📄 当前页: {page1}/{total_pages1}")
    
    # 模拟第二次获取（可能有新文章）
    print("\n3️⃣ 第二次获取文章...")
    articles2 = parser.fetch_articles(test_url, count=5)
    print(f"✅ 获取到 {len(articles2)} 篇文章")
    
    # 再次检查历史记录
    print("\n4️⃣ 检查更新后的历史记录...")
    history2, has_more2, page2, total_pages2 = parser.get_articles_history(test_url, page_size=10, page=1)
    print(f"📚 历史记录中有 {len(history2)} 篇文章")
    print(f"🔄 是否有更多: {has_more2}")
    print(f"📄 当前页: {page2}/{total_pages2}")
    
    # 测试分页
    if len(history2) > 3:
        print("\n5️⃣ 测试分页功能...")
        page1_articles, has_more_p1, current_p1, total_p1 = parser.get_articles_history(test_url, page_size=3, page=1)
        page2_articles, has_more_p2, current_p2, total_p2 = parser.get_articles_history(test_url, page_size=3, page=2)
        
        print(f"📄 第1页: {len(page1_articles)} 篇文章, 有更多: {has_more_p1}, 总页数: {total_p1}")
        print(f"📄 第2页: {len(page2_articles)} 篇文章, 有更多: {has_more_p2}, 总页数: {total_p2}")
    
    # 显示文章时间信息
    if history2:
        print("\n6️⃣ 最新文章的时间信息:")
        latest_article = history2[0]
        print(f"  标题: {latest_article['title'][:40]}...")
        print(f"  发布时间: {latest_article.get('published', 'N/A')}")
        print(f"  获取时间: {latest_article.get('fetch_time', 'N/A')[:19]}")
    
    print("\n✅ 测试完成！")
    
    # 询问是否清理测试数据
    cleanup = input("\n是否清理测试数据? (y/n): ").strip().lower()
    if cleanup == 'y':
        if os.path.exists(parser.articles_history_file):
            os.remove(parser.articles_history_file)
            print(f"🧹 已清理: {parser.articles_history_file}")

if __name__ == "__main__":
    try:
        test_real_rss()
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
