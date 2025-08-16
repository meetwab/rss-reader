#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试分页优化功能：
1. 展示总共有多少页
2. 当用户在最后一页时，如果选择 "查看更多"，则提示 "没有更多内容啦~"
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from demo_refactored import RssParser, UserInterface
from rich.console import Console

def test_pagination_optimization():
    """测试分页优化功能"""
    print("🎯 测试分页优化功能")
    print("=" * 50)
    
    parser = RssParser()
    ui = UserInterface()
    console = Console()
    
    # 创建测试数据
    test_url = "https://test-blog.com/rss"
    test_articles = []
    
    # 创建10篇测试文章以便测试分页
    for i in range(1, 11):
        article = {
            'title': f'测试文章{i:02d} - 分页测试专用',
            'link': f'https://test-blog.com/article{i:02d}',
            'summary': f'这是第{i}篇测试文章的摘要内容，用于验证分页功能是否正常工作。',
            'published': f'2025-01-{i:02d}T10:00:00Z',
            'fetch_time': f'2025-01-{i:02d}T10:30:00'
        }
        test_articles.append(article)
    
    # 添加测试文章到历史
    print("📚 创建测试数据...")
    parser._update_articles_history(test_url, test_articles)
    
    # 测试总页数显示
    print("\n1️⃣ 测试总页数显示")
    print("-" * 30)
    
    for page_size in [3, 4, 5]:
        articles, has_more, current_page, total_pages = parser.get_articles_history(test_url, page_size=page_size, page=1)
        print(f"页面大小: {page_size}, 总页数: {total_pages}, 第1页文章数: {len(articles)}")
    
    # 测试分页边界情况
    print("\n2️⃣ 测试分页边界情况")
    print("-" * 30)
    
    page_size = 3
    total_articles = len(test_articles)
    expected_total_pages = (total_articles + page_size - 1) // page_size
    
    print(f"总文章数: {total_articles}")
    print(f"每页文章数: {page_size}")
    print(f"预期总页数: {expected_total_pages}")
    
    for page in range(1, expected_total_pages + 2):  # 多测试一页
        articles, has_more, current_page, total_pages = parser.get_articles_history(test_url, page_size=page_size, page=page)
        print(f"第{page}页: {len(articles)}篇文章, 有更多: {has_more}, 总页数: {total_pages}")
    
    # 测试UI组件的页码显示
    print("\n3️⃣ 测试UI页码显示")
    print("-" * 30)
    
    # 测试第一页
    articles, has_more, current_page, total_pages = parser.get_articles_history(test_url, page_size=3, page=1)
    print("第1页的菜单显示:")
    ui.show_articles_menu(articles, has_more, current_page, total_pages)
    
    # 测试中间页
    articles, has_more, current_page, total_pages = parser.get_articles_history(test_url, page_size=3, page=2)
    print("\n第2页的菜单显示:")
    ui.show_articles_menu(articles, has_more, current_page, total_pages)
    
    # 测试最后一页
    articles, has_more, current_page, total_pages = parser.get_articles_history(test_url, page_size=3, page=total_pages)
    print(f"\n第{total_pages}页(最后一页)的菜单显示:")
    ui.show_articles_menu(articles, has_more, current_page, total_pages)
    
    # 测试"没有更多内容"的提示
    print("\n4️⃣ 测试'没有更多内容'提示")
    print("-" * 30)
    
    if not has_more:
        print("✅ 在最后一页，has_more = False")
        print("模拟用户在最后一页点击'查看更多'时的提示:")
        
        # 模拟UI中的提示逻辑
        from rich.panel import Panel
        info_panel = Panel(
            "[yellow]😊 没有更多内容啦~ [/yellow]",
            style="yellow",
            border_style="yellow"
        )
        console.print(info_panel)
    
    # 测试空页面情况
    print("\n5️⃣ 测试空页面情况")
    print("-" * 30)
    
    empty_url = "https://empty-blog.com/rss"
    articles, has_more, current_page, total_pages = parser.get_articles_history(empty_url, page_size=3, page=1)
    print(f"空订阅的分页信息: 文章数={len(articles)}, 有更多={has_more}, 当前页={current_page}, 总页数={total_pages}")
    
    print("\n✅ 分页优化功能测试完成！")
    
    # 清理测试数据
    if os.path.exists(parser.articles_history_file):
        os.remove(parser.articles_history_file)
        print("🧹 已清理测试数据")

def test_interactive_pagination():
    """测试交互式分页功能"""
    print("\n" + "=" * 50)
    print("🎮 交互式分页测试 (可选)")
    print("=" * 50)
    
    user_input = input("是否进行交互式分页测试? (y/n): ").strip().lower()
    if user_input != 'y':
        return
    
    print("\n📝 说明: 这将模拟用户在UI中的分页操作")
    print("你可以测试以下场景:")
    print("1. 在有更多页面时选择 [m] - 应该翻到下一页")
    print("2. 在最后一页时选择 [m] - 应该显示'没有更多内容啦~'")
    print("3. 观察页码信息的显示")
    
    # 这里可以添加更详细的交互测试
    # 但为了简化，我们先提供说明
    print("\n💡 提示: 运行主程序 demo_refactored.py 来体验完整的交互式功能")

if __name__ == "__main__":
    try:
        test_pagination_optimization()
        test_interactive_pagination()
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
