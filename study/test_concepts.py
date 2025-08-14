#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
概念验证和测试脚本
用于理解 RSS 阅读器中的每个编程概念
"""

import json
import os
from typing import Dict, List, Optional

def test_1_file_operations():
    """测试文件操作和 JSON 处理"""
    print("🧪 测试1: 文件操作和 JSON 处理")
    print("-" * 40)
    
    # 1. 创建测试数据
    test_subscriptions = {
        "Python 官方博客": "https://blog.python.org/feeds/posts/default?alt=rss",
        "GitHub 博客": "https://github.blog/feed/"
    }
    
    # 2. 写入文件（模拟 save_subscriptions）
    config_file = "test_subscriptions.json"
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(test_subscriptions, f, ensure_ascii=False, indent=2)
        print("✅ JSON 文件写入成功")
    except Exception as e:
        print(f"❌ 写入失败: {e}")
    
    # 3. 读取文件（模拟 load_subscriptions）
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            print(f"✅ 读取成功，加载了 {len(loaded_data)} 个订阅源:")
            for name, url in loaded_data.items():
                print(f"   - {name}: {url}")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"❌ 读取失败: {e}")
    
    # 4. 清理测试文件
    if os.path.exists(config_file):
        os.remove(config_file)
        print("🧹 测试文件已清理")
    
    print("\n")

def test_2_exception_handling():
    """测试异常处理机制"""
    print("🧪 测试2: 异常处理")
    print("-" * 40)
    
    # 1. 测试单个异常
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"✅ 捕获除零错误: {e}")
    
    # 2. 测试多个异常类型
    test_cases = [
        ("不存在的文件", "non_existent_file.json"),
        ("格式错误的JSON", "invalid.json")
    ]
    
    for description, filename in test_cases:
        try:
            if filename == "invalid.json":
                # 创建格式错误的 JSON 文件
                with open(filename, 'w') as f:
                    f.write("{invalid json}")
            
            with open(filename, 'r') as f:
                json.load(f)
                
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"✅ 捕获异常 ({description}): {type(e).__name__}")
            
            # 清理测试文件
            if os.path.exists(filename):
                os.remove(filename)
    
    print("\n")

def test_3_class_and_objects():
    """测试面向对象编程概念"""
    print("🧪 测试3: 类和对象")
    print("-" * 40)
    
    # 简化版的 RSS Reader 类
    class SimpleRSSReader:
        def __init__(self, config_name: str = "test_config.json"):
            """构造函数"""
            self.config_file = config_name
            self.subscriptions = {}
            print(f"✅ RSS 阅读器实例已创建，配置文件: {config_name}")
        
        def add_subscription(self, name: str, url: str):
            """添加订阅源"""
            self.subscriptions[name] = url
            print(f"✅ 已添加订阅源: {name}")
        
        def get_count(self) -> int:
            """获取订阅源数量"""
            return len(self.subscriptions)
        
        def list_subscriptions(self):
            """列出所有订阅源"""
            if not self.subscriptions:
                print("📭 暂无订阅源")
                return
            
            print("📚 当前订阅源:")
            for i, (name, url) in enumerate(self.subscriptions.items(), 1):
                print(f"  [{i}] {name}")
    
    # 创建实例并测试
    reader = SimpleRSSReader("my_test_config.json")
    print(f"初始订阅源数量: {reader.get_count()}")
    
    reader.add_subscription("测试博客", "https://example.com/feed")
    reader.add_subscription("技术新闻", "https://tech.example.com/rss")
    
    print(f"添加后订阅源数量: {reader.get_count()}")
    reader.list_subscriptions()
    
    print("\n")

def test_4_type_hints():
    """测试类型提示"""
    print("🧪 测试4: 类型提示")
    print("-" * 40)
    
    # 基本类型提示
    def process_articles(articles: List[Dict[str, str]]) -> Optional[int]:
        """
        处理文章列表
        参数: articles - 文章字典列表
        返回: 文章数量或 None
        """
        if not articles:
            return None
        
        print(f"处理 {len(articles)} 篇文章:")
        for i, article in enumerate(articles, 1):
            title = article.get('title', '无标题')
            print(f"  {i}. {title}")
        
        return len(articles)
    
    # 测试数据
    test_articles = [
        {'title': 'Python 教程', 'link': 'https://example.com/1'},
        {'title': 'Web 开发指南', 'link': 'https://example.com/2'}
    ]
    
    result = process_articles(test_articles)
    print(f"✅ 返回结果: {result}")
    
    # 测试空列表情况
    empty_result = process_articles([])
    print(f"✅ 空列表返回: {empty_result}")
    
    print("\n")

def test_5_string_formatting():
    """测试字符串格式化"""
    print("🧪 测试5: 字符串格式化")
    print("-" * 40)
    
    # f-string 格式化
    name = "Python RSS 阅读器"
    version = "1.0"
    article_count = 10
    
    print(f"项目名称: {name}")
    print(f"版本: {version}")
    print(f"文章数量: {article_count}")
    
    # 格式化数字和日期
    from datetime import datetime
    now = datetime.now()
    
    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"格式化数字: {article_count:,}")  # 千位分隔符
    print(f"百分比: {0.856:.1%}")  # 百分比格式
    
    # 字符串方法
    sample_text = "  Hello Python World!  "
    print(f"原文: '{sample_text}'")
    print(f"去空格: '{sample_text.strip()}'")
    print(f"转小写: '{sample_text.lower()}'")
    print(f"是否数字: '{sample_text.strip().isdigit()}'")
    
    print("\n")

def main():
    """主测试函数"""
    print("🔬 RSS 阅读器概念验证测试")
    print("=" * 50)
    
    # 依次运行各个测试
    test_functions = [
        test_1_file_operations,
        test_2_exception_handling,
        test_3_class_and_objects,
        test_4_type_hints,
        test_5_string_formatting
    ]
    
    for test_func in test_functions:
        try:
            test_func()
        except Exception as e:
            print(f"❌ 测试 {test_func.__name__} 失败: {e}")
    
    print("🎉 所有概念验证完成！")
    print("\n下一步: 运行原项目并对比理解")
    print("命令: python rss_reader.py")

if __name__ == "__main__":
    main()
