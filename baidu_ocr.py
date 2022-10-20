
from aip import AipOcr
import sys
import io
from translator import translator

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


def img_to_str(image_path):
    APP_ID = '25988176'
    API_KEY = '3LhapXAf4F8VUGeNHNamUwoX'
    SECRET_KEY = 'VMaq4pLefBtXQPahMQbd9grXIFLoGxIk'
    

    # 初始化AipFace对象
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    """ 可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"  # 中英文混合
    options["detect_direction"] = "true"  # 检测朝向
    options["detect_language"] = "true"  # 是否检测语言
    options["probability"] = "false"  # 是否返回识别结果中每一行的置信度

    with open(image_path, 'rb') as fp:
        image = fp.read()


    """ 带参数调用通用文字识别 """
    result = client.basicGeneral(image, options)
    # 格式化输出-提取需要的部分
    if 'words_result' in result:
        text = ('\n'.join([w['words'] for w in result['words_result']])).strip('n')
    return text+'\n'+translator(text)

if __name__ == '__main__':
    filePath = './data/test.jpg'
    print(img_to_str(filePath))
    
