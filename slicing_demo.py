#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 切片（slicing）规则演示
"""

def demo_slicing():
    """演示 Python 切片的各种用法"""
    
    print("=== Python 切片规则演示 ===\n")
    
    # 创建一个示例列表
    items = ['A', 'B', 'C', 'D', 'E', 'F']
    print(f"原始列表: {items}")
    print("索引对照:")
    for i, item in enumerate(items):
        print(f"  索引 {i}: '{item}'")
    
    print("\n" + "="*50)
    
    # 各种切片示例
    print("\n1. [:3] 的含义:")
    result = items[:3]
    print(f"  items[:3] = {result}")
    print(f"  解释: 从开始到索引3（不包括索引3）")
    print(f"  实际取到: 索引 0, 1, 2")
    
    print("\n2. [0:3] 的含义（与 [:3] 相同）:")
    result = items[0:3]
    print(f"  items[0:3] = {result}")
    print(f"  解释: 从索引0到索引3（不包括索引3）")
    
    print("\n3. [:4] 会取多少个？")
    result = items[:4]
    print(f"  items[:4] = {result}")
    print(f"  解释: 取4个元素（索引 0, 1, 2, 3）")
    
    print("\n4. [1:4] 从中间切片:")
    result = items[1:4]
    print(f"  items[1:4] = {result}")
    print(f"  解释: 从索引1到索引4（不包括索引4）")
    
    print("\n5. 更多切片示例:")
    examples = [
        ("[:1]", items[:1], "取第1个"),
        ("[:2]", items[:2], "取前2个"),
        ("[:5]", items[:5], "取前5个"),
        ("[2:]", items[2:], "从索引2到结尾"),
        ("[-3:]", items[-3:], "取最后3个"),
        ("[1:-1]", items[1:-1], "去掉首尾"),
    ]
    
    for notation, result, explanation in examples:
        print(f"  items{notation} = {result} ({explanation})")

def visual_demo():
    """可视化演示切片"""
    print("\n" + "="*50)
    print("可视化演示 [:3] 的工作原理:")
    print()
    
    items = ['第0个', '第1个', '第2个', '第3个', '第4个']
    
    print("列表元素和索引:")
    print("索引:  0      1      2      3      4")
    print("元素: ", end="")
    for item in items:
        print(f"{item:6}", end=" ")
    print()
    
    print("\n[:3] 切片范围:")
    print("      ├──────┼──────┼──────┤")
    print("      取这些元素（0,1,2）   │")
    print("                            停在这里（不包括索引3）")
    
    print(f"\n结果: {items[:3]}")

if __name__ == "__main__":
    demo_slicing()
    visual_demo()
