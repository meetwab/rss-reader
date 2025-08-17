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


class RssParser:
    """RSS 解析器，负责网络请求和 RSS 源解析"""
    
    def __init__(self, article_manager: ArticleManager, timeout: int = 10):
        self.timeout = timeout
        self.console = Console()
        self.article_manager = article_manager
    
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

            title = feed.feed.get("title")
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
                article = {
                    'title': entry.get("title", "无标题"),
                    'link': entry.get("link", "无链接"),
                    'summary': self._clean_html(entry.get("summary", "无摘要")),
                    'published': entry.get("published", ""),
                    'fetch_time': datetime.now().isoformat()
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
    
    def fetch_and_save_articles(self, url: str, count: int = 3) -> List[Dict[str, str]]:
        """
        获取 RSS 源的最新文章并保存到 articles_history.json 文件中。

        Args:
            url (str): RSS 源链接
            count (int): 获取文章数量

        Returns:
            List[Dict[str, str]]: 文章列表
        """
        # 获取新文章
        new_articles = self.fetch_articles(url, count)
        
        # 如果获取成功，则更新历史记录
        if new_articles:
            self.article_manager.update_articles_history(url, new_articles)
        
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
