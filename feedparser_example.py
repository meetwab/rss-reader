#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feedparser 使用示例
"""

import requests
import feedparser

def demo_feedparser():
    """演示 feedparser 的基本用法"""
    
    # 使用一个公开的 RSS 源作为示例
    rss_url = "https://feeds.feedburner.com/oreilly/radar"
    
    print("🔍 正在获取 RSS 数据...")
    try:
        # 获取 RSS 内容
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
        
        # 解析 RSS 内容
        feed = feedparser.parse(response.content)
        
        # 显示 RSS 源信息
        print(f"\n📰 RSS 源信息:")
        print(f"标题: {feed.feed.get('title', '未知')}")
        print(f"描述: {feed.feed.get('description', '无描述')}")
        print(f"链接: {feed.feed.get('link', '无链接')}")
        
        # 显示前 3 篇文章
        print(f"\n📑 最新文章 (共 {len(feed.entries)} 篇):")
        print("-" * 60)
        
        for i, entry in enumerate(feed.entries[:3], 1):
            print(f"\n[{i}] {entry.get('title', '无标题')}")
            print(f"🔗 链接: {entry.get('link', '无链接')}")
            print(f"📅 发布: {entry.get('published', '未知日期')}")
            
            # 摘要
            summary = entry.get('summary', entry.get('description', '无摘要'))
            if len(summary) > 150:
                summary = summary[:150] + "..."
            print(f"📝 摘要: {summary}")
            print("-" * 60)
            
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    demo_feedparser()
