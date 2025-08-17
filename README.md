# RSS Reader

一个功能完整的 RSS 订阅管理器，支持订阅管理、文章缓存、分页浏览和丰富的控制台界面。

## 功能特性

- 📰 RSS 订阅源管理（添加/删除）
- 📚 文章历史缓存和分页浏览
- 🎨 美观的 Rich 控制台界面
- 🔄 文章刷新和去重
- 🌐 浏览器集成（点击链接打开文章）
- ⚡ 模块化架构，易于扩展

## 项目结构

```
rss/
├── rss_reader/              # 主要模块包
│   ├── __init__.py         # 包初始化文件
│   ├── models.py           # 数据模型和枚举
│   ├── file_handler.py     # 文件操作处理
│   ├── article_manager.py  # 文章管理逻辑
│   ├── rss_parser.py      # RSS解析和网络请求
│   ├── subscription_manager.py # 订阅管理
│   ├── ui.py              # 用户界面
│   └── main.py            # 主程序控制器
├── demo/                   # 旧版本代码（参考）
├── run.py                  # 应用启动脚本
├── requirements.txt        # 项目依赖
└── README.md              # 项目说明文档
```

## 模块说明

### 核心模块

1. **models.py** - 数据模型
   - `NavigationAction`: 导航动作枚举

2. **file_handler.py** - 文件操作
   - `FileHandler`: JSON 文件读写操作

3. **article_manager.py** - 文章管理
   - `ArticleManager`: 文章历史存储、检索和分页

4. **rss_parser.py** - RSS 解析
   - `RssParser`: 网络请求和 RSS 源解析

5. **subscription_manager.py** - 订阅管理
   - `SubscriptionManager`: 订阅的增删改查

6. **ui.py** - 用户界面
   - `UserInterface`: 用户交互和界面显示

7. **main.py** - 主程序
   - `RssApp`: 应用主控制器

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行程序

### 方式一：使用启动脚本
```bash
python run.py
```

### 方式二：直接运行主模块
```bash
python -m rss_reader.main
```

### 方式三：作为包使用
```python
from rss_reader import RssApp

app = RssApp()
app.run()
```

## 设计原则

### 模块化设计
- 每个模块都有单一职责
- 低耦合，高内聚
- 便于单独测试和维护

### 依赖关系
```
main.py
└── ui.py
    ├── subscription_manager.py
    │   ├── file_handler.py
    │   └── rss_parser.py
    │       └── article_manager.py
    │           └── file_handler.py
    ├── article_manager.py
    └── models.py
```

### 数据持久化
- `subscriptions.json`: 订阅列表
- `articles_history.json`: 文章历史缓存

## 扩展指南

### 添加新功能
1. 在相应模块中添加新方法
2. 如需新的数据模型，在 `models.py` 中定义
3. 在 `ui.py` 中添加对应的界面交互
4. 在 `main.py` 中添加控制逻辑

### 自定义配置
可以在各个类的 `__init__` 方法中修改默认参数：
- 文件名
- 超时时间
- 分页大小
- 文章获取数量

## 版本历史

- v0.0.1: 初始模块化版本
  - 将单文件重构为多模块架构
  - 保持原有功能完整性
  - 提升代码可维护性
