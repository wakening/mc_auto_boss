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
from utils import *


def isNumber_isloading(keyword, screenshot):
    text = pytesseract.image_to_string(screenshot)
    if re.search(r'\b' + keyword + r'\b', text):
        return True
    else:
        return False


def isNumber_isloading_disPlay(screenshot):
    # 使用 pytesseract 识别截图中的文字
    text = pytesseract.image_to_string(screenshot)

    # 检查识别到的文字是否包含数字
    if any(char.isdigit() for char in text):
        return text
    else:
        return None


def isNumber_isloading_disPlays():
    """
    检查游戏《鸣潮》的加载进度，以确定是否卡加载进度。

    该函数通过捕获游戏窗口的文本信息，判断加载进度是否达到要求。
    如果加载进度匹配的对应的值超过，则认为游戏卡加载进度，关闭加载窗口，结束检查。
    """
    last_number = None  # 上一次识别到的数字
    appear_count = 0  # 连续出现的次数
    number = 0  # OCR识别的进度值
    interval = 0.2  # OCR间隔时间
    weight = 0.8  # 权重
    # timeout = 超时的时间/权重
    timeout = config.ISLoadingTimeout / weight
    while True:
        try:
            time.sleep(interval)
            # 获取游戏窗口的加载进度文本
            text = isNumber_isloading_disPlay(capture_window(win32gui.FindWindow(None, "鸣潮  ")))
            # 将文本中的百分号去除，转换为整数
            number = int(text.replace('%', ''))
            if last_number is not None and number == last_number:
                appear_count += 1
            else:
                appear_count = 0  # 出现的数字和上一次不一样，置0
                logger("地图加载进度：" + text)  # 出现的数字和上一次不一样, 打印日志
            if appear_count >= (round(timeout / interval * weight)):  # 加载进度超时，则认为游戏卡加载进度，关闭加载窗口，结束检查
                logger(f"监测到游戏在{config.ISLoadingTimeout}s内连续卡在进度{text}, 关闭游戏",
                       "WARN")
                close_window(None, "鸣潮  ")
                return
            last_number = number  # 必须做的，将ocr识别到的赋值给临时变量 last_number
        except Exception as e:
            # 出现异常，结束循环
            # logger("卡进度检测结束，没有检测到卡进度")
            return


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
