# import pytesseract
# from PIL import Image,ImageFilter
# from PIL import ImageEnhance
# import pytesser3
import os
import requests

codeurl = 'http://xxx/login/code'
valcode = requests.get(codeurl)
img = '/Users/bob/Desktop/bobtthp/static/code.png'


def getcode(img):
    getim = Image.open(img)
    gryim = getim.convert('L')
    gryim = gryim.filter(ImageFilter.DETAIL)
    gryim = gryim.point(lambda i: i * 0.75)
    gryim = ImageEnhance.Contrast(gryim)
    gryim = gryim.enhance(4)
    return pytesseract.image_to_string(gryim)


data = {
    # "username": "xx",
    # "password": "xxx",
    # "validateCode" : "qwqe"
}
header_base = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "http://kq2.qk365.com/login",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
}

# if __name__ == '__main__':

data['username'] = 'xxx'
data['password'] = 'xxx'
data['validateCode'] = 'nrts'
r = requests.get('http://xxx/login')

r1 = requests.get('http://xxx/login/code', cookies=r.cookies)
context = requests.post('http://xxx/login', data=data, headers=header_base, cookies=r.cookies)

print (context.text)
