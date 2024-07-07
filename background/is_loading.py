import time
import pytesseract
import win32con
import win32gui
import pyautogui
import cv2
import numpy as np
import re
from concurrent.futures import ThreadPoolExecutor, as_completed  # 导入ThreadPoolExecutor和as_completed，用于并发执行任务
from config import config

def isNumber_isloading(keyword, screenshot):
    text = pytesseract.image_to_string(screenshot)
    if re.search(r'\b' + keyword + r'\b', text):
        return True
    else:
        return False

def capture_window(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)  # 获取窗口的位置和大小
    width = right - left  # 计算窗口宽度
    height = bottom - top  # 计算窗口高度
    if (width >= 1280 and height >= 720):
        screenshot = pyautogui.screenshot(region=(right - 250, bottom - 200, 200, 160))  # 截取窗口右下角区域
    elif (width >= 1920 and height >= 1080):
        screenshot = pyautogui.screenshot(region=(right - 250, bottom - 200, 240, 140))  # 截取窗口右下角区域
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)  # 将图片从RGB格式转换为BGR格式
    return screenshot


def find_keyword_loading(keyword):
    hwnd = win32gui.FindWindow(None, "鸣潮  ")
    detection_count = config.IsLoadingJueTime  # 检测次数
    right_amount = 0  # 正确次数
    weight = 0.8  # 权重
    for i in range(detection_count):
        screenshot = capture_window(hwnd)  # 获取到截取的图片
        if isNumber_isloading(keyword, screenshot):  # 判断是否包含关键词
            right_amount += 1
        time.sleep(1)  # 每秒截图1次
    if right_amount >= round(detection_count * weight):  # 默认8秒中内有6秒检测出10或者75(并发)，则返回True
        return True
    else:
        return False

def check_results():
    keywords = ['10', '75']  # 关键词列表
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(find_keyword_loading, keywords))  # 使用线程池并发搜索关键字
    for result in results:
        if result:
            return True
    return False


# 关闭窗口
def close_window(class_name, window_title):
    # 尝试关闭窗口，如果成功返回 True，否则返回 False
    hwnd = win32gui.FindWindow(class_name, window_title)
    if hwnd != 0:
        win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        # 等待窗口关闭
        time.sleep(2)
        if win32gui.FindWindow(class_name, window_title) == 0:
            return True
    return False
