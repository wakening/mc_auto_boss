# 更新日志, 点这里: [跳转](background/version.py)

# 鸣潮后台自动刷BOSS声骸 GPU

> 如果觉得项目不错，可以点个star支持一下，谢谢！
> 
>  点击链接加入QQ频道：[mc_auto_boss](https://pd.qq.com/s/ayygl9edg)
> 
> 后台运行时可以有其他窗口遮挡，但是不可以最小化
> 
> 代码仅供学习交流，不得用于商业用途，未对游戏进行任何修改，不会对游戏平衡性产生影响，如有侵权请联系删除。
> 
> 本项目基于python3.10开发,如果有问题请先查看：[常见问题](https://github.com/lazydog28/mc_auto_boss/wiki/%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98)
> 
> 仍有问题请提交issue

## 前置条件

1. 游戏窗口仅支持16:9分辨率,推荐分辨率为1280x720,屏幕缩放为100%
2. 必须解锁借位信标，在击杀目标BOSS的战利品位置放置借位信标，保证传送到借位信标后能直接触发BOSS或者和声弦交互
3. 脚本必须以管理员权限运行！
4. 项目路径中不能包含中文或特殊字符
5. 请将设置界面中控制选项下的 `镜头重置` 打开！
![1717844361594.png](https://hermes981128.oss-cn-shanghai.aliyuncs.com/ImageBed/1717844361594.png)
6. [推荐游戏设置](https://github.com/lazydog28/mc_auto_boss/wiki/%E6%8E%A8%E8%8D%90%E6%B8%B8%E6%88%8F%E8%AE%BE%E7%BD%AE)（如果运行有问题，请确保游戏内的设置与推荐游戏设置一致）
7. 请确保背包里面至少有一个复活药剂，`是否判断角色是否阵亡`功能是通过检查药剂使用弹窗实现，无任何药剂则不会有弹窗！

## 使用方法

任选一个教程搭建环境
> GPU环境搭建：[40系显卡，CUDA12环境搭建.md](CUDA12环境搭建.md)    
> GPU环境搭建：[GPU环境搭建 · lazydog28/mc_auto_boss Wiki (github.com)](https://github.com/lazydog28/mc_auto_boss/wiki/GPU环境搭建)

1. ### 下载本项目
    ```shell
    git clone https://github.com/lazydog28/mc_auto_boss.git
    cd mc_auto_boss
    ```
2. ### 安装依赖
    ```shell
    pip install -r requirements.txt
    ```
   > 当前为GPU分支，使用的模型为`paddleocr`提供的模型进行识别，如果需要使用其他OCR引擎，请自行修改代码
   >
   >  `paddlepaddle-gpu` 官方地址：[https://www.paddlepaddle.org.cn/install/quick](https://www.paddlepaddle.org.cn/install/quick)
   > 
   > 如果当前用户名为中文，请下载 `paddleocr` [模型文件](https://github.com/PaddlePaddle/PaddleOCR/blob/main/doc/doc_ch/models_list.md) 后自行修改`background/ocr.py`中实例化`PaddleOCR`的参数`det_model_dir`和`rec_model_dir`为绝对路径且不包含中文

    

3. ### 修改配置文件
    程序默认使用config.yaml作为配置文件，创建你的配置文件：
    ```shell
    cp config.example.yaml config.yaml
    ```
   修改`config.yaml`中的配置项，主要是 TargetBoss 将你要刷的BOSS名称前的 #井号 删除，
   回到游戏，在BOSS领取奖励位置放置借位信标


4. ### 运行项目
   请在运行之前保证游戏已经打开
    ```shell
    python background/main.py
    ```
   
   请在提示 `初始化完成` 后按 `F5` 开始刷BOSS
   
   | 快捷键 | 功能      |
   |-----|---------|
   | F5  | 开始刷BOSS |
   | F6  | [开始合成声骸](https://github.com/lazydog28/mc_auto_boss/wiki/%E5%A3%B0%E9%AA%B8%E8%9E%8D%E5%90%88%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B)  |
   | F7  | 暂停运行    |
   | F8  | 锁定声骸    |
   | F12 | 停止运行    |

5. ### 命令行参数
    ```shell
    # 例：使用自定义配置文件启动程序，并在启动后直接打boss
    python background/main.py -t F5 -c config-dreamless.yaml
    python background/main.py --task=F5 --config=config-dreamless.yaml
    # 例启动后先合成再打无妄者：
    python background/main.py -t F6,F5 -c config-dreamless.yaml
    # 例启动后先打开背包锁定有用声骸，再合成掉无用声骸，再打无妄者：
    python background/main.py -t F8,F6,F5 -c config-dreamless.yaml
    ```
   
   | 参数            | 功能              |
   |---------------|-----------------|
   | -t / --task   | 启动后执行的任务，值为快捷键  |
   | -c / --config | 指定配置文件，需放在项目根目录 |

6. ### 战斗策略
   | 策略           | 说明         |
   |--------------|------------|
   | `a`          | 鼠标左键 普攻    |
   | `s`          | space 空格跳跃 |
   | `e`、`q`、`r`  | 技能、声骸、大招   |
   | `0.5`        | 等待0.5秒     |
   | `a~ `        | 重击（按下0.5秒） |
   | `e~ `        | 按下E键0.5秒   |
   | `a~2`        | 按下鼠标左键2秒,  |
   | `e~2`        | 按下E键2秒,    |

7. ### 非NVIDIA显卡需切换依赖
   非N卡用户在完成GPU环境搭建以及项目配置后
   在项目路径内打开终端逐行执行如下命令即可完成依赖切换并正常使用
    ```shell
    conda activate mc
    pip uninstall onnxruntime-gpu
    pip uninstall paddlepaddle-gpu
    pip install -r requirements_cpu.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```

8. ### todo
	* ~~优化内存占用~~
	* ~~记录战斗次数及吸取次数~~
	* ~~掉落声骸目标识别进行拾取~~
    * ~~数据坞自动合成紫色声骸~~
