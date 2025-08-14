import os
import json
import requests

# 测试文件操作
def test_file_operations():
    # 造一个测试数据，参数为 name & url
    test_data = {
        "name": "test",
        "url": "https://feeds.feedburner.com/ruanyifeng"
    }

    # 把测试数据写入文件 test.json
    with open("test.json", "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    # 读取文件内容并打印
    with open("test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        print(data)

# 获取指定目录下的文件列表
def get_file_list(directory):
    return os.listdir(directory)

# 检查用户输入的文件是否存在
# 输入文件名和目录，如果文件存在，返回 True；否则返回 False
def file_exists(file_name: str, directory: str) -> bool:
    # 获取指定目录下的文件列表
    file_list = get_file_list(directory)
    # 检查文件是否在列表中
    return file_name in file_list

# 使用 os.path.exists() 检查文件是否存在
def file_exists_v2(file_name: str, directory: str) -> bool:
    file_path = os.path.join(directory, file_name)
    return os.path.exists(file_path)

# 主函数
if __name__ == "__main__":
    # 测试文件操作
    test_file_operations()
