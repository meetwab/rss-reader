# 🚀 Python RSS项目 - 快速参考卡

## 📋 目录导航
- [基础语法](#基础语法)
- [常用库](#常用库)
- [调试技巧](#调试技巧)
- [常见错误](#常见错误)
- [实用代码片段](#实用代码片段)

---

## 🐍 基础语法

### **类和对象**
```python
class RSSReader:
    def __init__(self):                    # 构造函数
        self.config_file = "config.json"   # 实例变量
        self.subscriptions = {}
    
    def add_subscription(self, name: str): # 实例方法
        # self 指向当前实例
        pass
```

### **异常处理**
```python
try:
    # 可能出错的代码
    with open("file.json", "r") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
finally:
    # 无论是否异常都会执行
    print("清理工作")
```

### **文件操作**
```python
# 读取文件
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 写入文件
with open("file.txt", "w", encoding="utf-8") as f:
    f.write("内容")

# JSON操作
import json
data = {"name": "test"}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### **列表和字典**
```python
# 列表操作
articles = []
articles.append({"title": "标题"})        # 添加
articles.extend(other_list)               # 合并
filtered = [a for a in articles if condition]  # 列表推导

# 字典操作
config = {}
config["key"] = "value"                   # 添加
value = config.get("key", "default")      # 安全获取
for key, value in config.items():         # 遍历
    print(f"{key}: {value}")
```

### **字符串操作**
```python
text = "  Hello World  "
text.strip()           # 去空格
text.lower()           # 转小写
text.startswith("H")   # 检查开头
text.replace("H", "h") # 替换

# f-string格式化
name = "Python"
print(f"欢迎使用 {name}！")
```

---

## 📚 常用库

### **requests - HTTP请求**
```python
import requests

# 基本请求
response = requests.get(url, timeout=10)
response.raise_for_status()  # 检查HTTP错误
content = response.content   # 获取内容

# 带头部的请求
headers = {'User-Agent': 'My RSS Reader'}
response = requests.get(url, headers=headers)

# 异常处理
try:
    response = requests.get(url, timeout=10)
except requests.exceptions.Timeout:
    print("请求超时")
except requests.exceptions.ConnectionError:
    print("连接失败")
```

### **feedparser - RSS解析**
```python
import feedparser

# 解析RSS
feed = feedparser.parse(rss_content)

# 获取文章信息
for entry in feed.entries:
    title = entry.get('title', '无标题')
    link = entry.get('link', '')
    summary = entry.get('summary', '')
    published = entry.get('published', '')
```

### **datetime - 时间处理**
```python
from datetime import datetime

# 当前时间
now = datetime.now()
formatted = now.strftime('%Y-%m-%d %H:%M:%S')

# 时间戳
timestamp = now.isoformat()
```

### **os - 系统操作**
```python
import os

# 文件操作
os.path.exists(filename)     # 检查文件存在
os.makedirs(dirname)         # 创建目录
os.listdir(directory)        # 列出目录内容

# 路径操作
path = os.path.join("dir", "file.txt")  # 跨平台路径
dirname = os.path.dirname(path)         # 获取目录名
```

---

## 🐛 调试技巧

### **打印调试**
```python
def debug_function(self, param):
    print(f"DEBUG: 函数开始，参数={param}")
    print(f"DEBUG: self.subscriptions={self.subscriptions}")
    
    # 处理逻辑...
    
    print(f"DEBUG: 函数结束")
```

### **断点调试**
```python
import pdb

def problematic_function():
    pdb.set_trace()  # 程序会在此暂停
    # 调试命令：
    # n - 下一行
    # s - 进入函数
    # c - 继续执行
    # p variable_name - 打印变量
    # l - 显示当前代码
```

### **日志记录**
```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 使用日志
logger.debug("调试信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("错误信息")
```

---

## ❌ 常见错误

### **ModuleNotFoundError**
```bash
# 问题：import requests 失败
# 解决：
pip install requests feedparser

# 或指定Python版本
pip3 install requests feedparser
```

### **JSON解析错误**
```python
# 问题：json.decoder.JSONDecodeError
# 解决：
try:
    with open(config_file, 'r') as f:
        data = json.load(f)
except json.JSONDecodeError:
    print("JSON格式错误，重置配置")
    data = {}
```

### **编码问题**
```python
# 问题：UnicodeDecodeError 
# 解决：指定编码
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

# JSON保存中文
json.dump(data, f, ensure_ascii=False, indent=2)
```

### **网络请求失败**
```python
# 问题：requests.exceptions.RequestException
# 解决：添加错误处理
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.Timeout:
    print("请求超时")
except requests.exceptions.HTTPError as e:
    print(f"HTTP错误: {e}")
```

---

## 💡 实用代码片段

### **配置文件管理**
```python
class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
```

### **URL验证**
```python
def validate_url(url):
    from urllib.parse import urlparse
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
```

### **HTML清理**
```python
def clean_html(text):
    import re
    # 移除HTML标签
    clean = re.sub(r'<[^>]+>', '', text)
    # 解码HTML实体
    import html
    return html.unescape(clean).strip()
```

### **安全请求**
```python
def safe_request(url, timeout=10):
    headers = {
        'User-Agent': 'Mozilla/5.0 RSS Reader'
    }
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
    except Exception as e:
        print(f"请求失败: {e}")
        return None
```

### **数据去重**
```python
def remove_duplicates(items, key_func=None):
    """去除列表中的重复项"""
    if key_func is None:
        return list(set(items))
    
    seen = set()
    result = []
    for item in items:
        key = key_func(item)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result

# 使用示例
unique_articles = remove_duplicates(articles, lambda x: x['link'])
```

### **简单缓存**
```python
class SimpleCache:
    def __init__(self, expire_minutes=60):
        self.cache = {}
        self.expire_minutes = expire_minutes
    
    def get(self, key):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if (datetime.now() - timestamp).total_seconds() < self.expire_minutes * 60:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key, data):
        self.cache[key] = (data, datetime.now())
```

### **进度显示**
```python
def show_progress(current, total, prefix="进度"):
    """显示简单的进度条"""
    percentage = (current / total) * 100
    bar_length = 20
    filled = int(bar_length * current // total)
    bar = "█" * filled + "-" * (bar_length - filled)
    print(f"\r{prefix}: |{bar}| {percentage:.1f}% ({current}/{total})", end="")
    if current == total:
        print()  # 完成后换行
```

---

## 🎯 快速命令

### **测试代码**
```bash
# 运行特定脚本
python rss_reader.py

# 交互式测试
python3 -c "from rss_reader import RSSReader; r=RSSReader(); print(r.subscriptions)"

# 模块导入测试
python3 -c "import requests, feedparser; print('依赖库正常')"
```

### **文件操作**
```bash
# 查看文件内容
head -20 rss_reader.py    # 前20行
tail -20 rss_reader.py    # 后20行
wc -l rss_reader.py       # 统计行数

# 搜索代码
grep -n "def " rss_reader.py        # 查找所有函数
grep -n "class " rss_reader.py      # 查找所有类
```

### **Python环境**
```bash
# 查看Python版本
python --version

# 查看已安装包
pip list

# 安装包
pip install package_name

# 创建虚拟环境
python -m venv venv_name
source venv_name/bin/activate  # macOS/Linux
```

---

## 📖 学习检查清单

### **基础概念** ✅
- [ ] 理解类和对象的概念
- [ ] 掌握异常处理机制
- [ ] 熟悉文件操作和JSON处理
- [ ] 会使用字典和列表

### **网络编程** 🌐
- [ ] 会使用requests发送HTTP请求
- [ ] 理解RSS/XML的基本结构
- [ ] 能处理网络请求异常
- [ ] 掌握feedparser的使用

### **实用技能** 🛠️
- [ ] 能设计简单的用户界面
- [ ] 会组织代码结构
- [ ] 掌握调试技巧
- [ ] 能解决常见问题

### **进阶能力** 🚀
- [ ] 能独立设计和实现新功能
- [ ] 理解代码重构和优化
- [ ] 会编写测试代码
- [ ] 能帮助他人解决问题

---

**💡 提示：将此卡片保存到手机或打印出来，随时查阅！**
