import ddddocr

def ocr_code(img_path):
    ocr = ddddocr.DdddOcr()

    with open(img_path, 'rb') as f:
        image = f.read()

    res = ocr.classification(image)
    return res