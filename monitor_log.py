#coding:utf-8
import pickle
from ptail import Tail
import time
import os
import sys
import redis
import ConfigParser
from bob_modules import get_conf
class Record_log(Tail):

    """
           overwrite ptail follw modules and it can be record logs
    """
    def follow(self,s=0.01):

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
    def init_conf(self,pname):
        redis_conf = get_conf.get_conf().get('redis')
        log_config = get_conf.get_log_conf(pname)
        self.log_path = log_config.get('basic', 'log_name')
        self.keywords = log_config.get('error_words_monitor', 'monitor_words')
        pool = redis.ConnectionPool(**redis_conf)
        self.rclient = redis.Redis(connection_pool=pool)

    def _write_to_redis(self,line):
        '''
        write logs to redis then search keywords from lines
        '''
        #print(line)
        self.rclient.rpush('test',line)
        self._search_keywords(self.keywords,line)
    def _search_keywords(self,keywords_list,line):
        '''
        :param keywords_list:one or more keywords from sets
        '''
        key_list = keywords_list.split(',')
        for keyword in key_list:
            status = line.find(keyword)
            if status != -1:
                print self.rclient.llen('test')
                print line,keyword


#def init(pname):
#    redis_conf = get_conf.get_conf().get('redis')
#    log_config = get_conf.get_log_conf(pname)
#    log_path = log_config.get('basic','log_name')
#    keywords = log_config.get('error_words_monitor', 'monitor_words')
#    pool = redis.ConnectionPool(**redis_conf)
#    return keywords,pool,log_path

#
if __name__ == '__main__':
    #Record_log('conf/' + log_path).follow()
    pass
    #keywords, pool,log_path = init('test')
    #print log_path
    #Record_log('conf/' + log_path).follow()


