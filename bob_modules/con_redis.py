#!/usr/bin/python
import redis

redis_config = {
    "host" : "192.168.122.3",
    "port" : 6379,
    "decode_responses" : True
}
pool = redis.ConnectionPool(**redis_config)
r_client = redis.Redis(connection_pool=pool)

def test(pname):
    s_postion = r_client.llen(pname)
    print s_postion
    for i in range(100):
        pass
        #r_client.rpush(pname,'t' + str(i))
        #r_client.rpop(pname)
    print r_client.lrange(pname,50,400)

test('test')

#f#or num in range(1000):
#    key = 'bob' + str(num)
#    #r_client.set(key,num)
print  'abc'.find('da')

#





