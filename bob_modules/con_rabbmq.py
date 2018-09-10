import pika


class Provider_info:
    def __init__(self, config):
        self.user = config['username']
        self.passwd = config['pwd']
        self.host = config['host']
        self.user_info = pika.PlainCredentials(config['username'], config['pwd'])
        self.push_to_mq()

    def push_to_mq(self):
        r_conn = pika.BlockingConnection(pika.ConnectionParameters(self.host, credentials=self.user_info))
        chan = r_conn.channel()
        chan.queue_declare(queue='test')
        chan.basic_publish(exchange='', routing_key='test', body='it is a test')
        chan.close()


config = {
    'username': 'bob',
    'pwd': 'bob.1234',
    'host': '11.11.11.3'
}
#Provider_info(config)
