1. ### 下载本项目
    安装git，打开cmd或powershell执行以下命令下载项目
    ```shell
    git clone https://github.com/wakening/mc_auto_boss.git
    cd mc_auto_boss
    ```
2. ### 安装 python 3.10.x
    双击python-3.10.11-amd64.exe    
    点击Add python.exe to Path    
    一直点下一步完成安装

3. ### 安装 CUDA 12
    下载 CUDA 12.x：https://developer.nvidia.com/cuda-toolkit-archive    
    如CUDA 12.6，安装，自定义，取消勾选其他组件，只勾选安装CUDA
    
    下载cuDNN v8.9.7, for CUDA 12.x
    https://developer.nvidia.com/rdp/cudnn-archive    
    解压zip文件，将所有文件夹（如：bin include lib）复制到路径内：C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\
    
4. ### 安装依赖
   打开cmd或powershell执行以下命令：    
   1.安装paddlepaddle-gpu，官方地址：[https://www.paddlepaddle.org.cn/install/quick](https://www.paddlepaddle.org.cn/install/quick)
   打开网址后，    
   选择2.6 windows pip 英伟达 CUDA12.0，复制链接执行    
  （此链接可能随官方更新失效，建议使用官网最新的链接）：
   ```shell
   python -m pip install paddlepaddle-gpu==2.6.1.post120 -f https://www.paddlepaddle.org.cn/whl/windows/mkl/avx/stable.html
   ```
    2.安装onnxruntime-gpu：
   ```shell
   pip install onnxruntime-gpu==1.18.0 --extra-index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/
   ```
    3.安装剩余依赖：
    ```shell
   pip install --upgrade -r requirements_gpu_cuda12.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

