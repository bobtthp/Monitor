#coding:utf-8
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

from_addr = ''
password = ''
mail = {'qqmail':{'host':'smtp.exmail.qq.com','port':465},
        'hotmail':{'host':'smtp.live.com','port':465},
        'gmail':{'host':'smtp.gmail.com','port':465}
        }


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(),addr.encode('utf-8') if isinstance(addr, unicode) else addr))
def dealinfo(kwargs):
    msg = MIMEText(kwargs['text'], 'plain', 'utf-8')
    msg['From'] = _format_addr('bob <%s>' % from_addr)
    msg['To'] = _format_addr('%s <%s>' % (kwargs['to_name'],kwargs['to_addr']))
    msg['Subject'] = Header(kwargs['subject'],charset='utf-8').encode()
    return msg
def sendmail(kwargs):
    '''
    subject:主题内容
    text:文章内容
    to_addr:对方邮箱地址
    to_name:对方称呼
    '''
    msg = dealinfo(kwargs)
    server = smtplib.SMTP_SSL(mail['qqmail']['host'],mail['qqmail']['port'])
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [kwargs['to_addr']], msg.as_string())
    server.quit()
    server.close()

info = {
    'subject':'主题',
    'text':'文本',
    'to_addr':'',
    'to_name':'bob'
        }
sendmail(info)
