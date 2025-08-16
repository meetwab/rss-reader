#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试假数据的历史文章功能
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from demo_refactored import RssParser, FileHandler

def test_fake_data():
    """测试假数据的历史文章功能"""
    print("🧪 测试假数据的历史文章功能")
    print("=" * 50)
    
    # 创建解析器
    parser = RssParser()
    file_handler = FileHandler()
    
    # 加载订阅数据
    subscriptions = file_handler.load_subscriptions("subscriptions.json")
    print(f"📰 加载的订阅数量: {len(subscriptions)}")
    
    for i, (name, url) in enumerate(subscriptions.items(), 1):
        print(f"  {i}. {name} - {url}")
    
    # 测试每个订阅的历史文章
    print(f"\n📚 测试历史文章:")
    
    for name, url in subscriptions.items():
        print(f"\n📖 {name}:")
        
        # 获取历史文章（第一页）
        articles, has_more, current_page, total_pages = parser.get_articles_history(url, page_size=3, page=1)
        
        print(f"  📄 第{current_page}页 / 共{total_pages}页")
        print(f"  📝 文章数量: {len(articles)}")
        print(f"  🔄 是否有更多: {has_more}")
        
        if articles:
            print(f"  📋 文章列表:")
            for i, article in enumerate(articles, 1):
                print(f"    {i}. {article['title']}")
                print(f"       发布时间: {article.get('published', 'N/A')}")
                print(f"       获取时间: {article.get('fetch_time', 'N/A')[:19]}")
        else:
            print(f"  ⚠️  没有找到历史文章")
    
    # 测试分页功能
    if subscriptions:
        first_url = list(subscriptions.values())[0]
        first_name = list(subscriptions.keys())[0]
        
        print(f"\n🔍 详细测试 '{first_name}' 的分页功能:")
        
        # 获取总文章数
        all_articles, _, _, total_pages = parser.get_articles_history(first_url, page_size=100, page=1)
        print(f"  📊 总文章数: {len(all_articles)}")
        print(f"  📄 按3篇/页计算总页数: {total_pages}")
        
        # 测试前3页
        for page in range(1, min(4, total_pages + 1)):
            articles, has_more, current_page, total_pages = parser.get_articles_history(first_url, page_size=3, page=page)
            print(f"\n  📄 第{page}页:")
            print(f"    文章数: {len(articles)}")
            print(f"    有更多: {has_more}")
            
            for i, article in enumerate(articles, 1):
                print(f"    {i}. {article['title'][:40]}...")

def demonstrate_ui_simulation():
    """模拟用户界面交互"""
    print(f"\n{'='*50}")
    print("🎮 模拟用户界面交互")
    print("=" * 50)
    
    from demo_refactored import UserInterface
    
    ui = UserInterface()
    
    # 获取第一个订阅进行演示
    subscriptions = ui.subscription_manager.get_subscriptions()
    if subscriptions:
        first_name, first_url = list(subscriptions.items())[0]
        
        print(f"📖 模拟查看 '{first_name}' 的文章:")
        
        # 获取历史文章（第一页）
        articles, has_more, current_page, total_pages = ui.rss_parser.get_articles_history(first_url, page_size=3, page=1)
        
        # 显示文章
        ui.display_articles(articles, f"{first_name} (历史文章)")
        
        # 显示菜单
        ui.show_articles_menu(articles, has_more, current_page, total_pages)
        
        print("💡 提示: 在实际使用中，您可以:")
        print("  - 按 [h] 进入历史文章模式")
        print("  - 按 [m] 查看更多文章")
        print("  - 看到页码信息显示")
        print("  - 在最后一页会看到'没有更多内容啦~'的提示")

if __name__ == "__main__":
    try:
        test_fake_data()
        demonstrate_ui_simulation()
        
        print(f"\n{'='*50}")
        print("✅ 假数据测试完成!")
        print("🚀 现在您可以运行 'python3 demo_refactored.py' 来体验完整功能")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
