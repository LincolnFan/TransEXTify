import easyocr
import io
import sys
from translator import translator

reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)

def get_ocr_str(file_path):
    result = reader.readtext(file_path)
    str = ''
    for i in result:
        word = i[1]
        str = str+word
    return str + '\n' +translator(str)

    
if __name__ == '__main__':
    IMAGE_PATH = "D:/VsCode/TransEXTify/data/test.jpg"
    print(get_ocr_str(IMAGE_PATH))
