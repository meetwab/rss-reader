"""
Article management functionality including history storage and pagination.
"""

from typing import Dict, List, Tuple
import paginate
from .file_handler import FileHandler


class ArticleManager:
    """文章管理器，负责文章历史数据的存储、检索和管理"""
    
    def __init__(self, articles_history_file: str = "articles_history.json"):
        self.articles_history_file = articles_history_file
        self.file_handler = FileHandler()
    
    def _load_and_sort_articles_by_url(self, url: str) -> List[Dict[str, str]]:
        """
        1. 从 articles_history.json 文件中，根据 URL 获取 RSS 源的文章;
        2. 将文章按时间排序。
        
        Args:
            url (str): RSS 源链接
            
        Returns:
            List[Dict[str, str]]: 按获取时间倒序排列的文章列表
        """
        # 从 articles_history.json 文件中加载所有订阅源及其文章
        articles_history = self.file_handler.load_articles_history(self.articles_history_file)
        # 获取指定 URL 的所有文章
        all_articles = articles_history.get(url, [])
        
        # 按获取时间倒序排列，最新的在前面
        all_articles.sort(key=lambda x: x.get('fetch_time', ''), reverse=True)
        
        return all_articles
    
    def _paginate_articles(self, items: List[Dict[str, str]], page_size: int, page: int) -> Tuple[List[Dict[str, str]], bool, int, int]:
        """
        使用 paginate 库对项目列表进行分页。

        这是一个通用的分页辅助方法，可以处理任何项目列表。
        
        Args:
            items (List[Dict[str, str]]): 需要分页的项目列表。
            page_size (int): 每页显示的项目数量。
            page (int): 当前请求的页码（从 1 开始）。
            
        Returns:
            Tuple[List[Dict[str, str]], bool, int, int]: 一个元组，包含：
                - 当前页的项目列表。
                - 是否有下一页 (bool)。
                - 当前页码 (int)。
                - 总页数 (int)。
        """
        if not items:
            return [], False, 1, 1
        
        paginator = paginate.Page(items, page=page, items_per_page=page_size)
        
        # 检查是否有下一页：next_page 不为 None 表示有下一页
        has_next = paginator.next_page is not None
        
        return paginator.items, has_next, paginator.page, paginator.page_count
    
    def get_paginated_articles(self, url: str, page_size: int = 5, page: int = 1) -> Tuple[List[Dict[str, str]], bool, int, int]:
        """
        获取 RSS 订阅源的历史文章并进行分页处理
        
        Args:
            url (str): RSS 源链接
            page_size (int): 每页文章数量
            page (int): 页码（从 1 开始）

        Returns:
            Tuple[List[Dict[str, str]], bool, int, int]: (当前页的文章列表，是否有下一页，当前页码，总页数)
        """
        # 1. 加载并排序文章
        all_articles = self._load_and_sort_articles_by_url(url)
        
        # 2. 分页处理
        return self._paginate_articles(items=all_articles, page_size=page_size, page=page)
    
    def update_articles_history(self, url: str, new_articles: List[Dict[str, str]]):
        """
        1. 把 RSS 订阅源的最新文章 (new_articles) 添加到 articles_history.json 文件中;
        2. 如果文章链接已存在，则不重复添加。

        Args:
            url (str): RSS 源链接
            new_articles (List[Dict[str, str]]): 新获取的文章列表
        """
        # 从 articles_history.json 文件中加载所有订阅源及其文章
        articles_history = self.file_handler.load_articles_history(self.articles_history_file)
        
        # 获取目标订阅源的现有文章
        existing_articles = articles_history.get(url, [])
        # 创建一个集合用于快速查找现有文章链接
        existing_links = {article['link'] for article in existing_articles}
        
        # 只添加新文章（通过链接去重）
        for article in new_articles:
            if article['link'] not in existing_links:
                existing_articles.append(article)
                existing_links.add(article['link'])

        # 更新历史记录
        articles_history[url] = existing_articles
        
        # 保存到文件
        self.file_handler.save_articles_history(self.articles_history_file, articles_history)
