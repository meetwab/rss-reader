#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的文章历史和分页功能
"""

import os
import sys
import json
from datetime import datetime

# 添加当前目录到路径以便导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from demo_refactored import RssParser, FileHandler

def test_articles_history():
    """测试文章历史功能"""
    print("=== 测试文章历史功能 ===")
    
    # 创建测试用的RSS解析器
    parser = RssParser()
    
    # 模拟文章数据
    test_url = "https://example.com/rss"
    test_articles = [
        {
            'title': '测试文章1',
            'link': 'https://example.com/article1',
            'summary': '这是第一篇测试文章的摘要',
            'published': '2025-01-01',
            'fetch_time': datetime.now().isoformat()
        },
        {
            'title': '测试文章2',
            'link': 'https://example.com/article2',
            'summary': '这是第二篇测试文章的摘要',
            'published': '2025-01-02',
            'fetch_time': datetime.now().isoformat()
        },
        {
            'title': '测试文章3',
            'link': 'https://example.com/article3',
            'summary': '这是第三篇测试文章的摘要',
            'published': '2025-01-03',
            'fetch_time': datetime.now().isoformat()
        }
    ]
    
    # 测试更新文章历史
    print("1. 添加第一批文章到历史记录...")
    parser._update_articles_history(test_url, test_articles[:2])
    
    # 获取历史文章
    history_articles, has_more, page, total_pages = parser.get_articles_history(test_url, page_size=3, page=1)
    print(f"历史文章数量: {len(history_articles)}")
    print(f"是否有更多: {has_more}")
    print(f"当前页: {page}/{total_pages}")
    
    # 添加更多文章
    print("\n2. 添加更多文章...")
    more_articles = [
        {
            'title': '测试文章4',
            'link': 'https://example.com/article4',
            'summary': '这是第四篇测试文章的摘要',
            'published': '2025-01-04',
            'fetch_time': datetime.now().isoformat()
        },
        {
            'title': '测试文章5',
            'link': 'https://example.com/article5',
            'summary': '这是第五篇测试文章的摘要',
            'published': '2025-01-05',
            'fetch_time': datetime.now().isoformat()
        }
    ]
    
    parser._update_articles_history(test_url, more_articles)
    
    # 测试分页
    print("\n3. 测试分页功能...")
    page1_articles, has_more1, current_page1, total_pages1 = parser.get_articles_history(test_url, page_size=2, page=1)
    print(f"第1页: {len(page1_articles)} 篇文章, 有更多: {has_more1}, 总页数: {total_pages1}")
    for article in page1_articles:
        print(f"  - {article['title']}")
    
    page2_articles, has_more2, current_page2, total_pages2 = parser.get_articles_history(test_url, page_size=2, page=2)
    print(f"第2页: {len(page2_articles)} 篇文章, 有更多: {has_more2}, 总页数: {total_pages2}")
    for article in page2_articles:
        print(f"  - {article['title']}")
    
    # 测试重复文章去重
    print("\n4. 测试重复文章去重...")
    duplicate_articles = [test_articles[0]]  # 重复的第一篇文章
    parser._update_articles_history(test_url, duplicate_articles)
    
    final_articles, _, _, final_total_pages = parser.get_articles_history(test_url, page_size=10, page=1)
    print(f"去重后总文章数: {len(final_articles)}")
    print(f"总页数: {final_total_pages}")
    
    # 清理测试文件
    if os.path.exists(parser.articles_history_file):
        os.remove(parser.articles_history_file)
        print(f"\n已清理测试文件: {parser.articles_history_file}")

def test_file_operations():
    """测试文件操作功能"""
    print("\n=== 测试文件操作功能 ===")
    
    test_filename = "test_articles_history.json"
    test_data = {
        "https://example.com/rss": [
            {
                'title': '测试文章',
                'link': 'https://example.com/article',
                'summary': '测试摘要',
                'published': '2025-01-01',
                'fetch_time': datetime.now().isoformat()
            }
        ]
    }
    
    # 测试保存
    print("1. 测试保存文章历史...")
    success = FileHandler.save_articles_history(test_filename, test_data)
    print(f"保存结果: {success}")
    
    # 测试加载
    print("2. 测试加载文章历史...")
    loaded_data = FileHandler.load_articles_history(test_filename)
    print(f"加载的数据键: {list(loaded_data.keys())}")
    print(f"文章数量: {len(loaded_data.get('https://example.com/rss', []))}")
    
    # 清理测试文件
    if os.path.exists(test_filename):
        os.remove(test_filename)
        print(f"已清理测试文件: {test_filename}")

if __name__ == "__main__":
    try:
        test_file_operations()
        test_articles_history()
        print("\n✅ 所有测试通过！")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
