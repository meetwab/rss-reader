#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS 阅读器快速启动脚本
自动检查依赖并启动程序
"""

import sys
import subprocess
import os

def check_and_install_dependencies():
    """检查并安装必要的依赖"""
    required_packages = ['requests', 'feedparser']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} 未安装")
    
    if missing_packages:
        print(f"\n📦 正在安装缺失的依赖包: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                *missing_packages
            ])
            print("✅ 依赖安装完成!")
        except subprocess.CalledProcessError:
            print("❌ 依赖安装失败，请手动运行:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def choose_version():
    """让用户选择要运行的版本"""
    print("\n🎯 选择要运行的版本:")
    print("1. 基础版 (rss_reader.py) - 适合学习基础概念")
    print("2. 增强版 (rss_reader_enhanced.py) - 包含更多功能")
    print("3. 运行示例演示 (example_usage.py)")
    
    while True:
        choice = input("请选择 (1/2/3): ").strip()
        
        if choice == '1':
            return 'rss_reader.py'
        elif choice == '2':
            return 'rss_reader_enhanced.py'
        elif choice == '3':
            return 'example_usage.py'
        else:
            print("❌ 无效选择，请输入 1、2 或 3")

def main():
    """主函数"""
    print("🚀 RSS 阅读器快速启动")
    print("=" * 40)
    
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("❌ 需要 Python 3.6 或更高版本")
        print(f"当前版本: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python 版本: {sys.version.split()[0]}")
    
    # 检查并安装依赖
    if not check_and_install_dependencies():
        sys.exit(1)
    
    # 选择版本
    script_to_run = choose_version()
    
    if not os.path.exists(script_to_run):
        print(f"❌ 文件不存在: {script_to_run}")
        sys.exit(1)
    
    print(f"\n🎉 正在启动: {script_to_run}")
    print("=" * 40)
    
    # 运行选定的脚本
    try:
        if script_to_run == 'example_usage.py':
            # 对于示例脚本，直接导入并运行
            import example_usage
        else:
            # 对于主程序，使用subprocess运行
            subprocess.call([sys.executable, script_to_run])
    except KeyboardInterrupt:
        print("\n👋 程序被用户中断")
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")

if __name__ == "__main__":
    main()
