import requests
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

def translator(query):
    url = 'http://fanyi.youdao.com/translate'
    data = {
        "i": query,  # 待翻译的字符串
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": "16081210430989",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CLICKBUTTION"
    }
    res = requests.post(url, data=data).json()
    return res['translateResult'][0][0]['tgt']  # 打印翻译后的结果

if __name__ == '__main__':
    translator('I am chinese') # 输出: hello
