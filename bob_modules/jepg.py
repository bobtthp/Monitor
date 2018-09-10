#import pytesseract
#from PIL import Image,ImageFilter
#from PIL import ImageEnhance
#import pytesser3
import os
import requests

codeurl = 'http://kq2.qk365.com/login/code'
valcode = requests.get(codeurl)
img = '/Users/bob/Desktop/bobtthp/static/code.png'
def getcode(img):
    getim = Image.open(img)
    gryim = getim.convert('L')
    gryim = gryim.filter(ImageFilter.DETAIL)
    gryim = gryim.point(lambda i : i * 0.75)
    gryim = ImageEnhance.Contrast(gryim)
    gryim = gryim.enhance(4)
    return pytesseract.image_to_string(gryim)

data = {
    #"username": "gaozequn",
    #"password": "Gzq123321",
    #"validateCode" : "qwqe"
}
header_base = {
"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "zh-CN,zh;q=0.9",
"Cache-Control": "max-age=0",
"Connection": "keep-alive",
"Content-Type": "application/x-www-form-urlencoded",
#"Cookie": "gr_user_id=7982af3d-e5e5-4f71-9eb1-01b58a36a2bc; _ga=GA1.2.909036554.1517660261; Hm_lvt_53c8bf761df44282a0cf7d4949581592=1517660262; JSESSIONID=3C1C34F6619E176BE2B8F2A863DB51E1",
#"Host": "kq2.qk365.com",
#"Origin": "http://kq2.qk365.com",
"Referer": "http://kq2.qk365.com/login",
#"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
}

#if __name__ == '__main__':
#    #with open(img, 'wb') as im:
#        im.write(valcode.content)
#    getcode(img)
#    requests.post()
data['username'] = 'gaozequn'
data['password'] = 'Gzq123321'
data['validateCode'] = 'nrts'
r = requests.get('http://kq2.qk365.com/login')

r1 = requests.get('http://kq2.qk365.com/login/code',cookies = r.cookies)
context = requests.post('http://kq2.qk365.com/login',data=data,headers=header_base,cookies=r.cookies)

print (context.text)
