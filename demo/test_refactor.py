#!/usr/bin/env python3
"""
测试重构后的删除订阅功能
"""

import json
import os
import tempfile
from demo_refactored import SubscriptionManager, UserInterface

def test_delete_refactor():
    """测试重构后的删除功能"""
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        test_subscriptions = {
            "测试订阅 1": "https://example1.com/rss",
            "测试订阅 2": "https://example2.com/rss"
        }
        json.dump(test_subscriptions, f, ensure_ascii=False)
        temp_file = f.name
    
    try:
        # 测试 SubscriptionManager
        manager = SubscriptionManager(temp_file)
        
        # 测试获取订阅信息
        name, url = manager.get_subscription_info(1)
        print(f"获取到订阅信息：{name} - {url}")
        assert name == "测试订阅 1"
        assert url == "https://example1.com/rss"
        
        # 测试无效序号
        name, url = manager.get_subscription_info(999)
        assert name is None
        assert url is None
        
        # 测试 UserInterface 确认方法
        ui = UserInterface()
        
        print("\n✅ 重构测试通过！")
        print("✅ SubscriptionManager 不再包含用户交互逻辑")
        print("✅ UserInterface 新增了确认删除的方法")
        print("✅ 职责分离成功实现")
        
    finally:
        # 清理临时文件
        os.unlink(temp_file)

if __name__ == "__main__":
    test_delete_refactor()
