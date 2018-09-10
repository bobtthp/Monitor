#!coding:gbk
import pycurl
import os,sys,time
def getInfo(URL):
    c = pycurl.Curl()
    c.setopt(pycurl.URL,URL) #定义请求的URL常量
    c.setopt(pycurl.CONNECTTIMEOUT,5) #请求等待时间最多5秒
    c.setopt(pycurl.TIMEOUT,5)   #定义请求超时时间（服务器没回应）
    c.setopt(pycurl.NOPROGRESS,1) #屏蔽下载进度条
    c.setopt(pycurl.FORBID_REUSE,1) #交互完成后强制断开连接，不重用
    c.setopt(pycurl.MAXREDIRS,1)  #指定HTTP重定向的最大数为1
    c.setopt(pycurl.DNS_CACHE_TIMEOUT,30) #设置DNS信息保存时间为30秒
    c.setopt(pycurl.USERAGENT,"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81 (Edition Baidu)")
    dic = {}
    info ={'NAMELOOKUP_TIME':'DNS解析时间','CONNECT_TIME':'建立连接时间','PRETRANSFER_TIME':'建立到准备传输所消耗的时间','STARTTRANSFER_TIME':'建立连接到传输开始消耗的时间','TOTAL_TIME':'传输总时间',
           'HTTP_CODE':'HTTP状态码','SIZE_DOWNLOAD':'下载数据包大小','HEADER_SIZE':'HTTP头部大小','SPEED_DOWNLOAD':'平均下载速度'}
    with open(os.path.dirname(os.path.realpath(__file__))+"/content.txt","wb") as indexfile:
        c.setopt(pycurl.WRITEHEADER,indexfile)   #将返回的HTTP HEADER定向到indexfile文件对象
        c.setopt(pycurl.WRITEDATA,indexfile)     #将返回的HTML内容定向到indexfile文件对象
        try:
            c.perform()
        except Exception as e:
            print "Connection error:" +str(e)
            c.close()
            sys.exit()
        dic['NAMELOOKUP_TIME'] = '%.2f ms' % (c.getinfo(c.NAMELOOKUP_TIME)*1000)     #获取DNS解析时间
        dic['CONNECT_TIME'] = '%.2f ms' % (c.getinfo(c.CONNECT_TIME)*1000)          #获取建立连接时间
        dic['PRETRANSFER_TIME'] = '%.2f ms' % (c.getinfo(c.PRETRANSFER_TIME)*1000)  #获取从建立到准备传输所消耗的时间
        dic['STARTTRANSFER_TIME'] = '%.2f ms' % (c.getinfo(c.STARTTRANSFER_TIME)*1000)  #获取从建立连接到传输开始消耗的时间
        dic['TOTAL_TIME'] = '%.2f ms' % (c.getinfo(c.TOTAL_TIME)*1000)              #获取传输总时间
        dic['HTTP_CODE'] = c.getinfo(c.HTTP_CODE)                #获取HTTP状态码
        dic['SIZE_DOWNLOAD'] = '%d bytes/s' % (c.getinfo(c.SIZE_DOWNLOAD))        #获取下载数据包大小
        dic['HEADER_SIZE'] = '%d bytes/s' % (c.getinfo(c.HEADER_SIZE))            #获取HTTP头部大小
        dic['SPEED_DOWNLOAD'] = '%d bytes/s' % (c.getinfo(c.SPEED_DOWNLOAD))      #获取平均下载速度
    for key in info:
        print info[key],':',dic[key]
def main():
    while True:
        URL = raw_input("请输入一个URL地址(Q for exit)：")
        if URL.lower() == 'q':
            sys.exit()
        else:
            getInfo(URL)
if __name__ == '__main__':
    main()


