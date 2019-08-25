import execjs
import requests
import json
"""
在py文件中传递js文件中需要的已知参数
"""


def get_params(method, city, type_, startTime, endTime):
    with open('weather.js', 'r', encoding='utf-8') as fp:
        line = fp.read()
    ctx = execjs.compile(line)  # 读取js 中的函数。
    #  调用函数获取post请求的参数
    result = ctx.call('getPostparamCode', method, city, type_, startTime, endTime)
    return result


def get_post_param():
    method = 'GETCITYWEATHER'
    city = '北京'
    type_ = 'HOUR'
    startTime = '2019-08-23 16:00:00'
    endTime = '2019-08-24 19:00:00'
    # 传入参数 ， 调用内部的getPostparamCode函数， 进而调用js文件中的getparam函数
    d = get_params(method, city, type_, startTime, endTime)
    return d


def post_to_have_data(d):
    """
    发出post请求， 来获取加密后的数据， 然而响应的数据依然是要破解的
    :return:
    """
    resp = requests.post(url, data={'d': d})
    if resp.status_code == 200:
        # print(resp.text)  # 依然是要解密的。
        encrypt_data = resp.text  # 但是我们js文件中有了解密的方法， 直接掉用传入要解密的数据解密就是。

        encrypt_data = encrypt_data.encode('utf-8').decode('unicode_escape')
        print(type(encrypt_data))
        return encrypt_data


def decrypt_data(data):
    with open('weather.js', 'r', encoding='utf-8') as fp:
        line = fp.read()
    ctx = execjs.compile(line)  # 再次读取一遍js文件， 要调用 其中的解密函数。
    result = ctx.call('decodeData', data)   # 这就是我们最终解密的数据， 逻辑清晰。
    return result


if __name__ == '__main__':
    url = 'https://www.aqistudy.cn/apinew/aqistudyapi.php'
    d = get_post_param()
    encrypt_data = post_to_have_data(d)  # 从post_to_have_data中获取加密响应数据。

    text = decrypt_data(encrypt_data)
    print(text)

# slashUStr = "\\u897f\\u5357\\u98ce"
# str = slashUStr.encode('utf-8').decode('unicode_escape')
# print(str)
