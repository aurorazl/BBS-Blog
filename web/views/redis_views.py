import redis
from django.shortcuts import render
from utils.redis_pool import pool

def index(request):
    conn = redis.Redis(connection_pool=pool)
    conn.hset('h','age',18)

def order(request):
    conn = redis.Redis(connection_pool=pool)
    conn.hget('h','age')

def new_index(request):
    from django_redis import get_redis_connection
    conn = get_redis_connection("default")