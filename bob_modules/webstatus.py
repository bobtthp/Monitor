#!coding:gbk
import pycurl
import os,sys,time
def getInfo(URL):
    c = pycurl.Curl()
    c.setopt(pycurl.URL,URL) #���������URL����
    c.setopt(pycurl.CONNECTTIMEOUT,5) #����ȴ�ʱ�����5��
    c.setopt(pycurl.TIMEOUT,5)   #��������ʱʱ�䣨������û��Ӧ��
    c.setopt(pycurl.NOPROGRESS,1) #�������ؽ�����
    c.setopt(pycurl.FORBID_REUSE,1) #������ɺ�ǿ�ƶϿ����ӣ�������
    c.setopt(pycurl.MAXREDIRS,1)  #ָ��HTTP�ض���������Ϊ1
    c.setopt(pycurl.DNS_CACHE_TIMEOUT,30) #����DNS��Ϣ����ʱ��Ϊ30��
    c.setopt(pycurl.USERAGENT,"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81 (Edition Baidu)")
    dic = {}
    info ={'NAMELOOKUP_TIME':'DNS����ʱ��','CONNECT_TIME':'��������ʱ��','PRETRANSFER_TIME':'������׼�����������ĵ�ʱ��','STARTTRANSFER_TIME':'�������ӵ����俪ʼ���ĵ�ʱ��','TOTAL_TIME':'������ʱ��',
           'HTTP_CODE':'HTTP״̬��','SIZE_DOWNLOAD':'�������ݰ���С','HEADER_SIZE':'HTTPͷ����С','SPEED_DOWNLOAD':'ƽ�������ٶ�'}
    with open(os.path.dirname(os.path.realpath(__file__))+"/content.txt","wb") as indexfile:
        c.setopt(pycurl.WRITEHEADER,indexfile)   #�����ص�HTTP HEADER����indexfile�ļ�����
        c.setopt(pycurl.WRITEDATA,indexfile)     #�����ص�HTML���ݶ���indexfile�ļ�����
        try:
            c.perform()
        except Exception as e:
            print "Connection error:" +str(e)
            c.close()
            sys.exit()
        dic['NAMELOOKUP_TIME'] = '%.2f ms' % (c.getinfo(c.NAMELOOKUP_TIME)*1000)     #��ȡDNS����ʱ��
        dic['CONNECT_TIME'] = '%.2f ms' % (c.getinfo(c.CONNECT_TIME)*1000)          #��ȡ��������ʱ��
        dic['PRETRANSFER_TIME'] = '%.2f ms' % (c.getinfo(c.PRETRANSFER_TIME)*1000)  #��ȡ�ӽ�����׼�����������ĵ�ʱ��
        dic['STARTTRANSFER_TIME'] = '%.2f ms' % (c.getinfo(c.STARTTRANSFER_TIME)*1000)  #��ȡ�ӽ������ӵ����俪ʼ���ĵ�ʱ��
        dic['TOTAL_TIME'] = '%.2f ms' % (c.getinfo(c.TOTAL_TIME)*1000)              #��ȡ������ʱ��
        dic['HTTP_CODE'] = c.getinfo(c.HTTP_CODE)                #��ȡHTTP״̬��
        dic['SIZE_DOWNLOAD'] = '%d bytes/s' % (c.getinfo(c.SIZE_DOWNLOAD))        #��ȡ�������ݰ���С
        dic['HEADER_SIZE'] = '%d bytes/s' % (c.getinfo(c.HEADER_SIZE))            #��ȡHTTPͷ����С
        dic['SPEED_DOWNLOAD'] = '%d bytes/s' % (c.getinfo(c.SPEED_DOWNLOAD))      #��ȡƽ�������ٶ�
    for key in info:
        print info[key],':',dic[key]
def main():
    while True:
        URL = raw_input("������һ��URL��ַ(Q for exit)��")
        if URL.lower() == 'q':
            sys.exit()
        else:
            getInfo(URL)
if __name__ == '__main__':
    main()


