# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: ocr.py
@time: 2024/6/5 下午4:36
@author SuperLazyDog
"""
import time
import paddle
from paddleocr import PaddleOCR
from multiprocessing import current_process
import numpy as np
from schema import OcrResult, Position
from config import config
import logging
from status import logger,info


ocrIns: PaddleOCR = None

if paddle.is_compiled_with_cuda() and paddle.get_device().startswith("gpu"):  # 判断是否调用GPU
    use_gpu = True
else:
    use_gpu = False

if current_process().name == "task":
    logger("OCR初始化中...")
    logging.disable(logging.WARNING)  # 关闭WARNING日志的打印
    ocrIns = PaddleOCR(use_angle_cls=False, use_gpu=use_gpu, lang="ch", show_log=False)

last_time = time.time()

def ocr_switch():
    info.useGpu = not info.useGpu

def ocr_switch_cpu():
    if info.useGpu == True:
        info.useGpu = False

def ocr_switch_gpu():
    if info.useGpu == False:
        info.useGpu = True

status_use:bool = None
def init_ocr():
    if config.IntelligentSceneSwitching:
        global ocrIns
        global use_gpu
        global status_use
        if use_gpu == True:
            if status_use !=None and (status_use == info.useGpu):
            #  logger(f"默认使用【GPU】识别","DEBUG") if info.useGpu == True else logger(f"默认使用【CPU】识别","DEBUG")
                if info.useGpu:
                    logger(f"默认使用【GPU】识别","DEBUG")
                else:
                    logger(f"默认使用【CPU】识别","DEBUG")
                return
            elif (status_use != info.useGpu):
                use_gpu_t = info.useGpu
                status_use  = use_gpu_t
                ocrIns = PaddleOCR(use_angle_cls=False, use_gpu=use_gpu_t, lang="ch",show_log=False)
                # logger(f"使用GPU识别") if use_gpu_t == True else logger(f"使用CPU识别")
                if use_gpu_t:
                    logger(f"使用【GPU】识别","DEBUG")
                else:
                    logger(f"使用【CPU】识别","DEBUG")


def ocr(img: np.ndarray) -> list[OcrResult]:
    global last_time
    if (
        config.OcrInterval > 0 and time.time() - last_time < config.OcrInterval
    ):  # 限制OCR调用频率
        if wait_time := config.OcrInterval - (time.time() - last_time) > 0:
            time.sleep(wait_time)
    last_time = time.time()
    results = ocrIns.ocr(img)[0]
    if not results:
        return []
    res = []
    for result in results:
        text = result[1][0]
        position = result[0]
        x1, y1, x2, y2 = position[0][0], position[0][1], position[2][0], position[2][1]
        position = Position(x1=x1, y1=y1, x2=x2, y2=y2)
        confidence = result[1][1]
        res.append(OcrResult(text=text, position=position, confidence=confidence))
    return res
