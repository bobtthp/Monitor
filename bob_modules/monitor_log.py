# coding:utf-8
import os
import sys
import time
import redis
from bob_modules import get_conf
from bob_modules.ptail import Tail
import pika


class Record_log(Tail):
    """
           overwrite ptail follw modules and it can be record logs
    """

    def __init__(self, tailed_file, pname):
        ''' Initiate a Tail instance.
            Check for file validity, assigns callback function to standard out.

            Arguments:
                tailed_file - File to be followed. '''
        self.check_file_exist(tailed_file)
        self.tailed_file = tailed_file
        self.callback = sys.stdout.write
        self.try_count = 0
        self.pname = pname

        try:
            self.file_ = open(self.tailed_file, "r")
            self.size = os.path.getsize(self.tailed_file)

            # Go to the end of file
            self.file_.seek(0, 2)
        except:
            raise

    def reload_tailed_file(self):
        """ Reload tailed file when it be empty be `echo "" > tailed file`, or
            segmentated by logrotate.
        """
        try:
            self.file_ = open(self.tailed_file, "r")
            self.size = os.path.getsize(self.tailed_file)

            # Go to the head of file
            self.file_.seek(0, 1)

            return True
        except:
            return False

    def follow(self, s=0.01):

        while True:
            _size = os.path.getsize(self.tailed_file)
            if _size < self.size:
                while self.try_count < 3:
                    if not self.reload_tailed_file():
                        self.try_count += 1
                    else:
                        self.try_count = 0
                        self.size = os.path.getsize(self.tailed_file)
                        break
                    time.sleep(0.1)

                if self.try_count == 3:
                    raise Exception("Open %s failed after try 3 times" % self.tailed_file)
            else:
                self.size = _size

            curr_position = self.file_.tell()
            line = self.file_.readline()

            if not line:
                self.file_.seek(curr_position)
            elif not line.endswith("\n"):
                self.file_.seek(curr_position)
            else:
                self._write_to_redis(line)
            time.sleep(s)

    def _write_to_redis(self, line):
        '''
        write logs to redis then search keywords from lines
        '''
        # print(line)
        log_config = get_conf.get_log_conf(self.pname)
        keywords = log_config.get('error_words_monitor', 'monitor_words')
        redis_conf = get_conf.get_conf().get('redis')
        pool = redis.ConnectionPool(**redis_conf)
        rclient = redis.Redis(connection_pool=pool)
        rclient.rpush(self.pname, line)
        line_num = rclient.llen(self.pname)
        self._search_keywords(keywords, line, line_num)

    def _search_keywords(self, keywords_list, line, line_num):
        '''
        :param keywords_list:one or more keywords from sets
        '''
        key_list = keywords_list.split(',')
        for keyword in key_list:
            status = line.find(keyword)
            if status != -1:
                # print line,line_num
                self._push_message_mq(line_num)

    def _push_message_mq(self, line_num):
        config = get_conf.get_conf().get('rabbitmq')
        user_info = pika.PlainCredentials(config['username'], config['pwd'])
        mq_conn = pika.BlockingConnection(pika.ConnectionParameters(config['host'], credentials=user_info))
        chan = mq_conn.channel()
        chan.queue_declare(queue=self.pname)
        chan.basic_publish(exchange='', routing_key=self.pname, body=str(line_num) + ',' + self.pname)
        chan.close()
