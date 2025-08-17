#!/usr/bin/env python3
"""
测试模块化后的 RSS 阅读器是否工作正常
"""

def test_imports():
    """测试所有模块是否能正常导入"""
    try:
        print("🔍 测试模块导入...")
        
        from rss_reader.models import NavigationAction
        print("✅ models.py 导入成功")
        
        from rss_reader.file_handler import FileHandler
        print("✅ file_handler.py 导入成功")
        
        from rss_reader.article_manager import ArticleManager
        print("✅ article_manager.py 导入成功")
        
        from rss_reader.rss_parser import RssParser
        print("✅ rss_parser.py 导入成功")
        
        from rss_reader.subscription_manager import SubscriptionManager
        print("✅ subscription_manager.py 导入成功")
        
        from rss_reader.ui import UserInterface
        print("✅ ui.py 导入成功")
        
        from rss_reader.main import RssApp
        print("✅ main.py 导入成功")
        
        print("\n🎉 所有模块导入测试通过！")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败：{e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误：{e}")
        return False

def test_basic_functionality():
    """测试基本功能是否正常"""
    try:
        print("\n🔍 测试基本功能...")
        
        from rss_reader.file_handler import FileHandler
        from rss_reader.models import NavigationAction
        
        # 测试文件处理器
        file_handler = FileHandler()
        test_data = {"test": "data"}
        
        # 测试枚举
        action = NavigationAction.BACK_TO_HOME
        print(f"✅ 枚举测试通过：{action}")
        
        print("✅ 基本功能测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 基本功能测试失败：{e}")
        return False

def test_app_creation():
    """测试应用创建"""
    try:
        print("\n🔍 测试应用创建...")
        
        from rss_reader.main import RssApp
        
        # 创建应用实例
        app = RssApp()
        print("✅ RssApp 实例创建成功")
        
        # 检查应用是否有必要的属性
        assert hasattr(app, 'ui'), "应用缺少 ui 属性"
        print("✅ 应用结构验证通过")
        
        print("✅ 应用创建测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 应用创建测试失败：{e}")
        return False

def main():
    """运行所有测试"""
    print("=" * 50)
    print("🧪 RSS Reader 模块化测试")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_basic_functionality,
        test_app_creation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果：✅ {passed} 个通过，❌ {failed} 个失败")
    
    if failed == 0:
        print("🎉 所有测试通过！模块化重构成功！")
        print("\n启动应用请运行：")
        print("  python run.py")
        print("或：")
        print("  python -m rss_reader.main")
    else:
        print("⚠️ 有测试失败，请检查代码")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
