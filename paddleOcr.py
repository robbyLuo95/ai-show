from paddleocr import PaddleOCR, draw_ocr
from paddleocr import PPStructure, draw_structure_result, save_structure_res
from PIL import Image
import os
import cv2


def orc_draw_orc(img_path, lang='ch'):
    ocr = PaddleOCR(use_angle_cls=True, lang=lang)

    result = ocr.ocr(img_path, cls=True)
    res = []
    for line in result:
        res.append(line[1][0])
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    im_show.save('result1.jpg')
    return res



def orc_draw_result():
    table_engine = PPStructure(show_log=True)

    save_folder = './output/table'
    img_path = 'tmp/ct/591t1.jpg'
    img = cv2.imread(img_path)
    result = table_engine(img)
    save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

    for line in result:
        line.pop('img')
        print(line)

    font_path = './fonts/simfang.ttf'  # PaddleOCR下提供字体包
    image = Image.open(img_path).convert('RGB')
    im_show = draw_structure_result(image, result, font_path=font_path)
    im_show = Image.fromarray(im_show)
    im_show.save('result.jpg')


if __name__ == '__main__':
    img_path = 'tmp/ct/YD20210705-113354.png'
    orc_draw_orc(img_path)