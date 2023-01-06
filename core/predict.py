import cv2
import os
import datetime

def predict(dataset, model, ext):
    global img_y
    x = dataset[0].replace('\\', '/')
    file_name = dataset[1]
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    x = cv2.imread(x)
    img_y, image_info = model.detect(x)
    path = 'tmp/draw/'+str(year)+'/'+str(month)
    if not os.path.exists(path):
        os.makedirs(path)
    url = 'tmp/draw/'+str(year)+'/'+str(month)+'/{}.{}'.format(file_name, ext)
    if cv2.imwrite(url, img_y) == False:
        raise Exception('保存图片时出错.Error saving thepicture.')
    return image_info
