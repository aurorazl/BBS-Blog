import redis

pool = redis.ConnectionPool(host='192.168.80.128', port=6379,db=0)