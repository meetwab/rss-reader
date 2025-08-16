# RSS 订阅管理器

一个基于 Python 的简洁 RSS 订阅管理工具，采用面向对象设计，提供命令行交互界面。

## 📋 项目概述

这个项目是一个 RSS（Really Simple Syndication）订阅管理器，允许用户添加、管理和阅读 RSS 订阅源。项目采用面向对象的架构设计，具有良好的代码组织和可维护性。

## ✨ 功能特性

- 📚 **RSS 订阅管理**：添加新的 RSS 订阅源
- 💾 **数据持久化**：自动保存订阅信息到本地 JSON 文件
- 📰 **文章阅读**：获取并显示最新文章的标题、链接和摘要
- 🔄 **实时刷新**：支持手动刷新文章列表
- 🎯 **智能导航**：层级式菜单导航，支持返回上级或主页
- 🛡️ **错误处理**：完善的异常处理机制，提供友好的错误提示
- 🧹 **内容清理**：自动清理 HTML 标签，提供纯文本阅读体验

## 🏗️ 项目架构

### 核心类设计

#### 1. `RssManager` 类

RSS 管理器的核心类，负责订阅的增删改查：

- `save_subscription(link: str)`: 保存新的 RSS 订阅
- `load_subscriptions(filename: str)`: 从文件加载订阅列表
- `view_subscriptions()`: 查看所有订阅并提供交互选择
- `view_single_subscription_articles()`: 查看单个订阅的文章列表

#### 2. `ArticleFetcher` 类

文章获取和处理的专用类：

- `fetch_latest_articles(url: str, count: int)`: 获取指定数量的最新文章
- `remove_html_tags(text: str)`: 清理 HTML 标签，保留纯文本
- `display_articles(articles: List[str])`: 格式化显示文章列表

#### 3. `NavigationAction` 枚举

定义用户导航动作，替代魔术字符串：

- `BACK_TO_LIST`: 返回订阅列表
- `BACK_TO_HOME`: 返回主页

### 文件结构

```text
demo/
├── demo.py              # 主程序文件
├── subscriptions.json   # 订阅数据存储文件
└── README.md           # 项目文档
```

## 🚀 快速开始

### 环境要求

- Python 3.6+
- 网络连接（用于获取 RSS 内容）

### 安装依赖

```bash
pip install requests feedparser
```

### 运行程序

```bash
cd demo
python demo.py
```

## 📖 使用指南

### 主菜单操作

启动程序后，你会看到主菜单：

```text
--- RSS 订阅管理 ---
1. 添加新的订阅
2. 查看所有订阅
0. 退出
```

### 添加订阅

1. 选择选项 `1`
2. 输入有效的 RSS 链接（例如：`https://www.v2ex.com/index.xml`）
3. 程序会自动获取订阅源的标题并保存

### 查看订阅

1. 选择选项 `2`
2. 浏览所有已保存的订阅列表
3. 输入序号进入特定订阅查看文章
4. 在文章列表中可以：
   - 按 `r` 刷新文章
   - 按 `b` 返回订阅列表
   - 按 `0` 返回主页

## 🔧 技术实现

### 核心技术栈

- **HTTP 请求**：使用 `requests` 库获取 RSS 内容
- **XML 解析**：使用 `feedparser` 库解析 RSS/Atom 格式
- **数据存储**：使用 JSON 格式进行本地数据持久化
- **文本处理**：使用正则表达式清理 HTML 内容

### 设计模式

- **单一职责原则**：每个类专注于特定功能
- **开闭原则**：易于扩展新功能而无需修改现有代码
- **枚举模式**：使用枚举类型提高代码可读性和安全性

## 🧪 推荐测试源

以下是一些可用于测试的 RSS 源：

- **V2EX**: `https://www.v2ex.com/index.xml`
- **阮一峰的网络日志**: `http://feeds.feedburner.com/ruanyifeng`
- **知乎**: `https://www.zhihu.com/rss`
- **少数派**: `https://sspai.com/feed`
- **酷壳**: `https://coolshell.cn/feed`

## 📝 数据格式

订阅信息存储在 `subscriptions.json` 文件中：

```json
{
  "V2EX": "https://www.v2ex.com/index.xml",
  "阮一峰的网络日志": "http://feeds.feedburner.com/ruanyifeng",
  "知乎": "https://www.zhihu.com/rss"
}
```

## 🛠️ 扩展建议

### 可能的功能扩展

1. **分类管理**：为订阅源添加分类功能
2. **搜索功能**：在文章中搜索关键词
3. **导出功能**：导出文章到文件
4. **定时更新**：自动定时获取最新文章
5. **GUI 界面**：开发图形用户界面
6. **数据库支持**：使用 SQLite 替代 JSON 存储

### 代码优化建议

1. **配置文件**：添加配置文件支持自定义设置
2. **日志系统**：添加日志记录功能
3. **单元测试**：编写测试用例确保代码质量
4. **异步处理**：使用异步 IO 提高性能
5. **内容缓存**：缓存文章内容减少网络请求

## 🐛 常见问题

### Q: 为什么有些 RSS 源无法添加？

A: 可能的原因包括：

- RSS 源链接无效或格式不正确
- 网络连接问题
- 服务器响应超时（默认 10 秒超时）

### Q: 文章摘要显示不完整怎么办？

A: 程序默认显示前 200 个字符的摘要，这是为了保持界面整洁。可以点击链接查看完整文章。

### Q: 如何备份我的订阅列表？

A: 直接复制 `subscriptions.json` 文件即可备份所有订阅信息。

## 📄 许可证

本项目采用 MIT 许可证，详情请查看 LICENSE 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

---

> 💡 **提示**: 这是一个学习项目，非常适合 Python 初学者了解面向对象编程、网络编程和文件操作等概念。
