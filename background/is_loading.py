import os  # 导入os模块，用于处理文件和目录操作
import cv2  # 导入cv2模块，用于图像处理
import numpy as np  # 导入numpy模块，用于数组操作
import win32gui  # 导入win32gui模块，用于Windows窗口操作
import pyautogui  # 导入pyautogui模块，用于自动化鼠标和键盘操作
import time  # 导入time模块，用于时间操作
import win32con
import random  # 导入random模块，用于生成随机数
from concurrent.futures import ThreadPoolExecutor, as_completed  # 导入ThreadPoolExecutor和as_completed，用于并发执行任务
from config import config
folder_path = os.path.join(config.project_root, "./isLoading") # 指定加载图片文件夹路径

def capture_window(hwnd):
    # 捕获指定窗口的屏幕截图
    time.sleep(random.uniform(0.1, 1.0))  # 等待随机时间
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)  # 获取窗口的位置和大小
    width = right - left  # 计算窗口宽度
    height = bottom - top  # 计算窗口高度
    img = pyautogui.screenshot(region=(left, top, width, height))  # 截取窗口区域的图片
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)  # 将图片从RGB格式转换为BGR格式
    return img

def compare_images(image1, image2):
    # 比较两张图片的相似度
    hist1 = cv2.calcHist([image1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])  # 计算第一张图片的直方图
    hist2 = cv2.calcHist([image2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])  # 计算第二张图片的直方图
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)  # 比较两个直方图的相关性

def find_similarity(img_name):
    # 查找指定图片与窗口截图的相似度
    hwnd = win32gui.FindWindow(None, "鸣潮  ")  # 查找窗口句柄
    if hwnd == 0:
        return
    # project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取项目根目录
    reference_image = cv2.imread(img_name)  # 读取参考图片
    count = 0  # 初始化相似计数器
    detection_count = config.IsLoadingJueTime  # 默认10秒内，每秒检测1次
    for i in range(detection_count):
        current_image = capture_window(hwnd)  # 捕获当前窗口截图
        similarity = compare_images(reference_image, current_image)  # 比较参考图片和当前截图的相似度
        if similarity > 0.8: # 相似度 高于阈值
            count += 1
        time.sleep(1)
    threshold = round(detection_count * 0.75)  # 设置相似度阈值
    if count > threshold:
        return True
    else:
        return False

def process_image(image_path):
    result = find_similarity(image_path)
    return result

def get_image_paths(folder_path):
    image_extensions = ['.png', '.jpg', '.jpeg']  # 根据需要添加其他图片格式
    image_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.endswith(ext) for ext in image_extensions):
                image_paths.append(os.path.join(root, file))
    return image_paths


def check_results():
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_image, get_image_paths(folder_path)))
    for result in results:
        if result:
            return True
    return False


# result = check_results()
# print(result)

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