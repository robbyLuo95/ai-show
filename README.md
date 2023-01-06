##项目概述
    yolov5图片识别以及orc文字图片识别
##安装环境
    python 3.8.1以上
###安装依赖
    pip install -r requirements.txt
    //因为本地电脑不是英伟达的显卡，模型的加载，安装cpu版本的pytorch
    pip install torch==1.7.0+cpu torchvision==0.8.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

###启动flask服务
    python app.py
    