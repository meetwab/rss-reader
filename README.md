# RSS 终端阅读器

一个简单易用的 Python RSS 终端阅读器，专为学习 Python 的新手设计。

## 功能特性

- 📚 **订阅源管理**: 添加、删除、列出 RSS 订阅源
- 📰 **文章阅读**: 获取并显示最新文章标题、摘要和发布日期
- 🌐 **浏览器打开**: 一键在默认浏览器中打开感兴趣的文章
- 💾 **数据持久化**: 自动保存订阅源配置到本地文件
- 🔄 **实时刷新**: 随时获取最新文章内容
- 🎨 **友好界面**: 清晰的菜单和丰富的 emoji 提示

## 安装和使用

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install requests feedparser
```

### 2. 运行程序

```bash
python rss_reader.py
```

### 3. 基本操作

1. **添加订阅源**: 选择菜单选项 2，输入 RSS 链接
2. **查看订阅列表**: 选择菜单选项 1
3. **阅读文章**: 选择菜单选项 4，然后选择要阅读的订阅源
4. **删除订阅源**: 选择菜单选项 3

## 推荐的 RSS 源

以下是一些不错的中文 RSS 源供测试使用：

- **少数派**: https://sspai.com/feed
- **阮一峰的网络日志**: http://www.ruanyifeng.com/blog/atom.xml  
- **酷壳**: https://coolshell.cn/feed
- **V2EX**: https://www.v2ex.com/index.xml

## 项目结构

```
rss/
├── rss_reader.py          # 主程序文件
├── requirements.txt       # 依赖文件
├── README.md             # 说明文档
└── rss_subscriptions.json # 订阅配置文件 (程序运行后自动生成)
```

## 代码学习要点

这个项目涵盖了 Python 新手需要掌握的多个重要概念：

### 1. 基础语法
- 类和对象的使用
- 函数定义和调用
- 异常处理 (try/except)
- 字典和列表操作

### 2. 标准库使用
- `json`: 数据序列化和反序列化
- `os`: 文件系统操作
- `sys`: 系统相关功能
- `webbrowser`: 浏览器操作
- `re`: 正则表达式

### 3. 第三方库
- `requests`: HTTP 请求
- `feedparser`: RSS/Atom 解析

### 4. 软件设计概念
- 模块化设计
- 配置文件管理
- 用户交互界面
- 错误处理和用户反馈

## 扩展建议

当你熟练掌握基础功能后，可以尝试以下扩展：

1. **文章缓存**: 将已读文章保存到本地，避免重复下载
2. **关键词过滤**: 根据关键词筛选感兴趣的文章
3. **定时更新**: 使用 `schedule` 库实现定时获取最新文章
4. **导出功能**: 将文章导出为 Markdown 或 HTML 格式
5. **图形界面**: 使用 `tkinter` 或 `PyQt` 创建桌面应用
6. **Web 界面**: 使用 Flask 创建 Web 版本

## 故障排除

### 常见问题

1. **依赖库安装失败**
   ```bash
   # 使用国内镜像源
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests feedparser
   ```

2. **RSS 链接无法访问**
   - 检查网络连接
   - 确认 RSS 链接是否正确
   - 某些网站可能需要设置 User-Agent

3. **中文显示问题**
   - 确保终端支持 UTF-8 编码
   - macOS 和 Linux 通常没有问题
   - Windows 用户可能需要设置控制台编码

## 开发环境

- Python 3.6+
- 支持的操作系统: Windows, macOS, Linux

---

祝你学习愉快！🎉
