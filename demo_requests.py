#!/usr/bin/env python3
import requests
import json

print("=== requests.get() 演示 ===")
print()

# 1. 基本用法示例
print("1. 发送 GET 请求:")
url = "https://httpbin.org/get"  # 测试网站
print(f"请求 URL: {url}")

try:
    response = requests.get(url, timeout=10)
    print(f"响应状态码: {response.status_code}")
    print(f"响应类型: {type(response)}")
    print()
    
    print("2. response 对象的常用属性:")
    print(f"response.status_code = {response.status_code}")
    print(f"response.headers['Content-Type'] = {response.headers.get('Content-Type')}")
    print(f"response.text 的前100字符:")
    print(response.text[:100] + "...")
    print()
    
    print("3. 超时参数的重要性:")
    print("timeout=10 表示:")
    print("- 如果服务器在 10 秒内没有响应，就抛出超时异常")
    print("- 防止程序永远等待")
    print("- 提升用户体验")
    
except requests.exceptions.Timeout:
    print("❌ 请求超时!")
except requests.exceptions.RequestException as e:
    print(f"❌ 请求失败: {e}")

print("\n" + "="*50)
print("RSS 场景演示:")

# 2. RSS 场景的实际示例
rss_url = "https://sspai.com/feed"
print(f"获取 RSS: {rss_url}")

try:
    response = requests.get(rss_url, timeout=10)
    if response.status_code == 200:
        print("✅ RSS 获取成功!")
        print(f"内容长度: {len(response.content)} 字节")
        print("RSS 内容预览 (前200字符):")
        print(response.text[:200] + "...")
    else:
        print(f"❌ HTTP 错误: {response.status_code}")
        
except Exception as e:
    print(f"❌ 请求失败: {e}")
