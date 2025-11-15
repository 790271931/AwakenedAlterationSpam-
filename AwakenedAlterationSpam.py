# -*- coding: utf-8 -*-
"""
流放之路（Path of Exile）觉醒改造石自动刷属性脚本

这个脚本用于自动使用觉醒改造石来刷物品属性，直到找到符合指定正则表达式的属性为止。
脚本会自动复制物品信息、检查是否匹配目标属性，如果不匹配则继续使用改造石。

快捷键：
- Shift+= : 开始刷新
- Shift+- : 停止刷新
- Ctrl+C : 手动退出程序

注意：请确保游戏窗口处于活跃状态，鼠标悬停在要刷新的物品上。
"""

import keyboard  # 用于监听全局热键
import pyautogui  # 用于模拟鼠标点击和键盘操作
import pyperclip  # 用于读取剪贴板内容
import time  # 用于延时控制
import re  # 用于正则表达式匹配
import sys  # 用于系统操作（退出程序）
import random  # 用于生成随机等待时间

safety_limit = 200  # 退出前的最大尝试次数（安全限制）

# 全局状态变量
running = False  # 程序运行状态标志
user_regex = "导师的|女王的|女皇的|法术主动"  # 用户输入的正则表达式

def extract_item_name(text: str):
    """
    从POE物品tooltip文本中提取物品名称
    
    参数:
        text (str): 从剪贴板复制的完整物品信息文本
    
    返回:
        str: 提取出的物品名称（去除稀有度标识和分隔线之间的内容）
    """
    lines = text.splitlines()
    capture = False  # 是否开始捕获物品名称
    extracted = []  # 存储提取的物品名称行

    for line in lines:
        if line.startswith("Rarity:") or line.startswith("稀有度") or line.startswith("稀 有 度"):  # 找到稀有度标识行
            capture = True  # 开始捕获下一行的物品名称
            continue
        if line.strip() == "--------" and capture:  # 遇到分隔线则停止捕获
            break
        if capture:  # 如果正在捕获状态，则添加当前行
            extracted.append(line)

    return "\n".join(extracted)  # 将提取的行组合成完整的物品名称

def start():
    """
    开始自动刷新觉醒改造石的主要函数
    
    该函数会循环执行以下步骤：
    1. 复制当前鼠标悬停物品的信息到剪贴板
    2. 解析物品名称
    3. 检查是否匹配用户指定的正则表达式
    4. 如果匹配则退出，否则点击继续使用改造石
    5. 重复直到达到安全限制次数
    """
    print("1秒后开始运行，请将鼠标悬停在物品上...")
    time.sleep(1)
    global running, user_regex
    if not running:
        running = True
        print("程序已启动。")

        attempts = 0  # 当前尝试次数
        attempt_width = len(str(safety_limit))  # 根据安全限制数字对齐输出宽度

        while attempts < safety_limit and running:
            # 复制当前物品信息到剪贴板
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.05)  # 等待复制完成
            raw_text = pyperclip.paste()  # 获取剪贴板内容
            search_item_text = raw_text

            # 提取并清理物品名称
            # item_name = extract_item_name(raw_text)
            # item_name = "".join(line.lstrip() for line in item_name.splitlines())  # 移除行首空白字符

            # 检查是否匹配正则表达式
            # if re.search(user_regex, item_name):
            if re.search(user_regex, search_item_text):
                print("找到匹配项！程序退出。")
                # sys.exit(0)  # 成功退出程序
                break

            # 打印格式化的尝试日志
            print(f"尝试 {str(attempts + 1).rjust(attempt_width)}: 正则表达式: {user_regex} 物品名称: {search_item_text}")
            pyautogui.click()  # 点击使用改造石
            attempts += 1
            time.sleep(random.uniform(0.1, 0.3))  # 等待动画完成

        print(f"已达到安全限制 {safety_limit} 次尝试。程序退出。")
        running = False

def stop():
    """
    停止自动刷新程序
    
    将运行状态设置为False，停止当前的刷新循环
    """
    global running
    if running:
        running = False
        keyboard.unhook_all_hotkeys()  # 移除所有热键监听
        print("程序已停止。")

def main():
    """
    主程序入口，设置热键监听并启动主循环
    """
    global safety_limit, user_regex
    # 询问用户设置安全限制（如果输入无效则默认为40）
    try:
        user_input = input(f"请输入安全限制 [{safety_limit}] (自动停止前的最大尝试次数): ").strip()
    except ValueError:
        pass
    print(f"使用安全限制: {safety_limit}")

    # 询问用户输入匹配物品名称的正则表达式
    # user_regex = input("请输入匹配物品名称的正则表达式: ")
    print(f"使用正则表达式: {user_regex}")

    # 设置全局热键
    keyboard.add_hotkey('shift+=', start)  # Shift+= 开始刷新
    keyboard.add_hotkey('shift+-', stop)   # Shift+- 停止刷新

    print("等待 Shift+= 开始刷新，Shift+- 停止刷新。")
    print("如需手动退出，请按 Ctrl+C。")

    # 主程序循环
    try:
        while True:
            time.sleep(1)  # 保持程序运行，等待热键触发
    except KeyboardInterrupt:
        print("\n收到 Ctrl+C 信号，程序退出")

def test():
    """
    测试函数，用于调试和验证功能
    """
    time.sleep(5)  # 给用户5秒时间准备
    print("test程序已启动。")
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.05)  # 等待复制完成
    raw_text = pyperclip.paste()  # 获取剪贴板内容
    print("剪切板内容如下：")
    print(raw_text)

    if re.search(user_regex, raw_text):
        print("找到匹配项！程序退出。")
        keyboard.unhook_all_hotkeys()  # 移除所有热键监听
    else:
        print("未找到匹配项。")


if __name__ == "__main__":
    main()
    # test()
