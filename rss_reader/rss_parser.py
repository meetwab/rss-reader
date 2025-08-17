"""
RSS parsing and network request handling.
"""

import html
import re
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import feedparser
import requests
from bs4 import BeautifulSoup
from rich.console import Console

from .article_manager import ArticleManager
from .ai_summarizer_refactored import create_ai_summarizer_from_config


class RssParser:
    """RSS 解析器，负责网络请求和 RSS 源解析"""
    
    def __init__(self, article_manager: ArticleManager, ai_summarizer=None, timeout: int = 10, enable_ai_summary: bool = True):
        self.timeout = timeout
        self.console = Console()
        self.article_manager = article_manager
        self.enable_ai_summary = enable_ai_summary
        
        # 使用传入的 AI 摘要器，如果没有传入则创建新的
        if ai_summarizer is not None:
            self.ai_summarizer = ai_summarizer
        elif self.enable_ai_summary:
            self.ai_summarizer = create_ai_summarizer_from_config()
        else:
            self.ai_summarizer = None
    
    def fetch_feed_info(self, url: str) -> Tuple[Optional[str], bool]:
        """
        获取 RSS 源的标题信息

        Args:
            url (str): RSS 源链接

        Returns:
            Tuple[Optional[str], bool]: (标题，是否成功)
        """
        try:
            print(f"正在请求链接：{url}")
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            feed = feedparser.parse(response.content)
            
            if feed.bozo:
                print(f" 警告：链接 {url} 可能不是一个有效的 RSS/Atom 源。错误：{feed.bozo_exception}")

            title = getattr(feed.feed, 'title', None) if hasattr(feed, 'feed') else None
            if not title:
                print(" 无法从链接中获取标题，将使用默认名称。")
                # 添加微秒级时间戳和随机数，确保名称唯一性
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                random_suffix = random.randint(1000, 9999)
                title = f"未命名订阅_{timestamp}_{random_suffix}"
            
            print(f"成功获取标题：{title}")
            return title, True

        except requests.exceptions.SSLError:
            print(" ❌ SSL 连接错误：无法建立安全连接，可能是网站证书问题")
            return None, False
        except requests.exceptions.Timeout:
            print(" ⏰ 连接超时：网络响应过慢，请稍后重试")
            return None, False
        except requests.exceptions.ConnectionError:
            print(" 🌐 连接错误：无法连接到服务器，请检查网络连接")
            return None, False
        except requests.exceptions.HTTPError as e:
            print(f" 🚫 HTTP 错误：服务器返回错误状态码 {e.response.status_code}")
            return None, False
        except requests.exceptions.RequestException:
            print(" 📡 网络请求失败：连接或传输过程中发生问题")
            return None, False
        except Exception:
            print(" ❓ 处理订阅时发生未知错误，请稍后重试")
            return None, False
    
    def fetch_articles(self, url: str, count: int = 3) -> List[Dict[str, str]]:
        """
        获取 RSS 源的最新文章（纯获取功能，不涉及数据持久化）

        Args:
            url (str): RSS 源链接
            count (int): 获取文章数量

        Returns:
            List[Dict[str, str]]: 文章列表
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            feed = feedparser.parse(response.content)

            if not feed.entries:
                print(f" 警告：链接 {url} 没有找到任何文章。")
                return []

            # 获取新文章
            new_articles = []
            for entry in feed.entries[:count]:
                # 基础文章信息
                title = str(entry.get("title", "无标题"))
                link = str(entry.get("link", "无链接"))
                summary_raw = entry.get("summary", "无摘要")
                original_summary = self._clean_html(str(summary_raw) if summary_raw else "无摘要")
                published = str(entry.get("published", ""))
                fetch_time = datetime.now().isoformat()
                
                # 注意：AI摘要的生成已移到 _enhance_articles_with_ai 方法中
                # 在 fetch_and_save_articles 流程中进行AI增强处理
                article = {
                    'title': title,
                    'link': link,
                    'summary': original_summary,
                    'ai_summary': None,  # 新文章先设为None，稍后进行AI增强时生成
                    'published': published,
                    'fetch_time': fetch_time
                }
                new_articles.append(article)
            
            return new_articles

        except requests.exceptions.SSLError:
            print(" ❌ SSL 连接错误：无法建立安全连接，可能是网站证书问题")
            return []
        except requests.exceptions.Timeout:
            print(" ⏰ 连接超时：网络响应过慢，请稍后重试")
            return []
        except requests.exceptions.ConnectionError:
            print(" 🌐 连接错误：无法连接到服务器，请检查网络连接")
            return []
        except requests.exceptions.HTTPError as e:
            print(f" 🚫 HTTP 错误：服务器返回错误状态码 {e.response.status_code}")
            return []
        except requests.exceptions.RequestException as e:
            print(" 📡 网络请求失败：连接或传输过程中发生问题")
            return []
        except Exception as e:
            print(" ❓ 处理文章时发生未知错误，请稍后重试")
            return []
    
    def _enhance_articles_with_ai(self, articles: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        使用AI对文章进行增强处理（摘要生成等）
        
        职责：
        1. 为新文章生成AI摘要
        2. 可扩展支持其他AI功能（关键词提取、分类等）
        3. 保持原有文章数据结构不变
        
        Args:
            articles (List[Dict[str, str]]): 原始文章列表
            
        Returns:
            List[Dict[str, str]]: AI增强后的文章列表
        """
        enhanced_articles = []
        
        for article in articles:
            # 生成AI摘要（如果需要且可用）
            if not article.get('ai_summary') and self.ai_summarizer and self.ai_summarizer.is_enabled():
                print(f"  正在为文章「{article['title']}」生成 AI 摘要...")
                ai_summary = self.ai_summarizer.generate_summary(article['title'], article['summary'])
                if ai_summary:
                    article['ai_summary'] = ai_summary
                    print(f"  ✅ AI 摘要生成成功")
                else:
                    print(f"  ⚠️ AI 摘要生成失败，将使用原始摘要")
            
            # 未来可以在这里添加更多AI增强功能：
            # article = self._extract_keywords(article)
            # article = self._classify_article(article)
            
            enhanced_articles.append(article)
        
        return enhanced_articles
    
    def fetch_and_save_articles(self, url: str, count: int = 3) -> List[Dict[str, str]]:
        """
        获取 RSS 源的最新文章，进行AI增强处理，然后保存到历史记录

        Args:
            url (str): RSS 源链接
            count (int): 获取文章数量

        Returns:
            List[Dict[str, str]]: 文章列表
        """
        # 1. 获取原始文章
        new_articles = self.fetch_articles(url, count)
        
        # 2. 如果获取成功，识别真正的新文章，进行AI增强，再保存
        if new_articles:
            # 识别哪些是真正的新文章（避免对已存在的文章重复处理）
            truly_new_articles = self._filter_new_articles(url, new_articles)
            
            # 只对真正的新文章进行AI增强处理
            if truly_new_articles:
                enhanced_new_articles = self._enhance_articles_with_ai(truly_new_articles)
                
                # 保存到历史记录（ArticleManager只负责存储）
                self.article_manager.update_articles_history(url, enhanced_new_articles)
        
        return new_articles
    
    def _filter_new_articles(self, url: str, articles: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        过滤出真正的新文章（基于链接去重）
        
        Args:
            url (str): RSS源链接
            articles (List[Dict[str, str]]): 待检查的文章列表
            
        Returns:
            List[Dict[str, str]]: 真正的新文章列表
        """
        # 获取现有文章的链接集合
        articles_history = self.article_manager.file_handler.load_articles_history(
            self.article_manager.articles_history_file
        )
        existing_articles = articles_history.get(url, [])
        existing_links = {article['link'] for article in existing_articles}
        
        # 只返回链接不存在的新文章
        new_articles = []
        for article in articles:
            if article['link'] not in existing_links:
                new_articles.append(article)
        
        return new_articles
    
    def _clean_html(self, text: str) -> str:
        """使用 BeautifulSoup 清理 HTML 标签，保留文本内容"""
        if not text:
            return text
        
        try:
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(text, 'html.parser')
            
            # 移除 script 和 style 标签
            for script in soup(["script", "style"]):
                script.decompose()
            
            # 获取纯文本
            clean_text = soup.get_text()
            
            # 清理多余的空白字符
            clean_text = re.sub(r'\s+', ' ', clean_text)
            clean_text = html.unescape(clean_text)
            
            return clean_text.strip()
        except Exception:
            # 如果 BeautifulSoup 解析失败，回退到原始方法
            clean_text = re.sub(r'<[^>]+>', '', text)
            clean_text = re.sub(r'\s+', ' ', clean_text)
            clean_text = html.unescape(clean_text)
            return clean_text.strip()
