#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
enumerate() 函数用法演示
"""

def demo_enumerate():
    """演示 enumerate 的各种用法"""
    
    print("=== enumerate() 函数演示 ===\n")
    
    # 示例 1: 基本用法（从 0 开始计数）
    fruits = ['苹果', '香蕉', '橙子', '葡萄']
    
    print("1. 基本用法（从 0 开始）:")
    for i, fruit in enumerate(fruits):
        print(f"  索引 {i}: {fruit}")
    
    print()
    
    # 示例 2: 从 1 开始计数
    print("2. 从 1 开始计数:")
    for i, fruit in enumerate(fruits, 1):
        print(f"  第 {i} 个水果: {fruit}")
    
    print()
    
    # 示例 3: 不使用 enumerate 的传统方法（对比）
    print("3. 不使用 enumerate 的传统方法:")
    for i in range(len(fruits)):
        print(f"  索引 {i}: {fruits[i]}")
    
    print()
    
    # 示例 4: 只取前 3 个元素
    print("4. 只取前 3 个元素:")
    for i, fruit in enumerate(fruits[:3], 1):
        print(f"  [{i}] {fruit}")
    
    print()
    
    # 示例 5: 模拟你的 RSS 代码
    print("5. 模拟 RSS 文章列表:")
    fake_articles = [
        {'title': 'Python 入门教程', 'link': 'http://example.com/1'},
        {'title': '机器学习基础', 'link': 'http://example.com/2'},
        {'title': 'Web 开发指南', 'link': 'http://example.com/3'},
        {'title': '数据库优化技巧', 'link': 'http://example.com/4'}
    ]
    
    # 这就是你的代码中的用法
    for i, entry in enumerate(fake_articles[:3], 1):
        print(f"  [{i}] {entry['title']}")
        print(f"      🔗 {entry['link']}")
    
    print()
    
    # 示例 6: enumerate 返回的实际内容
    print("6. enumerate 返回的实际内容:")
    result = list(enumerate(fruits[:2], 1))
    print(f"  enumerate 结果: {result}")
    print(f"  数据类型: {type(result[0])}")

if __name__ == "__main__":
    demo_enumerate()
