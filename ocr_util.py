import easyocr
import io
import sys
from translator import translator

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)

def get_ocr_str(file_path):
    result = reader.readtext(file_path)
    f = open('1.txt', mode='w',encoding='utf-8')
    str = ''
    for i in result:
        word = i[1]
        str = str+word
    return str + '\n' +translator(str)

    
if __name__ == '__main__':
    IMAGE_PATH = "./data/test.jpg"
    print(get_ocr_str(IMAGE_PATH))
