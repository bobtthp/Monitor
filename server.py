#coding:utf-8
import threadpool
from bob_modules import monitor_log,get_conf
import pika
import redis


def Instance(pname):
    log_path =  get_conf.get_log_conf(pname).get('basic','log_name')
    monitor_log.Record_log(log_path,pname).follow()

def main():
    thread_pool = threadpool.ThreadPool(1024)
    plist = get_conf.get_conf().get('pname')
    requests = threadpool.makeRequests(Instance,plist)
    messages = threadpool.makeRequests(Log_consumer,plist)
    #提供消息
    [thread_pool.putRequest(req) for req in requests]
    #消费消息
    [thread_pool.putRequest(req) for req in messages]
    thread_pool.wait()
    #[thread_pool.putRequest(req) for req in requests ]
    #thread_pool.wait()
def Log_consumer(pname):
    config = get_conf.get_conf().get('rabbitmq')
    user_info = pika.PlainCredentials(config['username'], config['pwd'])
    mq_conn = pika.BlockingConnection(pika.ConnectionParameters(config['host'], credentials=user_info))
    chan = mq_conn.channel()
    chan.queue_declare(queue=pname)
    chan.basic_consume(callback,queue=pname,no_ack=True)
    import time
    time.sleep(1)
    chan.start_consuming()
def callback(chan,method,conf,body):
    redis_conf = get_conf.get_conf().get('redis')
    pool = redis.ConnectionPool(**redis_conf)
    rclient = redis.Redis(connection_pool=pool)
    pname =  body.split(',')[1]
    line_num = int(body.split(',')[0])
    print line_num
    print rclient.lrange(pname,line_num-100,line_num+100)






if __name__ == '__main__':
    #Log_provider()
    if __name__ == '__main__':
        main()